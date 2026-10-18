from dataclasses import dataclass
from .models import *

class MasterAuthorizationError(Exception): pass
@dataclass(frozen=True)
class MasterAuthorization:
    operator_id: str; bead_verified: bool; recovery_verified: bool
    @property
    def valid(self): return bool(self.operator_id and self.bead_verified and self.recovery_verified)

class DiamondCore:
    ATTACK={'SILENT':1.0,'GUARDIAN':.8,'CEREMONY':.9,'MASTER':.6}
    HARDEN={'SILENT':.9,'GUARDIAN':1.0,'CEREMONY':1.05,'MASTER':1.2}
    def __init__(self,mode=FirewallMode.GUARDIAN):
        self.mode=mode; self.state=CoreState.NORMAL
        self.outer=LayerState(1.0,1.0,.3); self.inner=LayerState(1.5,1.2,.1)
        self.outer_collapses=0; self.inner_hardening_passes=0; self.entropy_injected=0.0
    @property
    def resilience(self): return .5*self.outer.strength+.7*self.inner.strength+.3*self.outer.entropy+.4*self.inner.entropy
    def snapshot(self): return CoreSnapshot(self.state,self.outer.strength,self.outer.entropy,self.inner.strength,self.inner.entropy,self.resilience)
    def process(self,event,decision):
        if decision in (Decision.BLOCK,Decision.QUARANTINE,Decision.ESCALATE) or event.severity>=.7: self._absorb(event.severity)
        else: self._autonomous_hardening()
        return CoreResult(decision,CoreAction.HARDEN if event.severity<.7 else CoreAction.REGENERATE,self.snapshot(),tuple())
    def _absorb(self,intensity):
        eff=intensity*self.ATTACK[self.mode.value]; self.outer.strength-=eff*.2; self.outer.entropy=max(0,self.outer.entropy-eff*.05)
        if self.outer.strength<self.outer.collapse_threshold: self._collapse()
    def _collapse(self):
        self.state=CoreState.OUTER_COLLAPSED; self.outer_collapses+=1
        self.state=CoreState.INNER_HARDENING; self._inner_harden(); self.state=CoreState.REGEN_OUTER
        self.outer.strength=self.inner.strength*.8; self.outer.entropy=self.inner.entropy*.7; self.state=CoreState.NORMAL
    def _inner_harden(self):
        f=.15*self.HARDEN[self.mode.value]; self.inner.strength*=1+f; self.inner.entropy*=1+f*.5; self.inner_hardening_passes+=1; self.entropy_injected+=.02
    def _autonomous_hardening(self):
        f=.01*self.HARDEN[self.mode.value]; self.outer.strength*=1+f; self.inner.strength*=1+f*.8; self.outer.entropy+=.01; self.inner.entropy+=.02; self.entropy_injected+=.03
    def tap_to_harden(self):
        f=.03*self.HARDEN[self.mode.value]; self.outer.strength*=1+f; self.inner.strength*=1+f*.7; self.outer.entropy+=.05; self.inner.entropy+=.05; self.entropy_injected+=.1
    def full_hardening(self,auth:MasterAuthorization):
        if self.mode!=FirewallMode.MASTER or not auth.valid: raise MasterAuthorizationError('valid Master authorization required')
        self._inner_harden(); self.tap_to_harden()
