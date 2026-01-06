# devsecops-ci-pipeline-demo

Demonstrates how to build a **secure CI/CD pipeline** by integrating security checks into developer workflows — making security an **enabler**, not a blocker.

> CI platform: **GitHub Actions** (automatically runs on every push and pull request)

[![CI - Security Checks](https://github.com/0xmarziehlabs/devsecops-ci-pipeline-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/0xmarziehlabs/devsecops-ci-pipeline-demo/actions)


---

## Table of Contents
- [What This Is](#what-this-is)
- [Current Status](#current-status)
- [Roadmap (Next Steps)](#roadmap-next-steps)
- [How It Works](#how-it-works-so-far)
- [Fail → Fix → Pass (Semgrep demo)](#fail--fix--pass-semgrep-demo)
- [Fail → Fix → Pass (TruffleHog demo)](#fail--fix--pass-trufflehog-demo)
- [Fail → Fix → Pass (pre-commit demo)](#fail--fix--pass-pre-commit-demo)
- [Local Usage](#local-usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Why This Project?](#why-this-project)
- [Branch Protection](#branch-protection)
- [License](#license)

---

## What This Is
A minimal repository that showcases:
- **SAST** with **Semgrep** (pattern-based, fast)
- **Deep SAST** with **CodeQL** (semantic & data-flow analysis)
- **SCA** with **pip-audit** (Python dependency vulnerabilities)
- **Policy-as-code guardrails** via **Local + CI enforced pre-commit hooks**
- **Secret Scanning** with **TruffleHog** (filesystem + git history)
- **Key Management** best practices via GitHub Actions secrets
- Clean **PR workflow** with **Branch Protection**
- Clear **Fail → Fix → Pass** security demonstrations (shift-left security)


---

## Current Status
- [x] Project structure initialized (`src`, `tests`, `workflows`)
- [x] Demo Python app with basic tests

- [x] **Semgrep (SAST)** integrated and demonstrated (pattern-based)
- [x] **CodeQL (deep SAST)** integrated with SARIF upload → GitHub Code Scanning
- [x] **pip-audit (SCA)** integrated for Python dependencies

- [x] **TruffleHog (secret scanning)** integrated (filesystem + git history)
- [x] Keys handled securely (GitHub Actions secrets, excluded from repo)
- [x] Scheduled TruffleHog scan on `main` (weekly, verified-only)

- [x] **Pre-commit hooks enforced locally and in CI** (policy-as-code guardrails)

- [ ] Docs polish (badges, PR/Issue templates)
- [ ] First release: `v0.1`

---

## Roadmap (Enterprise-Oriented)

### Phase 1 — Stabilization & Release Readiness
Focus: baseline quality, trust, and reproducibility.

- Finalize documentation structure (README polish, clear sectioning, consistent terminology)
- Add CI badges (Security, Code Scanning, Dependency Health)
- Introduce PR and Issue templates (security-focused, reproducible reports)
- Tag and publish first stable release (`v0.1`)
- Validate branch protection rules against real PR workflows

---

### Phase 2 — Security Hardening (Pipeline & Runtime)
Focus: reducing blast radius and enforcing least privilege.

- Harden GitHub Actions workflows:
  - Explicit permissions (`permissions:` minimal scopes)
  - Remove implicit default tokens where possible
- Secrets lifecycle hardening:
  - Clear separation of build-time vs runtime secrets
  - Secret rotation & revocation workflow documentation
- Artifact hygiene:
  - Ensure sensitive files are shredded after use
  - Prevent artifact persistence of secrets or credentials
- Document security assumptions and threat boundaries

---

### Phase 3 — Supply Chain & Integrity Controls
Focus: protecting dependencies, artifacts, and build trust.

- Expand SCA coverage:
  - Dependency pinning and hash verification
  - Policy-based vulnerability thresholds
- Introduce artifact integrity checks:
  - Provenance metadata generation
  - Reproducible build considerations
- Add basic supply-chain threat scenarios and mitigations

---

### Phase 4 — Security Observability & Governance
Focus: visibility, accountability, and long-term maintainability.

- Improve security signal visibility:
  - Centralized view of SAST, SCA, and secret findings
  - Clear ownership and triage guidance
- Document security decision rationale:
  - Why specific tools, thresholds, and policies exist
- Add contribution security guidelines:
  - Secure contribution rules for external collaborators
  - Clear expectations for PR security checks

---

### Phase 5 — Scalability & Real-World Adaptation
Focus: demonstrating applicability beyond a demo repository.

- Provide guidance for adapting the pipeline to:
  - Multi-service repositories
  - Larger teams with multiple contributors
- Document trade-offs between security strictness and developer velocity
- Outline extension points for additional tooling (DAST, IaC scanning, container scanning)

---

> This roadmap reflects how a DevSecOps pipeline evolves in real-world engineering organizations:
> starting with guardrails, progressing through hardening and governance, and scaling with clarity rather than complexity.


---

## How It Works

This repository demonstrates how security controls can be embedded directly into the development lifecycle using layered, enforceable guardrails — without disrupting developer velocity.

The pipeline is designed around **early detection, clear ownership, and automated enforcement**, following a practical DevSecOps model.

---

### Static Application Security Testing (SAST)

- **Semgrep** is used for fast, pattern-based static analysis.
- Custom rules detect unsafe coding patterns (e.g., `eval`, insecure constructs).
- Runs on every pull request and push.
- Acts as an early, developer-facing guardrail by blocking known anti-patterns before merge.

This layer provides **fast feedback** and catches obvious security issues early.

---

### Deep Static Analysis (CodeQL)

- **CodeQL** performs semantic, data-flow–aware analysis.
- Detects complex vulnerabilities such as injection flaws (SQLi, XSS, RCE, SSRF).
- Runs on:
  - Pull requests
  - Pushes to `main`
  - Weekly scheduled scans
- Findings are uploaded in **SARIF format** and surfaced via GitHub Code Scanning.

This layer focuses on **depth and accuracy**, complementing Semgrep’s speed.

---

### Dependency Security (SCA)

- **pip-audit** scans Python dependencies against known vulnerability databases.
- Fails the pipeline if vulnerable packages are detected.
- Ensures third-party risk is evaluated alongside application code.

This prevents vulnerable dependencies from silently entering the codebase.

---

### Secret Detection & Key Handling

- **TruffleHog** is used for secret scanning across:
  - Filesystem (working tree)
  - Git history
- Scanning strategy:
  - PR / push: filesystem + recent git changes (fail on any result)
  - Weekly scan on `main`: full history (fails only on verified secrets)

- Secrets are never stored in the repository:
  - All sensitive keys are stored in **GitHub Actions secrets**
  - Written to disk only at runtime
  - Excluded via `.gitignore` and TruffleHog exclude paths
  - Securely removed after use

This approach balances **security coverage** with **false-positive control**.

---

### Developer Guardrails (Pre-commit)

- **Pre-commit hooks** run locally before every commit:
  - Formatting checks
  - YAML and merge sanity checks
  - Secret detection via Gitleaks
- The same hooks are enforced in CI using `pre-commit/action`.

This guarantees that:
- Unsafe changes are blocked early
- CI enforces the same standards across all contributors
- Security rules function as **policy-as-code**, not optional guidance

---

### CI Enforcement & Governance

- All checks run automatically via **GitHub Actions**.
- Branch protection ensures:
  - No direct pushes to `main`
  - No merges without all security checks passing
- The pipeline follows a **Fail → Fix → Pass** model:
  - Security issues fail the pipeline
  - Fixes are validated automatically
  - Only compliant code is allowed to merge

---

### Design Principles

This pipeline is intentionally:
- **Layered** (SAST, Deep SAST, SCA, Secrets, Guardrails)
- **Shift-left focused**
- **Developer-friendly but non-bypassable**
- **Extensible** for future hardening and scale

It reflects how DevSecOps pipelines operate in real engineering organizations — not just demo environments.



---

## Fail → Fix → Pass (Semgrep demo)

**Intent:** prevent unsafe language-level constructs from reaching `main`.

**Before (intentional):**
  ```python
  # insecure: eval(user_input)
  ```
**After (fixed):**
  ```python
  import ast

  def safe_eval_literal(expr: str):
          return ast.literal_eval(expr)  # evaluates only safe Python literals
  ```
**Workflow:**
1. Pull request introduces `eval(...)` → **Semgrep detects unsafe pattern** → CI fails
2. Code is refactored to `ast.literal_eval`
3. Semgrep passes → Merge to `main`is allowed

**Security outcome:**
Basic code injection risks are eliminated early through fast, pattern-based SAST.

---

## Fail → Fix → Pass (TruffleHog demo)

**Intent:** prevent credential leakage into version control.

**Before (intentional):**
```
# fake_secret.txt
-----BEGIN RSA PRIVATE KEY-----
MIIBOQIBAAJAXW...
```
**After (fixed):**
- Secret removed from the repository
- Keys injected securely at runtime via GitHub Actions Secrets
- `keys/**` excluded from both Git history and filesystem scans

**Workflow:**
1. Push containing a private key → **TruffleHog fails the pipeline**
2. Secrets moved to GitHub Actions Secrets → pipeline passes

**Security outcome:**
No long-lived credentials are stored in source control; secret exposure is blocked automatically.

---

## Fail → Fix → Pass (Pre-commit demo)

**Intent:** stop security issues before they even reach CI.

**Before (intentional):**
```text
tests/accidental_secret.txt
-----Sample_Alfreds-private-key.pem-----
```

**After (fixed):**
- Secret removed from staged files

**Workflow:**

1. Developer attempts to commit a staged secret → **pre-commit blocks the commit** (Gitleaks finds it)
2. Secret is removed → commit succeeds
3. CI re-runs the same hooks to ensure enforcement consistency (via `pre-commit/action`)

**Security outcome:**
Security rules are enforced as policy, not convention — locally and in CI.

---

## Fail → Fix → Pass (CodeQL demo)

**Intent:** detect complex, data-flow–driven vulnerabilities that pattern-based tools may miss.

**Before (intentional):**
- Code introduces a data-flow path from user-controlled input to a sensitive sink
- Issue is not trivially detectable via pattern matching

**Workflow:**
1. Pull request triggers CodeQL analysis
2. CodeQL identifies a vulnerable data-flow path
3. Finding is uploaded as SARIF and surfaced in GitHub Code Scanning
4. Pull request is blocked until the issue is remediated

**After (fixed):**
- Vulnerable flow is eliminated
- CodeQL re-run reports no findings

**Security outcome:**
High-impact vulnerabilities are prevented from merging, with findings visible and auditable via GitHub’s native security UI.

---

## Local Usage

These commands allow developers to reproduce CI security checks locally, enabling faster feedback and easier debugging before opening a pull request.


Run demo tests locally:
```
python3 -m tests.test_app
# or, with pytest:
# pip install pytest
pytest -v
```
![tests_locally](docs/img/tests_locally.png)

Run TruffleHog locally:
```
sudo docker run --rm -v "$PWD":/repo -v "$PWD/trufflehog_exclude_paths.txt":/trufflehog_exclude_paths.txt ghcr.io/trufflesecurity/trufflehog:latest git file:///repo  --since-commit HEAD --results=verified,unverified,unknown --fail
```
![trufflehog_git_locally](docs/img/trufflehog_git_locally1.png)

```
sudo docker run --rm -v "$PWD":/repo -v "$PWD/trufflehog_exclude_paths.txt":/trufflehog_exclude_paths.txt ghcr.io/trufflesecurity/trufflehog:latest filesystem /repo  --exclude-paths=/trufflehog_exclude_paths.txt --results=verified,unverified,unknown --fail

```
![trufflehog_filesystem_locally](docs/img/trufflehog_filesystem_locally1.png)

Run Pre-commit locally:
```
pre-commit run --hook-stage manual gitleaks-docker-dir  -v
```
![pre-commit_manual_locally](docs/img/precommit-gitleaks_manual_fail.png)

```
pre-commit run --all-files
```
![pre-commit_all_locally](docs/img/precommit_all.png)

---

## Project Structure
```
devsecops-ci-pipeline-demo/
├─ src/                           # Demo application code
│  └─ app.py
├─ tests/                         # Basic tests for the demo app
│  └─ test_app.py
├─ semgrep/                       # SAST rules (Semgrep)
│  └─ semgrep.yml
├─ .github/workflows              # CI/CD (GitHub Actions)
│  └─ ci.yml
├─ docs/img/                      # Screenshots
├─ .gitignore                     # excludes runtime keys
├─ trufflehog_exclude_paths.txt   # exclude paths for TruffleHog
├─ .pre-commit-config.yaml        # Pre-commit hooks config
├─ .gitleaks.toml                 # Gitleaks config (custom rules + allowlist)
├─ README.md
└─ requirements.txt
```

---

## Screenshots (CI & Developer Feedback)

The screenshots below illustrate how security controls behave across failure and remediation scenarios, both locally and in CI.
They demonstrate how security issues are detected early, enforced automatically, and resolved before code is allowed to merge into `main`.

---

### Semgrep — Pattern-based SAST

**Semgrep (Fail)**
This screenshot shows a pull request failing due to the presence of an unsafe coding pattern (`eval`).
Semgrep blocks the change early in the pipeline and provides immediate feedback to the developer.


![Semgrep fail example](docs/img/semgrep-fail.png)

**Semgrep (Pass)**
After refactoring the code to remove the unsafe construct, Semgrep reports no findings and the pipeline passes.

![Semgrep pass example](docs/img/semgrep-pass.png)

---

### TruffleHog — Secret Detection

**TruffleHog (Fail)**
This screenshot demonstrates TruffleHog detecting a leaked private key in the repository, causing the pipeline to fail and preventing secret exposure.

![TruffleHog fail example](docs/img/trufflehog_fail.png)

**TruffleHog (Pass)**
After removing the secret from the repository and handling keys securely via GitHub Actions secrets, TruffleHog reports a clean scan and the pipeline succeeds.

![TruffleHog pass example](docs/img/trufflehog_pass.png)

**TruffleHog (Weekly Scan — pass)**
This screenshot shows the scheduled weekly scan on the `main` branch.
The scan covers the full git history and is configured to fail only on verified secrets, balancing security coverage with false-positive control.

![TruffleHog_Weekly pass example](docs/img/trufflehog_weekly_scan.png)

---

### Dependency Security – pip-audit

**pip-audit (pass)**
This screenshot shows `pip-audit` reporting no known vulnerabilities in Python dependencies.
Dependency security is enforced as part of the CI pipeline alongside application-level checks.

![pip-audit pass example](docs/img/pip_audit_scan_pass_second.png)

---

### CodeQL – Deep SAST (Pull Request Gate)

**CodeQL (PR Gate — Fail → Pass)**
These screenshots demonstrate CodeQL operating as a mandatory security gate during pull requests.

> Note: In this repository, CodeQL enforcement is reflected at the pull request level via required status checks, as shown below.

**CodeQL (Fail)**
When CodeQL detects a security issue:
- The pull request is marked as **checks failed**
- Merge to `main` is blocked
- Findings are uploaded in SARIF format and surfaced via GitHub Code Scanning

![PR checks failed (CodeQL fail)](docs/img/codeql-pr-fail3-sql.png)

**CodeQL (Pass)**
After the issue is remediated:
- CodeQL re-runs automatically on the updated commit
- The security check passes
- The pull request becomes eligible for merge

![PR checks passed (CodeQL pass)](docs/img/codeql-main-accept.png)

---

### Developer Guardrails – Pre-commit

**Pre-commit (Fail)**
This screenshot shows a local commit being blocked by pre-commit hooks after detecting a staged secret via Gitleaks.

![Pre-commit fail](docs/img/git_fail_precommit.png)

**Pre-commit (Pass)**
After removing the secret, the commit succeeds locally.
The same hooks are re-executed in CI to ensure consistent enforcement across all contributors.

![Pre-commit pass](docs/img/git_pass_precommit.png)
![Pre-commit pass (CI)](docs/img/pass_precommit_ci.png)

---

## Why This Project?

Modern software delivery requires speed **without compromising security**.

This repository demonstrates how security controls can be embedded directly into CI/CD workflows as **non-bypassable guardrails**, enabling teams to shift security left without slowing down development.

By combining:
- Semgrep for fast, pattern-based SAST
- CodeQL for deep, data-flow–aware analysis
- TruffleHog for secret detection
- pip-audit for dependency risk assessment
- Pre-commit hooks for early, local enforcement

the project showcases a **layered DevSecOps approach** that blocks insecure code, leaked secrets, and vulnerable dependencies *before* they reach `main`.

> Note: The focus is not on tools themselves, but on enforcement, visibility, and repeatability — reflecting how real engineering teams operate at scale.

---

## Branch Protection

The `main` branch is protected to ensure that all changes are reviewed, validated, and security-checked before merge.

**Recommended settings:**

- ✅ Require a pull request before merging
  Ensures all changes are reviewed and evaluated through CI.

- ✅ Require status checks to pass
  Enforces all security controls as mandatory gates, including:
  - Semgrep (SAST)
  - CodeQL (deep SAST and code scanning)
  - TruffleHog (secret detection)
  - pip-audit (dependency vulnerability scanning)
  - Pre-commit hooks (policy-as-code enforcement)

- (Optional) ✅ Require branches to be up to date before merging
  Prevents outdated code from bypassing newly introduced security controls.

These protections ensure:
- No direct pushes to `main`
- No merges without verified, passing security checks

---

## License
This project is licensed under the MIT License.
