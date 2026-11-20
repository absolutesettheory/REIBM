
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class SemanticStatus(str, Enum):
    EXPLICIT = "explicit"
    DERIVED = "derived"
    POSSIBLE = "possible"
    UNKNOWN = "unknown"
    CONTRADICTED = "contradicted"


@dataclass(frozen=True)
class SemanticFact:
    subject: str
    predicate: str
    value: str
    status: SemanticStatus
    source_id: str
    rule_id: str | None = None


@dataclass(frozen=True)
class SemanticInterpretation:
    subject: str
    facts: tuple[SemanticFact, ...]
    unresolved: FrozenSet[str]


def interpret_case(
    subject: str,
    recorded_fields: dict[str, str],
    source_id: str,
) -> SemanticInterpretation:
    facts = []
    unresolved = set()

    for field, value in recorded_fields.items():
        if not value or not value.strip():
            unresolved.add(field)
            continue

        facts.append(
            SemanticFact(
                subject=subject,
                predicate=field,
                value=value.strip(),
                status=SemanticStatus.EXPLICIT,
                source_id=source_id,
            )
        )

    # A missing-person classification is not proof
    # of abduction, death, or recovery.
    for claim in (
        "abducted",
        "deceased",
        "recovered",
        "current_location",
    ):
        if not any(
            fact.predicate == claim for fact in facts
        ):
            unresolved.add(claim)

    return SemanticInterpretation(
        subject=subject,
        facts=tuple(facts),
        unresolved=frozenset(unresolved),
    )
