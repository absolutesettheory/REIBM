
"""
Module: cryptography.py

Project: Relational Evidence and Information Boundary Model (REIBM)
Author: Christopher Thomas Ronio

Purpose:
    Provide deterministic cryptographic content commitments,
    SHA-256 hashing, file integrity verification, and
    reproducible record fingerprints.

Security boundary:
    A matching hash establishes content integrity relative to
    a previously trusted digest. It does not establish the
    truth, authenticity, or authorship of the original content.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Mapping
import hashlib
import hmac
import json
import math


# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------

HASH_ALGORITHM = "sha256"
SCHEMA_VERSION = "1.0"


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

def _validate_json_value(value: Any, path: str = "record") -> Any:
    """
    Validate and normalize values for deterministic JSON.

    Accepted:
        None, bool, int, finite float, str, list, dict.

    Dictionary keys must be strings.
    """

    if value is None or isinstance(value, (bool, int, str)):
        return value

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(
                f"Non-finite float at {path}"
            )
        return value

    if isinstance(value, Mapping):
        normalized = {}

        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(
                    f"Non-string dictionary key at {path}"
                )

            normalized[key] = _validate_json_value(
                item,
                f"{path}.{key}",
            )

        return normalized

    if isinstance(value, list):
        return [
            _validate_json_value(item, f"{path}[{index}]")
            for index, item in enumerate(value)
        ]

    raise TypeError(
        f"Unsupported JSON value at {path}: "
        f"{type(value).__name__}"
    )


# ---------------------------------------------------------
# CANONICAL SERIALIZATION
# ---------------------------------------------------------

def canonicalize_record(
    record: Mapping[str, Any],
) -> bytes:
    """
    Convert a record into deterministic UTF-8 JSON bytes.

    Sorting keys and removing unnecessary whitespace ensures
    equivalent supported records produce identical bytes.
    """

    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")

    normalized = _validate_json_value(record)

    serialized = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )

    return serialized.encode("utf-8")


# ---------------------------------------------------------
# CONTENT HASHING
# ---------------------------------------------------------

def hash_bytes(data: bytes) -> str:
    """Return the SHA-256 digest of bytes."""

    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    return hashlib.sha256(data).hexdigest()


def hash_record(
    record: Mapping[str, Any],
) -> str:
    """Return a SHA-256 fingerprint of a structured record."""

    canonical_data = canonicalize_record(record)
    return hash_bytes(canonical_data)


def hash_file(
    file_path: str | Path,
    chunk_size: int = 65536,
) -> str:
    """
    Calculate the SHA-256 digest of a file.

    Reads incrementally rather than loading the entire file
    into memory.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    digest = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


# ---------------------------------------------------------
# INTEGRITY VERIFICATION
# ---------------------------------------------------------

def verify_digest(
    data: bytes,
    expected_digest: str,
) -> bool:
    """
    Compare content against a previously recorded SHA-256 digest.

    Returns False for malformed digest values.
    """

    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    if not isinstance(expected_digest, str):
        return False

    if len(expected_digest) != 64:
        return False

    try:
        bytes.fromhex(expected_digest)
    except ValueError:
        return False

    actual_digest = hash_bytes(data)

    return hmac.compare_digest(
        actual_digest,
        expected_digest.lower(),
    )


def verify_record_hash(
    record: Mapping[str, Any],
    expected_digest: str,
) -> bool:
    """Verify the integrity of a structured record."""

    canonical_data = canonicalize_record(record)

    return verify_digest(
        canonical_data,
        expected_digest,
    )


def verify_file_hash(
    file_path: str | Path,
    expected_digest: str,
) -> bool:
    """Verify a file against a previously recorded digest."""

    if not isinstance(expected_digest, str):
        return False

    if len(expected_digest) != 64:
        return False

    try:
        bytes.fromhex(expected_digest)
    except ValueError:
        return False

    actual_digest = hash_file(file_path)

    return hmac.compare_digest(
        actual_digest,
        expected_digest.lower(),
    )


# ---------------------------------------------------------
# CONTENT COMMITMENTS
# ---------------------------------------------------------

@dataclass(frozen=True)
class ContentCommitment:
    """
    Cryptographic commitment to a particular record version.

    The commitment binds the record content to its identifying
    metadata. It does not independently authenticate that metadata.
    """

    record_id: str
    source_id: str | None
    algorithm: str
    digest: str
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def create_content_commitment(
    record_id: str,
    record: Mapping[str, Any],
    source_id: str | None = None,
) -> ContentCommitment:
    """
    Create a SHA-256 commitment for a structured record.

    The record identifier and source identifier are included
    in the committed payload.
    """

    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record_id must be non-empty")

    if source_id is not None:
        if not isinstance(source_id, str) or not source_id.strip():
            raise ValueError("source_id must be non-empty or None")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "record_id": record_id,
        "source_id": source_id,
        "record": record,
    }

    digest = hash_record(payload)

    return ContentCommitment(
        record_id=record_id,
        source_id=source_id,
        algorithm=HASH_ALGORITHM,
        digest=digest,
    )


def verify_content_commitment(
    commitment: ContentCommitment,
    record: Mapping[str, Any],
) -> bool:
    """
    Verify that a record matches its content commitment.
    """

    if not isinstance(commitment, ContentCommitment):
        raise TypeError(
            "commitment must be a ContentCommitment"
        )

    if commitment.algorithm != HASH_ALGORITHM:
        return False

    payload = {
        "schema_version": commitment.schema_version,
        "record_id": commitment.record_id,
        "source_id": commitment.source_id,
        "record": record,
    }

    actual_digest = hash_record(payload)

    return hmac.compare_digest(
        actual_digest,
        commitment.digest,
    )


# ---------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------

__all__ = [
    "HASH_ALGORITHM",
    "SCHEMA_VERSION",
    "ContentCommitment",
    "canonicalize_record",
    "hash_bytes",
    "hash_record",
    "hash_file",
    "verify_digest",
    "verify_record_hash",
    "verify_file_hash",
    "create_content_commitment",
    "verify_content_commitment",
]
