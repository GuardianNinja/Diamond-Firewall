# Diamond Firewall Reference Architecture v0.1

Standalone governed defensive application. It has no dependency on SLOS, JarvondisU, LeafLink, or any other runtime.

## Authority diamond
1. Human Authority: supplies policy, operator commands, approvals, credentials.
2. Observe/Policy: Threat Monitor observes; Policy Engine decides permission.
3. Isolate/Execute: Isolation Engine enforces quarantine; Diamond Core performs defensive state changes.
4. Evidence: Evidence Engine records every authoritative transition and operator action.

No subsystem silently redefines another. Policy owns permission. Isolation owns containment. Core owns defensive state. Evidence owns audit records.

## Critical separation
The Core never converts BLOCK/QUARANTINE/ESCALATE into ALLOW. `CoreResult.policy_decision` is the Policy Engine decision and `core_action` is a separate defensive action.

## Production boundary
The reference implementation models protection states; it does not claim to implement kernel/network firewalling or real cryptographic key rotation. Production adapters must bind these abstractions to OS/network enforcement, secure key storage, privilege separation, fail-closed behavior, and tamper-evident storage.
