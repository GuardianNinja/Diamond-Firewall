# FILE: tests/test_evidence_chain.py
from diamond_firewall.application import DiamondFirewall
from diamond_firewall.evidence import EvidenceRecord
from diamond_firewall.models import ThreatEvent


def test_evidence_chain_links_each_record():
    firewall = DiamondFirewall()
    firewall.ingest(ThreatEvent("1", "scan", "network", 0.1))
    firewall.ingest(ThreatEvent("2", "burst", "network", 0.9))

    assert len(firewall.evidence.records) == 2
    assert firewall.evidence.records[0].sequence_number == 1
    assert firewall.evidence.records[1].previous_hash == firewall.evidence.records[0].chain_hash
    assert firewall.evidence.verify_chain() is True


def test_evidence_chain_detects_tampering():
    firewall = DiamondFirewall()
    firewall.ingest(ThreatEvent("1", "scan", "network", 0.1))
    firewall.ingest(ThreatEvent("2", "burst", "network", 0.9))

    tampered = EvidenceRecord(
        event_id="tampered-event",
        timestamp="2026-01-01T00:00:00+00:00",
        source="network",
        event_type="burst",
        policy_id="P-TEST",
        decision="ALLOW",
        affected_resource="network",
        previous_state="NORMAL",
        new_state="NORMAL",
        evidence_digest="tampered",
        operator_action=None,
        related_resource=None,
        previous_hash=firewall.evidence.records[0].chain_hash,
        chain_hash="0" * 64,
        sequence_number=2,
        record_hash="not-a-real-record-hash",
    )

    try:
        firewall.evidence.verify_record(tampered, firewall.evidence.records[0].chain_hash)
        assert False, "Expected chain verification to reject a tampered record"
    except ValueError:
        pass