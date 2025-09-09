# devsecops-ci-pipeline-demo

Demonstrates how to build a **secure CI/CD pipeline** by integrating security checks into developer workflows — making security an **enabler**, not a blocker.

> CI platform: **GitHub Actions** (automatically runs on every push and pull request)

[![CI - Security Checks](https://github.com/0xmarziehlabs/devsecops-ci-pipeline-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/0xmarziehlabs/devsecops-ci-pipeline-demo/actions)


---

## Table of Contents
- [What This Is](#what-this-is)
- [Current Status](#current-status)
- [Roadmap (Next Steps)](#roadmap-next-steps)
- [How It Works (so far)](#how-it-works-so-far)
- [Fail → Fix → Pass (Semgrep demo)](#fail--fix--pass-semgrep-demo)
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
- Clean **PR workflow** with **Branch Protection**
- Clear **Fail → Fix → Pass** narrative recruiters love

> Next modules will add **Secret Scanning (TruffleHog)** and **Dependency Scanning (pip-audit)**.

---

## Current Status
- [x] Project structure initialized (`src`, `tests`, `workflows`)
- [x] Demo Python app with basic tests
- [x] **Semgrep (SAST) integrated** into CI (custom `eval` rule)  
- [x] **Fix applied** to remove unsafe `eval` usage (pipeline green)
- [ ] Add TruffleHog (secret scanning)
- [ ] Add pip-audit (dependency scanning)
- [ ] Improve documentation (badges, PR/Issue templates), Release `v0.1`

---

## Roadmap (Next Steps)
1. **TruffleHog (Secrets):** scan worktree + git history; fail PRs on real findings.
2. **pip-audit (SCA):** audit Python dependencies; fail on High/Critical.
3. **Polish:** badges, templates, short demo screencast (30–45s), Release `v0.1`.

---

## How It Works (so far)
- **Custom Semgrep rule** (`semgrep/semgrep.yml`) flags any use of `eval(...)` as **ERROR**.
- **GitHub Actions** workflow (`.github/workflows/ci.yml`) runs Semgrep on every **push/PR**.
- **Branch protection** (on `main`) prevents merging unless checks pass → enforces guardrails.

---

## Fail → Fix → Pass (Semgrep demo)
**Intentional vulnerability** (for training only) was introduced and then fixed:
- **Before (intentional):**
  ```python
  # insecure: eval(user_input)
  ```
- **After (fixed):**
  ```python
  import ast

  def safe_eval_literal(expr: str):
          return ast.literal_eval(expr)  # evaluates only safe Python literals
  ```
**PR flow:**
1. Open PR with the intentional `eval` → CI fails (Semgrep catches it).
2. Commit the fix (replace/remove `eval`) → CI turns green.
3. Merge to `main` (protected branch).

This demonstrates a real DevSecOps guardrail: unsafe code can’t reach `main`.

---

## Local Usage

Run demo tests locally:
```
python3 -m tests.test_app
# or, with pytest:
# pip install pytest
# pytest -v
```
![tests_locally](docs/img/tests_locally.png)

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
├─ .github/workflows         # CI/CD configuration (GitHub Actions)
│  └─ ci.yml
├─ README.md
└─ requirements.txt
```

---

## Screenshots
Actions (Fail) – Semgrep flags `eval` on the first PR
![Semgrep fail example](docs/img/semgrep-fail.png)

Actions (Pass) – After fix, pipeline turns green
![Semgrep pass example](docs/img/semgrep-pass.png)

PR view – “Checks failed” → “All checks have passed”
![PR checks failed](docs/img/pr-checks-fail.png)
![PR checks passed](docs/img/pr-checks-pass.png)

---

## Why This Project?

Modern delivery needs speed and security.
This repo shows how to shift left and automate checks so issues are caught before merging — resulting in safer, faster delivery.

This is a living demo — new modules (secret scanning, dependency scanning) will be added to evolve the pipeline step by step.

---

## Branch Protection

`Settings → Branches → Add rule (main)`
Recommended:

✅ Require a pull request before merging

✅ Require status checks to pass (select the Semgrep job)

(Optional) ✅ Require branches to be up to date before merging

This ensures no direct pushes and no merges without green checks.

---

## License
This project is licensed under the MIT License.