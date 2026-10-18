from dataclasses import dataclass,asdict
from datetime import datetime,timezone
from .models import canonical_digest
@dataclass(frozen=True)
class EvidenceRecord:
    event_id:str; timestamp:str; source:str; event_type:str; policy_id:str; decision:str; affected_resource:str; previous_state:str; new_state:str; evidence_digest:str; operator_action:str|None; recovery_action:str|None; ceremonial_message:str
class EvidenceEngine:
    def __init__(self): self.records=[]
    def record(self,**kwargs):
        base=dict(kwargs); base['timestamp']=datetime.now(timezone.utc).isoformat(); base['evidence_digest']=canonical_digest(base)
        rec=EvidenceRecord(**base); self.records.append(rec); return rec
