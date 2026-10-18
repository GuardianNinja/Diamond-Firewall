Diamond Firewall — Installation and Validation

Status: Reference implementation / development scaffold
Document version: 0.1
Last updated: October 18, 2026

1. Scope and Safety Notice

These instructions install and test the current Python reference implementation.

The current scaffold does not establish that Diamond Firewall can enforce operating-system firewall rules, isolate real host processes or network resources, provide production-grade cryptographic key management, or operate as a certified security product.

Use a disposable development environment. Do not rely on this scaffold to protect production systems or sensitive assets.

2. Prerequisites

* Git
* Python 3.11 or later recommended; the complete supported version range has not yet been established
* pip, included with most standard Python installations

The current test suite uses pytest. A formal dependency manifest and fully reproducible dependency specification have not yet been established.

3. Obtain the Source

Open a terminal and run:

git clone https://github.com/GuardianNinja/Diamond-Firewall.git
cd Diamond-Firewall

Record the exact revision being tested:

git rev-parse HEAD

Retain this commit hash with your test results. Results from one revision should not automatically be attributed to another.

4. Create an Isolated Python Environment

macOS or Linux

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest

Windows PowerShell

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pytest

If PowerShell blocks environment activation, follow your organization’s approved Python environment procedure. Do not weaken system-wide execution policy solely to run this project.

5. Run the Test Suite

From the repository root, run:

python -m pytest -q

The repository currently contains tests covering:

* Policy decision boundaries.
* Quarantine behavior.
* Master-mode authorization gating.
* Evidence generation for forwarded events.
* Simulation harness execution across selected durations and modes.

Record the command, Python version, operating system, commit hash, exit code, and complete output.

A passing test suite verifies only the behavior covered by those tests. It does not constitute a security audit, penetration test, production certification, or proof of resistance to real-world attacks.

6. Run a Harness Example

The current harness exposes a Python API. From the repository root, with the virtual environment active, try:

python - <<'PY'
from diamond_firewall.harness import run_test
from diamond_firewall.models import FirewallMode
result = run_test(48, FirewallMode.GUARDIAN, "spike")
print(result)
PY

This example is based on the current reference API and must be verified against the exact checkout before release.

The harness duration is a simulation parameter. It must not be described as a real-world 48-hour, 72-hour, or 360-hour endurance test unless an actual test ran for that elapsed duration under a documented test plan.

7. Current Implementation Limitations

The current scaffold must not be represented as a production security control.

Production work requires design, implementation, and verification of at least:

* Authenticated operator identity and role enforcement.
* Platform-specific host and network enforcement adapters.
* Real isolation and verified recovery or release procedures.
* Cryptographic key generation, storage, rotation, and recovery.
* Durable, tamper-evident evidence storage and integrity verification.
* Secure configuration, secrets handling, and update mechanisms.
* Dependency pinning and reproducible builds.
* Threat modeling, abuse-case testing, and independent security review.
* Documented rollback, incident response, and recovery procedures.

The HARDEN core action must remain distinct from policy decisions such as ALLOW, BLOCK, QUARANTINE, and ESCALATE.

No subsystem may silently redefine another subsystem’s authority.

8. Troubleshooting

Error: No module named pytest

Activate the virtual environment and run:

python -m pip install pytest

Error: No module named diamond_firewall

Run commands from the repository root and confirm the diamond_firewall/ directory exists.

Test results differ from a prior report

Record the commit hash and complete test output. Do not assume that results from another archive or commit apply to your checkout.

Python or platform errors

Capture the Python version, pip version, operating system and version, exact command, and traceback before diagnosing the issue.

9. Before Production Use

Do not use the reference scaffold as a production firewall or claim regulatory compliance based solely on its existing tests.

Production readiness requires a defined operational scope, reviewed threat model, implemented platform integrations, measurable acceptance criteria, independent testing, and evidence tied to a specific release.

10. License Status

The proposed custom source-available license remains a draft pending legal review and confirmation of the copyright holder.

Until a final license is approved and published, do not assume this draft establishes finalized permissions for use, modification, redistribution, or commercial deployment.