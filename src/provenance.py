
"""
REIBM Provenance Engine
=======================

Tracks the origin, dependencies, and transformation history
of information records.

Author: Christopher Thomas Ronio

Core objectives:
    - Identify original information sources.
    - Preserve dependencies between records.
    - Track transformations and their inputs/outputs.
    - Detect circular dependencies.
    - Identify records without a traceable source origin.

A traceable source is not automatically a truthful source.
Source independence must be established separately.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class OriginStatus(str, Enum):
    SOURCE_BACKED = "source_backed"
    DERIVED_SOURCE_BACKED = "derived_source_backed"
    CIRCULAR = "circular"
    UNRESOLVED = "unresolved"
    INVALID = "invalid"


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    source_type: str
    locator: str
    independent_group_id: str | None = None

    def __post_init__(self):
        for name in ("source_id", "source_type", "locator"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{name} must be a non-empty string."
                )


@dataclass(frozen=True)
class ProvenanceRecord:
    artifact_id: str
    artifact_type: str
    source_id: str | None = None
    parent_ids: tuple[str, ...] = ()
    transformation_id: str | None = None

    def __post_init__(self):
        for name in ("artifact_id", "artifact_type"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{name} must be a non-empty string."
                )

        if self.source_id is not None and not self.source_id.strip():
            raise ValueError("source_id cannot be blank.")

        if self.transformation_id is not None:
            if not self.transformation_id.strip():
                raise ValueError(
                    "transformation_id cannot be blank."
                )

        if len(self.parent_ids) != len(set(self.parent_ids)):
            raise ValueError("Duplicate parent IDs are not allowed.")


@dataclass(frozen=True)
class TransformationRecord:
    transformation_id: str
    rule_id: str
    input_ids: tuple[str, ...]
    output_ids: tuple[str, ...]

    def __post_init__(self):
        for name in ("transformation_id", "rule_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{name} must be a non-empty string."
                )

        if len(self.input_ids) != len(set(self.input_ids)):
            raise ValueError("Duplicate transformation inputs.")

        if len(self.output_ids) != len(set(self.output_ids)):
            raise ValueError("Duplicate transformation outputs.")


@dataclass(frozen=True)
class ProvenanceIssue:
    code: str
    message: str
    artifact_id: str | None = None


@dataclass(frozen=True)
class ProvenanceReport:
    valid: bool
    issues: tuple[ProvenanceIssue, ...]


@dataclass(frozen=True)
class OriginTrace:
    artifact_id: str
    status: OriginStatus
    source_ids: tuple[str, ...]
    visited_artifact_ids: tuple[str, ...]


class ProvenanceLedger:
    """
    Immutable-input provenance evaluator.

    The ledger does not modify source records or artifacts.
    """

    def __init__(
        self,
        sources: Iterable[SourceRecord] = (),
        artifacts: Iterable[ProvenanceRecord] = (),
        transformations: Iterable[TransformationRecord] = (),
    ):
        self.sources = tuple(sources)
        self.artifacts = tuple(artifacts)
        self.transformations = tuple(transformations)

        self.source_index = {
            item.source_id: item for item in self.sources
        }
        self.artifact_index = {
            item.artifact_id: item for item in self.artifacts
        }
        self.transformation_index = {
            item.transformation_id: item
            for item in self.transformations
        }

    def validate(self) -> ProvenanceReport:
        issues = []

        # Validate identifier uniqueness.
        for records, identifier, label in (
            (self.sources, "source_id", "source"),
            (self.artifacts, "artifact_id", "artifact"),
            (
                self.transformations,
                "transformation_id",
                "transformation",
            ),
        ):
            seen = set()
            for record in records:
                value = getattr(record, identifier)
                if value in seen:
                    issues.append(
                        ProvenanceIssue(
                            "DUPLICATE_ID",
                            f"Duplicate {label} ID: {value}",
                        )
                    )
                seen.add(value)

        # Validate artifact dependencies.
        for artifact in self.artifacts:

            if (
                artifact.source_id is not None
                and artifact.source_id not in self.source_index
            ):
                issues.append(
                    ProvenanceIssue(
                        "MISSING_SOURCE",
                        f"Unknown source {artifact.source_id!r}.",
                        artifact.artifact_id,
                    )
                )

            for parent_id in artifact.parent_ids:
                if parent_id not in self.artifact_index:
                    issues.append(
                        ProvenanceIssue(
                            "MISSING_PARENT",
                            f"Unknown parent artifact {parent_id!r}.",
                            artifact.artifact_id,
                        )
                    )

            if artifact.transformation_id is not None:
                if (
                    artifact.transformation_id
                    not in self.transformation_index
                ):
                    issues.append(
                        ProvenanceIssue(
                            "MISSING_TRANSFORMATION",
                            "Referenced transformation does not exist.",
                            artifact.artifact_id,
                        )
                    )

            if artifact.parent_ids and artifact.transformation_id is None:
                issues.append(
                    ProvenanceIssue(
                        "MISSING_TRANSFORMATION_LINK",
                        "Derived artifact has parents but no transformation.",
                        artifact.artifact_id,
                    )
                )

        # Validate transformation inputs and outputs.
        for transformation in self.transformations:

            for artifact_id in (
                transformation.input_ids
                + transformation.output_ids
            ):
                if artifact_id not in self.artifact_index:
                    issues.append(
                        ProvenanceIssue(
                            "UNKNOWN_TRANSFORMATION_ARTIFACT",
                            f"Unknown artifact {artifact_id!r}.",
                        )
                    )

            for output_id in transformation.output_ids:
                output = self.artifact_index.get(output_id)

                if output is None:
                    continue

                if output.transformation_id != transformation.transformation_id:
                    issues.append(
                        ProvenanceIssue(
                            "TRANSFORMATION_OUTPUT_MISMATCH",
                            "Output artifact does not reference its "
                            "declared transformation.",
                            output_id,
                        )
                    )

                if not set(output.parent_ids).issubset(
                    set(transformation.input_ids)
                ):
                    issues.append(
                        ProvenanceIssue(
                            "INVALID_PARENT_RELATION",
                            "Output references a parent not declared "
                            "as a transformation input.",
                            output_id,
                        )
                    )

        # Detect dependency cycles.
        cycles = self._find_cycles()

        for artifact_id in cycles:
            issues.append(
                ProvenanceIssue(
                    "CIRCULAR_DEPENDENCY",
                    "Artifact participates in a dependency cycle.",
                    artifact_id,
                )
            )

        return ProvenanceReport(
            valid=not issues,
            issues=tuple(issues),
        )

    def _find_cycles(self) -> set[str]:
        """
        Depth-first cycle detection over artifact dependencies.
        """
        visiting = set()
        visited = set()
        cycle_nodes = set()

        def visit(artifact_id, path):
            if artifact_id in visiting:
                cycle_start = path.index(artifact_id)
                cycle_nodes.update(path[cycle_start:])
                return

            if artifact_id in visited:
                return

            artifact = self.artifact_index.get(artifact_id)
            if artifact is None:
                return

            visiting.add(artifact_id)
            path.append(artifact_id)

            for parent_id in artifact.parent_ids:
                visit(parent_id, path)

            path.pop()
            visiting.remove(artifact_id)
            visited.add(artifact_id)

        for artifact_id in self.artifact_index:
            visit(artifact_id, [])

        return cycle_nodes

    def trace_origin(self, artifact_id: str) -> OriginTrace:
        """
        Recursively trace an artifact to its identifiable sources.

        A cycle is not treated as proof of an independent origin.
        """

        if artifact_id not in self.artifact_index:
            return OriginTrace(
                artifact_id=artifact_id,
                status=OriginStatus.INVALID,
                source_ids=(),
                visited_artifact_ids=(),
            )

        cycle_nodes = self._find_cycles()

        if artifact_id in cycle_nodes:
            return OriginTrace(
                artifact_id=artifact_id,
                status=OriginStatus.CIRCULAR,
                source_ids=(),
                visited_artifact_ids=tuple(sorted(cycle_nodes)),
            )

        source_ids = set()
        visited = set()
        unresolved = False

        def walk(current_id):
            nonlocal unresolved

            if current_id in visited:
                return

            visited.add(current_id)

            record = self.artifact_index.get(current_id)

            if record is None:
                unresolved = True
                return

            if record.source_id is not None:
                if record.source_id in self.source_index:
                    source_ids.add(record.source_id)
                else:
                    unresolved = True

            if not record.parent_ids and record.source_id is None:
                unresolved = True

            for parent_id in record.parent_ids:
                walk(parent_id)

        walk(artifact_id)

        if unresolved or not source_ids:
            status = OriginStatus.UNRESOLVED

        elif self.artifact_index[artifact_id].parent_ids:
            status = OriginStatus.DERIVED_SOURCE_BACKED

        else:
            status = OriginStatus.SOURCE_BACKED

        return OriginTrace(
            artifact_id=artifact_id,
            status=status,
            source_ids=tuple(sorted(source_ids)),
            visited_artifact_ids=tuple(sorted(visited)),
        )
