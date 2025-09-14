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
- [ ] Add pip-audit (dependency scanning)
- [ ] Polich docs (badges, PR/Issue templates), Release `v0.1`

---

## Roadmap (Next Steps)
1. **pip-audit (SCA):** audit Python dependencies; fail on High/Critical.
2. **Polish:** badges, templates, demo screencast (30–45s)
3. **Release:** tag first stable version (`v0.1`).

---

## How It Works
- **Semgrep job:** (`semgrep/semgrep.yml`) blocks unsafe patterns (e.g., `eval(...)`).
- **TruffleHog jobs:**
  - **Filesystem:** scans working tree at every PR/push (`--results=verified,unverified,unknown --fail`).
  - **Git history:** scans commits since previous push (using '--since-commit'), preventing old leaks from blocking new work.
- **Key Handling:**
  - Private keys (`Alfred`, `Marina`, `Christina`) are stored in GitHub Actions secrets.
  - At runtime, they’re written into `keys/` (excluded via `.gitignore` + `trufflehog_exclude_paths.txt`).
  - Keys are securely shredded after use.

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
---

## Project Structure
```
devsecops-ci-pipeline-demo/
├─ src/                      # Demo application code
│  └─ app.py
├─ tests/                    # Basic tests for the demo app
│  └─ test_app.py
├─ semgrep/                  # SAST rules (Semgrep)
│  └─ semgrep.yml
├─ .github/workflows         # CI/CD (GitHub Actions)
│  └─ ci.yml
├─ docs/img/                 # Screenshots
├─ .gitignore                # excludes runtime keys
├─ trufflehog_exclude_paths.txt
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

- **PR Checks** – “Checks failed” → “All checks have passed”
![PR checks failed](docs/img/pr-checks-fail.png)
![PR checks passed](docs/img/pr-checks-pass.png)

---

## Why This Project?

Modern delivery needs speed **and** security.
This repo shows how to **shift security left** and enforce guardrails directly in CI/CD — blocking unsafe patterns and secret leaks before they ever reach `main`.

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