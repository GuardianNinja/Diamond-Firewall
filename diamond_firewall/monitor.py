from abc import ABC, abstractmethod
import random
from .models import ThreatEvent

class ThreatMonitor(ABC):
    @abstractmethod
    def events(self): ...

class SyntheticThreatMonitor(ThreatMonitor):
    def __init__(self, profile='baseline', seed=7): self.profile=profile; self.rng=random.Random(seed); self.minute=0
    def events(self):
        self.minute += 1
        if self.profile=='low_noise': intensity=self.rng.uniform(.05,.2)
        elif self.profile=='spike': intensity=.8 if self.minute%30==0 else self.rng.uniform(.1,.3)
        elif self.profile=='stealth': intensity=self.rng.uniform(.05,.4)
        else: intensity=self.rng.uniform(.1,.5)
        kind=self.rng.choice(['scan','burst','drift','system_hack'])
        yield ThreatEvent(f'syn-{self.minute}',kind,'network',round(intensity,4),{'profile':self.profile,'minute':self.minute})

class ReplayThreatMonitor(ThreatMonitor):
    def __init__(self, events): self._events=list(events)
    def events(self): yield from self._events
