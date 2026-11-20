# REIBM# Relational Evidence and Information Boundary Model (REIBM)

**A Mathematical Extension of the Relational Boundary Framework (RBF)**

**Author:** Christopher Thomas Ronio  
**Framework:** Relational Boundary Framework  
**Status:** Proposed mathematical research model  
**Version:** 1.0.0

---

## 1. Abstract

The Relational Evidence and Information Boundary Model (REIBM) is a proposed mathematical framework for classifying information, evaluating evidence, preserving uncertainty, and identifying the boundaries between established facts and unsupported conclusions.

REIBM extends the Relational Boundary Framework (RBF) into information systems where linguistic expressions, contextual relationships, evidence provenance, and selection criteria influence how information is interpreted.

The model introduces three principal information states:

- **Known:** Information supported by available evidence.
- **Possible:** Interpretations consistent with available evidence but not established as facts.
- **Unknown:** Information that cannot currently be established.

Its objective is to provide a formal structure for analyzing information without allowing unsupported assumptions to become factual conclusions.

Potential applications include missing-person databases, historical archives, scientific research, knowledge representation, artificial intelligence, and mathematical reasoning systems.

## 2. Foundational RBF Principle

The foundational relational structure is:

\[
R=I\cup O\cup B
\]

Where:

- \(I\) = Inside Boundary.
- \(O\) = Outside Boundary.
- \(B\) = Boundary Region.
- \(R\) = Complete relational classification domain.

For a strict partition, these regions must be mutually disjoint:

\[
I\cap O=I\cap B=O\cap B=\varnothing
\]

And:

\[
I\cup O\cup B=R
\]

The three regions represent the relationship between an information system and the conditions governing its inclusion, exclusion, and conditional acceptance.

### 2.1 Inside

Information satisfying the established inclusion criteria.

### 2.2 Outside

Information that does not satisfy the established inclusion criteria.

### 2.3 Boundary

Information requiring additional conditions, review, or evidence before classification.

The Boundary is not automatically an unknown state. It represents a relational classification requiring further evaluation.

## 3. Mathematical Information Model

Define an information transformation:

\[
F(\ell,c)\rightarrow \mathcal{P}(M)
\]

Where:

- \(\ell\) = Linguistic expression.
- \(c\) = Context.
- \(M\) = Domain of possible meanings.
- \(\mathcal{P}(M)\) = Power set of possible meanings.

The function returns the meanings compatible with the available expression and context.

For example:

\[
\ell=\text{"Missing"}
\]

The expression alone does not establish:

- Abduction.
- Death.
- Voluntary disappearance.
- Recovery.
- Current whereabouts.

The information system must preserve these distinctions.

A probabilistic extension could assign probabilities to possible meanings, but probability must not be confused with evidentiary confirmation.

## 4. Relational Evidence Classification

Define the evidence state of a record \(C_i\):

\[
E(C_i)=(K_i,P_i,U_i)
\]

Where:

- \(K_i\) = Known information.
- \(P_i\) = Possible interpretations.
- \(U_i\) = Unknown information.

Each component represents a different epistemic relationship.

### 4.1 Known

Information supported by identifiable evidence or an appropriately attributed source.

### 4.2 Possible

Information consistent with the available record but not independently established.

### 4.3 Unknown

Information for which the available evidence does not support a determination.

An unknown value must not automatically become a negative assertion.

For example:

\[
\text{Unknown cause}\neq\text{No cause}
\]

Likewise:

\[
\text{No documented recovery}\neq\text{Confirmed unrecovered}
\]

The model preserves the difference between absence of evidence and evidence of absence.

## 5. Case Record Architecture

An individual information record can be represented as:

\[
C_i=(ID,D,L,A,G,N,S,E)
\]

Where:

| Symbol | Description |
|---|---|
| ID | Record identifier |
| D | Date information |
| L | Location information |
| A | Age or relevant attributes |
| G | Classification |
| N | Narrative information |
| S | Current documented status |
| E | Evidence and provenance |

Each record should maintain a distinction between the original source statement and any subsequent interpretation.

## 6. Relational Information Boundary Function

Define the classification function:

\[
F_R(C_i)=
\begin{cases}
I & \text{if inclusion criteria are satisfied}\\
O & \text{if exclusion criteria are satisfied}\\
B & \text{if conditional evaluation is required}
\end{cases}
\]

The function determines the record's relationship to the information system.

It does not determine the underlying real-world cause of an event.

This distinction is essential:

\[
\text{Database Classification}
\neq
\text{Real-World Truth}
\]

## 7. Relational Information Preservation

A central proposed property of REIBM is Relational Information Preservation.

A transformation must not silently promote an unsupported possibility into an established fact.

Let \(T\) represent an information transformation.

Define:

\[
K(T(C))\subseteq K(C)\cup N(C)
\]

Where:

- \(K(C)\) = Previously established information.
- \(N(C)\) = New independently sourced information.
- \(K(T(C))\) = Established information after transformation.

This condition requires new factual claims to have traceable supporting information.

A transformation that introduces unsupported conclusions violates the preservation condition.

### 7.1 Uncertainty Preservation

Define:

\[
U(C)\rightarrow U(T(C))
\]

when no new evidence resolves the uncertainty.

The expression does not require unknown information to remain permanently unknown. It requires uncertainty to remain explicit until sufficient evidence changes its classification.

### 7.2 Provenance Preservation

Every established claim should retain its source relationship:

\[
Q=(q,s,t,v)
\]

Where:

- \(q\) = Claim.
- \(s\) = Source.
- \(t\) = Time of source observation or publication.
- \(v\) = Verification status.

This allows the system to distinguish original information from derived interpretations.

## 8. Selection Bias and Collection Boundaries

A collection of records is not necessarily representative of the entire population from which records originate.

Let:

- \(U\) = Complete target population.
- \(S\) = Selected records.
- \(X\) = A characteristic being measured.

Then:

\[
P(X\mid S)\neq P(X)
\]

in general.

This is a selection-bias problem.

For example, The Charley Project maintains a selected collection of missing-person profiles subject to its own inclusion criteria.

Consequently:

\[
\text{Charley Project Cases}
\neq
\text{All Missing-Person Cases}
\]

Statistical conclusions based exclusively on that collection describe the selected collection unless additional evidence establishes broader representativeness.

REIBM therefore treats collection boundaries as an essential part of data interpretation.

## 9. Computational Architecture

The proposed implementation consists of six independent components.

| Component | Responsibility |
|---|---|
| Boundary Engine | Inside, Outside, Boundary classification |
| Linguistic Engine | Expression and context interpretation |
| Evidence Engine | Known, Possible, Unknown classification |
| Provenance Engine | Source identification and traceability |
| Transformation Engine | Information updates and preservation |
| Verification Engine | Mathematical and logical consistency tests |

The components should be independently testable.

## 10. Python Reference Implementation

The following implementation provides a minimal executable foundation.

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
                    "state": item.state.value
                }
                for item in record.evidence
            ]
        }


if __name__ == "__main__":
    engine = REIBM()

    record = CaseRecord(
        identifier="CASE-001",
        evidence=[
            Evidence(
                claim="Person reported missing",
                source="Example source",
                independently_verified=True
            ),
            Evidence(
                claim="Cause of disappearance",
                source=None
            )
        ]
    )

    engine.classify(
        record,
        included=True,
        excluded=False
    )

    print(engine.information_report(record))
```

**Implementation note:** Independent verification in this reference implementation is represented by an explicit input flag. A production system must implement actual source validation, identity checks, temporal tracking, and conflict resolution. A supplied flag alone does not establish that evidence is true.

## 11. Mathematical Verification Tests

The following properties are proposed for independent testing.

**Test 1 — Boundary Exclusivity**

A record must occupy exactly one primary boundary region.

\[
I\oplus O\oplus B
\]

Here, \(\oplus\) denotes exclusive classification.

**Test 2 — Unknown Preservation**

An information transformation without new evidence must not convert an unknown claim into a known claim.

**Test 3 — Provenance Requirement**

Every established claim must have an identifiable supporting source.

**Test 4 — Classification Independence**

The classification of a record must not automatically establish the truth of its narrative.

**Test 5 — Contradiction Detection**

If two claims conflict, the system must preserve the conflict for evaluation rather than silently selecting one.

**Test 6 — Selection-Boundary Awareness**

Statistical results must identify the population and selection criteria to which they apply.

These tests define the initial verification program; they are not claims that the framework has already passed a complete mathematical proof.

## 12. Applications

REIBM is proposed for the following domains:

1. **Missing-Person Information Systems:** Distinguishing documented facts from possible explanations.
2. **Artificial Intelligence:** Reducing unsupported factual inference.
3. **Scientific Research:** Separating observations, hypotheses, and unknowns.
4. **Historical Archives:** Preserving source attribution and uncertainty.
5. **Set Theory:** Modeling membership and conditional boundaries.
6. **Mathematical Logic:** Detecting contradictory or unsupported transformations.
7. **Knowledge Graphs:** Preserving relationships between claims, evidence, and sources.

## 13. Limitations

REIBM is a proposed research framework, not an established mathematical standard.

Its classification results depend on the quality of the supplied information, source validation, and explicitly defined boundary conditions.

The model does not independently establish the truth of a source, determine the cause of a disappearance, or guarantee that all possible interpretations have been identified.

Probabilistic conclusions require additional assumptions and statistical validation.

Formal proofs and independent computational testing are required before stronger mathematical guarantees can be claimed.

## 14. Research Roadmap

- [ ] Formalize the boundary classification axioms.
- [ ] Define a rigorous semantics for Known, Possible, and Unknown.
- [ ] Develop contradiction detection.
- [ ] Implement source provenance validation.
- [ ] Develop transformation and uncertainty-preservation tests.
- [ ] Test against synthetic information datasets.
- [ ] Evaluate selection bias using known population data.
- [ ] Integrate with the Relational Boundary Framework.
- [ ] Develop a unified proof engine for set theory, geometry, topology, and mathematical logic.
- [ ] Publish reproducible computational results.

## 15. Relationship to the Relational Boundary Framework

REIBM extends the RBF principle:

\[
R=I+O+B
\]

into an evidence-oriented information architecture.

Its central objective is to establish a relationship between:

\[
\text{Boundary}
+
\text{Information}
+
\text{Evidence}
+
\text{Transformation}
\]

The resulting model provides a common structure for determining what information belongs within a system, what conclusions are supported, and what remains outside the established knowledge boundary.

## 16. Authorship and Research Attribution

**Author:** Christopher Thomas Ronio

**Research Title:** Relational Evidence and Information Boundary Model (REIBM)

**Parent Framework:** Relational Boundary Framework (RBF)

This document establishes the author's stated research attribution and describes the proposed mathematical framework.

The authorship statement is not a claim of independent legal verification or proof of priority.

## 17. Conclusion

The Relational Evidence and Information Boundary Model proposes that information must be evaluated not only by its content, but also by its relationship to the boundaries, context, and evidence supporting it.

Its fundamental principle is:

\[
\boxed{
\text{Information}
\neq
\text{Evidence}
\neq
\text{Conclusion}
}
\]

These three concepts are related, but they are not interchangeable.

By preserving their distinctions, REIBM provides a foundation for developing more rigorous information systems, mathematical reasoning engines, and evidence-aware artificial intelligence.

---

**End of README.md**

**Christopher Thomas Ronio**  
Relational Boundary Framework Research
