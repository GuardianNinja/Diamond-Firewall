from .models import *
from .policy import PolicyEngine
from .isolation import IsolationEngine
from .core import DiamondCore
from .evidence import EvidenceEngine
class DiamondFirewall:
    def __init__(self,mode=FirewallMode.GUARDIAN,rules=None):
        self.core=DiamondCore(mode); self.policy=PolicyEngine(rules or PolicyEngine.default().rules); self.isolation=IsolationEngine(); self.evidence=EvidenceEngine()
    def ingest(self,event):
        if not self.isolation.should_forward(event.source):
            return None
        decision,policy_id=self.policy.evaluate(event); before=self.core.state.value
        if decision==Decision.QUARANTINE: self.isolation.quarantine(event.source,event.event_id)
        result=self.core.process(event,decision); after=result.snapshot.state.value
        phrase={'ALLOW':'Boundary Observed','BLOCK':'Threat Blocked','QUARANTINE':'Threat Contained','ESCALATE':'Operator Review Required'}[decision]
        self.evidence.record(event_id=event.event_id,source=event.source,event_type=event.type,policy_id=policy_id,decision=decision.value,affected_resource=event.source,previous_state=before,new_state=after,operator_action=None,recovery_action='regrow_outer' if before!=after else None,ceremonial_message=phrase)
        return decision
    def tap_to_harden(self,operator_id):
        before=self.core.state.value; self.core.tap_to_harden(); self.evidence.record(event_id=f'op-{len(self.evidence.records)+1}',source='operator',event_type='manual_harden',policy_id='OPERATOR',decision='HARDEN',affected_resource='diamond-core',previous_state=before,new_state=self.core.state.value,operator_action=operator_id,recovery_action=None,ceremonial_message='Diamond Resilience Increased')
