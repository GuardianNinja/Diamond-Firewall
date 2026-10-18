# Diamond Firewall Specification v0.1

## Decisions
ALLOW, BLOCK, QUARANTINE, ESCALATE. `HARDEN` is a defensive action, not a permission decision.

## Core states
NORMAL -> OUTER_COLLAPSED -> INNER_HARDENING -> REGEN_OUTER -> NORMAL.

## Evidence
Every forwarded threat event yields one EvidenceRecord. Quarantine creates containment state and is represented by the same authoritative decision evidence. Operator actions yield separate records.

## Modes
Silent: baseline attack resistance, reduced autonomous hardening.
Guardian: balanced defaults.
Ceremony: moderated resistance with elevated hardening.
Master: strongest modifiers; destructive/full-hardening operations require explicit two-factor authorization represented by MDF-bead verification plus recovery verification. Raw recovery secrets are never stored.

## Integration contract
External systems may submit normalized ThreatEvents and operator commands and consume decisions/evidence/callbacks. No external integration may directly mutate PolicyEngine, IsolationEngine, DiamondCore, or EvidenceEngine state. A future adapter should expose versioned JSON/HTTP or local IPC boundaries without importing external runtime internals.

## Ceremonial vocabulary
- `Boundary Observed` — normal observation/allow path.
- `Threat Blocked` — policy denied execution.
- `Threat Contained` — policy quarantine enforced.
- `Operator Review Required` — policy escalation pending human action.
- `Outer Boundary Collapsed` — outer layer crossed threshold.
- `Inner Core Hardened` — inner layer completed a hardening pass.
- `Diamond Resilience Increased` — manual or autonomous hardening increased defensive state.
