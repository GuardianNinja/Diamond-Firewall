from dataclasses import dataclass
from .application import DiamondFirewall
from .monitor import SyntheticThreatMonitor
from .models import FirewallMode
@dataclass
class HarnessResult:
    duration:int; mode:str; profile:str; outer_collapses:int; inner_hardening_passes:int; entropy_injected:float; resilience:float; resilience_over_time:list; policy_decisions:dict; threat_intensity:float; evidence_count:int

def run_test(duration,mode,profile='baseline'):
    app=DiamondFirewall(mode); mon=SyntheticThreatMonitor(profile,seed=11); counts={k:0 for k in ['ALLOW','BLOCK','QUARANTINE','ESCALATE']}; total=0; curve=[]
    for minute in range(1,duration+1):
        ev=next(mon.events()); total+=ev.severity; d=app.ingest(ev); 
        if d: counts[d.value]+=1
        if minute%60==0 and mode!=FirewallMode.SILENT: app.tap_to_harden('harness')
        curve.append(app.core.resilience)
    c=app.core
    return HarnessResult(duration,mode.value,profile,c.outer_collapses,c.inner_hardening_passes,c.entropy_injected,c.resilience,curve,counts,total/duration,len(app.evidence.records))

def run_matrix():
    return [run_test(d,m,'spike') for d in (48,72,360) for m in (FirewallMode.SILENT,FirewallMode.GUARDIAN,FirewallMode.MASTER)]
