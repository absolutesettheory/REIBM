
import unittest

from reimb.semantics import (
    SemanticFact,
    SemanticStatus,
)
from reimb.evidence import (
    EvidenceRecord,
    EvidencePolarity,
    EvidenceValidation,
    EvidenceStatus,
    FactReference,
    assess_fact,
)


class TestREIBMEvidence(unittest.TestCase):

    def setUp(self):
        self.fact = SemanticFact(
            subject="case-001",
            predicate="recovered",
            value="yes",
            status=SemanticStatus.EXPLICIT,
            source_id="source-001",
        )

        self.target = FactReference(
            "case-001",
            "recovered",
            "yes",
        )

    def make_evidence(self, evidence_id, polarity, validation):
        return EvidenceRecord(
            evidence_id=evidence_id,
            target=self.target,
            polarity=polarity,
            source_id=f"source-{evidence_id}",
            validation=validation,
        )

    def test_no_evidence_is_unknown(self):
        result = assess_fact(self.fact, [])
        self.assertEqual(
            result.evidence_status,
            EvidenceStatus.UNKNOWN,
        )

    def test_admissible_support(self):
        result = assess_fact(
            self.fact,
            [
                self.make_evidence(
                    "E1",
                    EvidencePolarity.SUPPORTS,
                    EvidenceValidation.ADMISSIBLE,
                )
            ],
        )
        self.assertEqual(
            result.evidence_status,
            EvidenceStatus.SUPPORTED,
        )

    def test_admissible_refutation(self):
        result = assess_fact(
            self.fact,
            [
                self.make_evidence(
                    "E1",
                    EvidencePolarity.REFUTES,
                    EvidenceValidation.ADMISSIBLE,
                )
            ],
        )
        self.assertEqual(
            result.evidence_status,
            EvidenceStatus.REFUTED,
        )

    def test_conflicting_evidence_is_preserved(self):
        result = assess_fact(
            self.fact,
            [
                self.make_evidence(
                    "E1",
                    EvidencePolarity.SUPPORTS,
                    EvidenceValidation.ADMISSIBLE,
                ),
                self.make_evidence(
                    "E2",
                    EvidencePolarity.REFUTES,
                    EvidenceValidation.ADMISSIBLE,
                ),
            ],
        )
        self.assertEqual(
            result.evidence_status,
            EvidenceStatus.CONFLICT,
        )

    def test_unassessed_evidence_is_excluded(self):
        result = assess_fact(
            self.fact,
            [
                self.make_evidence(
                    "E1",
                    EvidencePolarity.SUPPORTS,
                    EvidenceValidation.UNASSESSED,
                )
            ],
        )
        self.assertEqual(
            result.evidence_status,
            EvidenceStatus.UNKNOWN,
        )
        self.assertEqual(
            result.excluded_evidence,
            ("E1",),
        )

    def test_explicit_does_not_mean_verified(self):
        result = assess_fact(self.fact, [])
        self.assertEqual(
            result.semantic_status,
            SemanticStatus.EXPLICIT,
        )
        self.assertEqual(
            result.evidence_status,
            EvidenceStatus.UNKNOWN,
        )


if __name__ == "__main__":
    unittest.main()

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LinguisticFeature:
    feature_type: str
    observed_text: str
    normalized_text: str
    source_id: str
    context: str
    status: str = "EXPLICIT"


@dataclass(frozen=True)
class LinguisticAnalysis:
    source_id: str
    features: Tuple[LinguisticFeature, ...]
    candidate_anomalies: Tuple[str, ...]
    decoding_status: str = "NOT_ESTABLISHED"
