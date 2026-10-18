from .models import Decision, PolicyRule, ThreatEvent
class PolicyEngine:
    def __init__(self, rules): self.rules=sorted(rules,key=lambda r:r.priority)
    @classmethod
    def default(cls):
        return cls([PolicyRule('P-SYSTEM-HACK-NET',Decision.QUARANTINE,event_type='system_hack',source='network',priority=10),PolicyRule('P-HIGH-SEVERITY',Decision.BLOCK,min_severity=.7,priority=20),PolicyRule('P-SCAN',Decision.ALLOW,event_type='scan',priority=30)])
    def evaluate(self,event):
        for r in self.rules:
            if r.event_type is not None and r.event_type!=event.type: continue
            if r.source is not None and r.source!=event.source: continue
            if r.min_severity is not None and event.severity<=r.min_severity: continue
            return r.decision,r.policy_id
        return Decision.ESCALATE,'P-DEFAULT-ESCALATE'
