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
- **SAST** with **Semgrep** (custom rule)
- **Secret Scanning** with **TruffleHog** (filesystem + git history)
- **Key Management** best practices via GitHub Actions secrets
- Clean **PR workflow** with **Branch Protection**
- Clear **Fail → Fix → Pass**

---

## Current Status
- [x] Project structure initialized (`src`, `tests`, `workflows`)
- [x] Demo Python app with basic tests
- [x] **Semgrep (SAST)** integrated and demonstrated
- [x] **TruffleHog (secrets)** integrated for filesystem + git scans
- [x] Keys handled securely (stored in GitHub secrets, excluded from repo)
- [x] Add scheduled TruffleHog scan on main (verified-only)
- [x] Add pip-audit (dependency scanning)
- [x] **Pre-commit hooks** (Black, YAML/merge checks, Gitleaks staged) + enforced in CI
- [ ] Polish docs (badges, PR/Issue templates), Release `v0.1`

---

## Roadmap (Next Steps)
1. **Polish:** badges, templates, demo screencast (30–45s)
2. **Release:** tag first stable version (`v0.1`).

---

## How It Works
- **Semgrep job:** (`semgrep/semgrep.yml`) blocks unsafe patterns (e.g., `eval(...)`).
- **TruffleHog jobs:**
  - **Filesystem scan:** scans working tree at every PR/push (`--results=verified,unverified,unknown --fail`).
  - **Git history scan:** scans commits since previous push (using '--since-commit'), preventing old leaks from blocking new work.
  - **Weekly scheduled scan on `main`:** runs every Monday, scanning the full history but **fails only on verified secrets** → reduces false positives while ensuring repo stays clean over time.
  - **pip-audit job:** (`pip-audit` Action step) audits `requirements.txt` against the Python Packaging Advisory DB.
    → Fails CI if vulnerable dependencies are detected.
- **Key Handling:**
  - Private keys (`Alfred`, `Marina`, `Christina`) are stored in GitHub Actions secrets.
  - At runtime, they’re written into `keys/` (excluded via `.gitignore` + `trufflehog_exclude_paths.txt`).
  - Keys are securely shredded after use.
- **Pre-commit hooks:**
  - Run locally on staged files before every commit (`pre-commit install`).
  - Includes formatters (Black), sanity checks (YAML, merge conflicts), and **Gitleaks**.
  - Prevents committing secrets by blocking staged leaks.
- **CI Pre-commit job:**
  - Runs all hooks on every push/PR (`pre-commit/action`).
  - Guarantees consistent enforcement across developer machines and CI.

---

## Fail → Fix → Pass (Semgrep demo)
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
1. PR with `eval` → CI fails.
2. Fix applied (`ast.literal_eval`) → CI passes.
3. Merge allowed to `main`.

This demonstrates a real DevSecOps guardrail: unsafe code can’t reach `main`.

---

## Fail → Fix → Pass (TruffleHog demo)
**Before (intentional):**
```
# fake_secret.txt
-----BEGIN RSA PRIVATE KEY-----
MIIBOQIBAAJAXW...
```
**After (fixed):**
- File removed from repo.
- Runtime keys generated securely from GitHub Secrets.
- `keys/**` excluded from repo & TruffleHog scan.

**Workflow:**
1. Push with fake key → **TruffleHog fails** pipeline.
2. Keys moved to **GitHub Secrets** → pipeline passes.

---

## Fail → Fix → Pass (Pre-commit demo)

**Before (intentional):**
```text
tests/accidental_secret.txt
-----Sample_Alfreds-private-key.pem-----
```

**After (fixed):**
- remove the secret

**Workflow:**

1.  Try to commit a staged file with a fake secret → **pre-commit blocks** the commit (Gitleaks finds it).
2. Comment/remove the fake secret → commit succeeds.
3. CI runs the same hooks (via `pre-commit/action`) to enforce rules repo-wide.

---

## Local Usage

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

## Screenshots
- **Semgrep (Fail)**
![Semgrep fail example](docs/img/semgrep-fail.png)

- **Semgrep (Pass)**

![Semgrep pass example](docs/img/semgrep-pass.png)

- **TruffleHog(Fail)**
![TruffleHog fail example](docs/img/trufflehog_fail.png)

- **TruffleHog(Pass)**
![TruffleHog pass example](docs/img/trufflehog_pass.png)

- **TruffleHog_Scan_weekly(pass):**
![TruffleHog_Weekly pass example](docs/img/trufflehog_weekly_scan.png)

- **pip-audit(pass):** – reports no known vulnerabilities

![pip-audit pass example](docs/img/pip_audit_scan_pass_second.png)

- **PR Checks** – “Checks failed” → “All checks have passed”
![PR checks failed](docs/img/pr-checks-fail.png)
![PR checks passed](docs/img/pr-checks-pass.png)

- **Pre-commit (Fail)**
![Pre-commit fail](docs/img/git_fail_precommit.png)

- **Pre-commit (Pass)**
![Pre-commit pass](docs/img/git_pass_precommit.png)
![Pre-commit pass](docs/img/pass_precommit_ci.png)
---

## Why This Project?

Modern delivery needs speed **and** security.
This repo shows how to **shift security left** and enforce guardrails directly in CI/CD — blocking unsafe patterns and secret leaks before they ever reach `main`.

Together, Semgrep (SAST), TruffleHog (secret scanning), and pip-audit (SCA) demonstrate a layered DevSecOps approach:
catching code issues, secret leaks, and vulnerable dependencies before merge.

---

## Branch Protection

Recommended settings for `main`:

✅ Require a pull request before merging

✅ Require status checks to pass (Semgrep+TruffleHog jobs).

(Optional) ✅ Require branches to be up to date before merging

This ensures **no direct pushes** and **no merges without green checks**.

---

## License
This project is licensed under the MIT License.
