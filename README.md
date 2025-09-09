# devsecops-ci-pipeline-demo

This repository demonstrates how to build a **secure CI/CD pipeline** by integrating security tools into the development workflow.  
The goal is to showcase how security can be an enabler, not a blocker, in modern development.

> CI platform: **GitHub Actions** (automatically runs on every push and pull request)

---

## Current Status
- [x] Project structure initialized (`src`, `tests`, `workflows`)
- [x] Demo Python app with basic test
- [ ] Add Semgrep (SAST scanning)
- [ ] Add TruffleHog (secret scanning)
- [ ] Add pip-audit (dependency scanning)
- [ ] Improve README and documentation

---

## Next Steps (Roadmap)
1. **Semgrep (SAST):** Add custom rules and run them in CI to detect insecure patterns (e.g., `eval`).
2. **TruffleHog (Secrets):** Scan for secrets in files/history with strict fail policy on real findings.
3. **pip-audit (SCA):** Audit Python dependencies for known vulnerabilities, failing only on High/Critical issues.
4. **Polish:** Enhance documentation, add status badges, PR/Issue templates, and publish Release `v0.1`.

---

## Project Structure
```
devsecops-ci-pipeline-demo/
├─ src/ # Demo application code
│ └─ app.py
├─ tests/ # Basic tests for the demo app
│ └─ test_app.py
├─ .github/workflows # CI/CD configuration (GitHub Actions)
├─ README.md
└─ requirements.txt
```

---

## Why this project?
Modern software delivery requires speed **and** security.  
This project demonstrates how security can be embedded directly into pipelines — shifting left and automating checks for safer, faster delivery.

---

## License
This project is licensed under the MIT License.

