from semantics import SemanticFact, SemanticStatus


from dataclasses import dataclass
from enum import Enum
from typing import Iterable


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

