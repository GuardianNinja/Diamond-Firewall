from dataclasses import dataclass
from datetime import datetime, timezone
class IsolationError(Exception): pass
@dataclass
class QuarantineRecord:
    resource: str; event_id: str; created_at: str; released_at: str|None=None; released_by: str|None=None
class IsolationEngine:
    def __init__(self): self.records={}
    def quarantine(self, resource,event_id):
        rec=QuarantineRecord(resource,event_id,datetime.now(timezone.utc).isoformat()); self.records[resource]=rec; return rec
    def is_quarantined(self,resource): return resource in self.records and self.records[resource].released_at is None
    def should_forward(self,source): return not self.is_quarantined(source)
    def release(self,resource,operator_id):
        if not self.is_quarantined(resource): raise IsolationError('resource not quarantined')
        self.records[resource].released_at=datetime.now(timezone.utc).isoformat(); self.records[resource].released_by=operator_id; return self.records[resource]
