from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable
from uuid import uuid4


class EvidencePolarity(str, Enum):
    SUPPORTS = "supports"
    REFUTES = "refutes"


class EvidenceValidation(str, Enum):
    UNASSESSED = "unassessed"
    ADMISSIBLE = "admissible"
    REJECTED = "rejected"


class EvidenceStatus(str, Enum):
    SUPPORTED = "supported"
    REFUTED = "refuted"
    CONFLICT = "conflict"
    UNKNOWN = "unknown"


@dataclass
class EvidenceItem:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    source_ref: str = ""  # URL, citation, document ID, etc.
    polarity: EvidencePolarity = EvidencePolarity.SUPPORTS
    validation: EvidenceValidation = EvidenceValidation.UNASSESSED
    rationale: str = ""
    reviewer: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_at: datetime | None = None

    def review(
        self,
        validation: EvidenceValidation,
        rationale: str = "",
        reviewer: str = "",
    ) -> None:
        if validation == EvidenceValidation.UNASSESSED:
            self.validation = validation
            self.rationale = rationale
            self.reviewer = reviewer
            self.reviewed_at = None
            return

        self.validation = validation
        self.rationale = rationale
        self.reviewer = reviewer
        self.reviewed_at = datetime.now(timezone.utc)


@dataclass
class Claim:
    id: str = field(default_factory=lambda: str(uuid4()))
    statement: str = ""
    evidence: list[EvidenceItem] = field(default_factory=list)

    @property
    def admissible_evidence(self) -> list[EvidenceItem]:
        return [
            item for item in self.evidence
            if item.validation == EvidenceValidation.ADMISSIBLE
        ]

    @property
    def unassessed_count(self) -> int:
        return sum(
            1 for item in self.evidence
            if item.validation == EvidenceValidation.UNASSESSED
        )

    @property
    def status(self) -> EvidenceStatus:
        return evaluate_claim_status(self.evidence)


def evaluate_claim_status(evidence_items: Iterable[EvidenceItem]) -> EvidenceStatus:
    admissible = [
        item for item in evidence_items
        if item.validation == EvidenceValidation.ADMISSIBLE
    ]

    has_support = any(item.polarity == EvidencePolarity.SUPPORTS for item in admissible)
    has_refute = any(item.polarity == EvidencePolarity.REFUTES for item in admissible)

    if has_support and has_refute:
        return EvidenceStatus.CONFLICT
    if has_support:
        return EvidenceStatus.SUPPORTED
    if has_refute:
        return EvidenceStatus.REFUTED
    return EvidenceStatus.UNKNOWN
