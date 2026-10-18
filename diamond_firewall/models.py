from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any
import hashlib, json

class Decision(str, Enum):
    ALLOW='ALLOW'; BLOCK='BLOCK'; QUARANTINE='QUARANTINE'; ESCALATE='ESCALATE'
class CoreAction(str, Enum):
    NONE='NONE'; HARDEN='HARDEN'; REGENERATE='REGENERATE'
class FirewallMode(str, Enum):
    SILENT='SILENT'; GUARDIAN='GUARDIAN'; CEREMONY='CEREMONY'; MASTER='MASTER'
class CoreState(str, Enum):
    NORMAL='NORMAL'; OUTER_COLLAPSED='OUTER_COLLAPSED'; INNER_HARDENING='INNER_HARDENING'; REGEN_OUTER='REGEN_OUTER'
class ThreatType(str, Enum):
    SCAN='scan'; BURST='burst'; DRIFT='drift'; SYSTEM_HACK='system_hack'

@dataclass(frozen=True)
class ThreatEvent:
    event_id: str; type: str; source: str; severity: float; metadata: dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True)
class PolicyRule:
    policy_id: str; decision: Decision; event_type: str|None=None; source: str|None=None; min_severity: float|None=None; priority: int=100

@dataclass
class LayerState:
    strength: float; entropy: float; collapse_threshold: float

@dataclass(frozen=True)
class CoreSnapshot:
    state: CoreState; outer_strength: float; outer_entropy: float; inner_strength: float; inner_entropy: float; resilience: float

@dataclass(frozen=True)
class CoreResult:
    policy_decision: Decision; core_action: CoreAction; snapshot: CoreSnapshot; ceremonial: tuple[str,...]

def canonical_digest(value: Any) -> str:
    raw=json.dumps(value, sort_keys=True, separators=(',',':'), default=lambda o: o.value if isinstance(o,Enum) else asdict(o)).encode()
    return hashlib.sha256(raw).hexdigest()
