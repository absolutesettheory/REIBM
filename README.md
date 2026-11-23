# Relational Evidence and Information Boundary Model (REIBM)

**A mathematical extension of the Relational Boundary Framework (RBF)**

![Status](https://img.shields.io/badge/status-proposed%20research-blue)
![Python](https://img.shields.io/badge/python-3.10+-yellow)
![License](https://img.shields.io/badge/license-Apache%202.0-green)

REIBM is a proposed framework for evaluating information while preserving uncertainty, provenance, and the difference between a supported fact and a possible interpretation.

> **Project status:** Research model under active formalization. The implementation is a minimal reference, not a production-ready evidence-validation system.

## Overview

The model organizes information into three epistemic states:

| State | Meaning |
|---|---|
| **Known** | Supported by identifiable evidence or an appropriately attributed source |
| **Possible** | Consistent with the evidence, but not independently established |
| **Unknown** | Not currently determinable from the available evidence |

REIBM extends the Relational Boundary Framework by relating records to a three-part classification domain:

```text
R = I ∪ O ∪ B
```

- **I — Inside:** satisfies the inclusion criteria
- **O — Outside:** does not satisfy the inclusion criteria
- **B — Boundary:** requires additional review or evidence

## Core Principles

### Preserve uncertainty

An unknown claim must not silently become a factual conclusion.

```text
Unknown cause ≠ No cause
No documented recovery ≠ Confirmed unrecovered
```

### Preserve provenance

Established claims should retain a traceable relationship to their source, observation time, and verification status.

### Preserve information through transformations

A transformation may add newly established information only from traceable, independently sourced evidence. It must not promote a possibility into a fact or remove unresolved uncertainty.

### Preserve collection boundaries

A selected collection is not automatically representative of its source population:

```text
P(X | selected records) ≠ P(X)
```

This is particularly important when using databases such as missing-person collections for statistical analysis.

## Reference Implementation

The repository includes a minimal Python implementation demonstrating boundary classification and evidence states.

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Boundary(Enum):
    INSIDE = "INSIDE"
    OUTSIDE = "OUTSIDE"
    CONDITIONAL = "BOUNDARY"


class EvidenceState(Enum):
    KNOWN = "KNOWN"
    POSSIBLE = "POSSIBLE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Evidence:
    claim: str
    source: Optional[str] = None
    independently_verified: bool = False

    @property
    def state(self):
        if not self.claim:
            return EvidenceState.UNKNOWN

        if self.independently_verified and self.source:
            return EvidenceState.KNOWN

        return EvidenceState.POSSIBLE


@dataclass
class CaseRecord:
    identifier: str
    evidence: list = field(default_factory=list)
    classification: Boundary = Boundary.CONDITIONAL


class REIBM:
    def classify(self, record, included, excluded):
        if included and not excluded:
            record.classification = Boundary.INSIDE
        elif excluded:
            record.classification = Boundary.OUTSIDE
        else:
            record.classification = Boundary.CONDITIONAL

        return record.classification

    def evaluate_evidence(self, evidence):
        return evidence.state

    def information_report(self, record):
        return {
            "identifier": record.identifier,
            "boundary": record.classification.value,
            "evidence": [
                {
                    "claim": item.claim,
                    "source": item.source,
                    "state": item.state.value,
                }
                for item in record.evidence
            ],
        }


if __name__ == "__main__":
    engine = REIBM()
    record = CaseRecord(
        identifier="CASE-001",
        evidence=[
            Evidence(
                claim="Person reported missing",
                source="Example source",
                independently_verified=True,
            ),
            Evidence(claim="Cause of disappearance", source=None),
        ],
    )

    engine.classify(record, included=True, excluded=False)
    print(engine.information_report(record))
```

### Implementation considerations

The `independently_verified` flag in the reference model represents a verification decision supplied by the caller. A production implementation would need real source validation, identity checks, confidence or verification policies, contradiction detection, and audit logging.

## Proposed Architecture

| Component | Responsibility |
|---|---|
| **Boundary Engine** | Inside, Outside, and Boundary classification |
| **Linguistic Engine** | Expression and context interpretation |
| **Evidence Engine** | Known, Possible, and Unknown classification |
| **Provenance Engine** | Source identification and traceability |
| **Transformation Engine** | Information updates and uncertainty preservation |
| **Verification Engine** | Mathematical and logical consistency tests |

## Verification Properties

The following properties define proposed testing criteria:

1. **Boundary exclusivity** — a record occupies exactly one primary boundary region.
2. **Unknown preservation** — an unchanged information state does not become known without new evidence.
3. **Provenance requirement** — established claims retain identifiable supporting sources.
4. **Classification independence** — database classification does not establish real-world truth.
5. **Contradiction detection** — conflicting claims remain visible for evaluation instead of being silently resolved.
6. **Selection-boundary awareness** — statistical results identify their target population and selection criteria.

These properties are verification goals, not claims that the framework has completed formal proof or independent empirical validation.

## Potential Applications

- Missing-person information systems
- Historical archives
- Scientific and knowledge research
- Artificial intelligence and knowledge graphs
- Set theory and mathematical logic
- Source-attribution and evidence-traceability systems

## Research Roadmap

- [ ] Formalize the boundary classification axioms
- [ ] Define rigorous semantics for Known, Possible, and Unknown
- [ ] Develop contradiction detection
- [ ] Implement source provenance validation
- [ ] Add transformation and uncertainty-preservation tests
- [ ] Test against synthetic information datasets
- [ ] Evaluate selection bias using known population data
- [ ] Integrate with the Relational Boundary Framework
- [ ] Develop a proof engine for set theory, geometry, topology, and logic
- [ ] Publish reproducible computational results

## Limitations

REIBM is a proposed research framework, not an established mathematical standard.

Its classifications depend on source quality, explicitly defined inclusion criteria, and independently validated evidence. The model does not establish real-world truth, determine the cause of an event, or guarantee complete interpretation of an information domain.

Probabilistic conclusions require additional assumptions and statistical validation. Formal proofs and independent testing are required before stronger guarantees can be made.

## Fundamental Principle

```text
Information ≠ Evidence ≠ Conclusion
```

These concepts are related but not interchangeable. Preserving their distinctions provides a foundation for rigorous information systems and evidence-aware reasoning.

## Related Project

- [The Charley Project](https://charleyproject.org)

## Authorship

**Author:** Christopher Thomas Ronio

**Framework:** Relational Boundary Framework (RBF)

**Research Title:** Relational Evidence and Information Boundary Model (REIBM)

This README describes the author's proposed framework and is not a claim of independently verified legal priority or an established mathematical standard.

## License

Distributed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.
