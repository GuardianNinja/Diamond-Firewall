from diamond_firewall.application import DiamondFirewall
from diamond_firewall.models import *
from diamond_firewall.core import MasterAuthorization,MasterAuthorizationError
from diamond_firewall.harness import run_test

def test_policy_boundaries():
    f=DiamondFirewall()
    assert f.ingest(ThreatEvent('1','scan','network',.1))==Decision.ALLOW
    assert f.ingest(ThreatEvent('2','burst','network',.9))==Decision.BLOCK
    assert f.ingest(ThreatEvent('3','system_hack','network',.5))==Decision.QUARANTINE

def test_quarantine_stops_forwarding():
    f=DiamondFirewall(); f.ingest(ThreatEvent('1','system_hack','network',.5)); assert f.ingest(ThreatEvent('2','scan','network',.1)) is None

def test_master_gate():
    f=DiamondFirewall(FirewallMode.MASTER)
    try: f.core.full_hardening(MasterAuthorization('x',False,True)); assert False
    except MasterAuthorizationError: pass
    f.core.full_hardening(MasterAuthorization('x',True,True))

def test_evidence_for_forwarded_events():
    f=DiamondFirewall(); f.ingest(ThreatEvent('1','scan','network',.1)); f.ingest(ThreatEvent('2','burst','other',.2)); assert len(f.evidence.records)==2

def test_harness_matrix_runs():
    for d in (48,72,360):
        for m in (FirewallMode.SILENT,FirewallMode.GUARDIAN,FirewallMode.MASTER):
            r=run_test(d,m,'spike'); assert r.duration==d and len(r.resilience_over_time)==d and r.evidence_count>=1
