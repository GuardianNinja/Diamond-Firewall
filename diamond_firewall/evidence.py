from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib

from .models import canonical_digest


@dataclass(frozen=True)
class EvidenceRecord:
    event_id: str
    timestamp: str
    source: str
    event_type: str
    policy_id: str
    decision: str
    affected_resource: str
    previous_state: str
    new_state: str
    evidence_digest: str
    operator_action: str | None = None
    related_resource: str | None = None
    previous_hash: str | None = None
    chain_hash: str | None = None
    sequence_number: int = 0
    record_hash: str = ""


class EvidenceEngine:
    GENESIS_HASH = "diamond-firewall-genesis-v0.2"

    def __init__(self):
        self.records = []
        self._last_hash = self.GENESIS_HASH
        self._sequence = 0

    def _compute_chain_hash(self, previous_hash: str, record_hash: str, sequence_number: int) -> str:
        content = f"{previous_hash}:{record_hash}:{sequence_number}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _compute_record_hash(self, payload: dict) -> str:
        return canonical_digest(payload)

    def _base_record(self, **kwargs):
        payload = dict(kwargs)

        required_fields = [
            "event_id",
            "source",
            "event_type",
            "policy_id",
            "decision",
            "affected_resource",
        ]
        for field in required_fields:
            if field not in payload or payload[field] in (None, ""):
                raise ValueError(f"{field} is required")

        self._sequence += 1
        payload["timestamp"] = datetime.now(timezone.utc).isoformat()
        payload["sequence_number"] = self._sequence
        payload["previous_hash"] = self._last_hash

        # record_hash is bound to authoritative record content before chain hash is added.
        payload["record_hash"] = self._compute_record_hash(payload)

        # chain_hash binds the current event to the prior event in the sequence.
        payload["chain_hash"] = self._compute_chain_hash(
            payload["previous_hash"],
            payload["record_hash"],
            self._sequence,
        )

        # Preserve the historical field name for compatibility with earlier usage.
        payload["evidence_digest"] = payload["record_hash"]

        return payload

    def record(self, **kwargs):
        payload = self._base_record(**kwargs)
        rec = EvidenceRecord(**payload)
        self.records.append(rec)
        self._last_hash = rec.chain_hash
        return rec

    def append(self, **kwargs):
        return self.record(**kwargs)

    def verify_record(self, record: EvidenceRecord, expected_previous_hash: str | None = None) -> bool:
        if record.sequence_number <= 0:
            raise ValueError("sequence_number must be positive")

        expected_previous = expected_previous_hash if expected_previous_hash is not None else self.GENESIS_HASH
        if record.previous_hash != expected_previous:
            raise ValueError(
                f"previous_hash mismatch: expected {expected_previous}, got {record.previous_hash}"
            )

        record_payload = asdict(record)

        # Remove fields that are derived from the underlying record content.
        for key in ("previous_hash", "chain_hash", "record_hash", "evidence_digest"):
            record_payload.pop(key, None)

        computed_record_hash = self._compute_record_hash(record_payload)
        if record.record_hash != computed_record_hash:
            raise ValueError("record_hash mismatch")

        expected_chain_hash = self._compute_chain_hash(
            record.previous_hash,
            record.record_hash,
            record.sequence_number,
        )
        if record.chain_hash != expected_chain_hash:
            raise ValueError("chain_hash mismatch")

        return True

    def verify_chain(self) -> bool:
        previous_hash = self.GENESIS_HASH

        for index, record in enumerate(self.records, start=1):
            if record.sequence_number != index:
                raise ValueError(
                    f"sequence_number mismatch at index {index}: expected {index}, got {record.sequence_number}"
                )
            self.verify_record(record, previous_hash)
            previous_hash = record.chain_hash

        return True