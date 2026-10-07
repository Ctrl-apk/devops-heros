# 15 — CI/CD & GitHub Actions

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and workflow files: [../../session-16-github-actions/](../../session-16-github-actions/)

---

## 📌 Concepts Covered

### 1. CI vs CD
- **Continuous Integration (CI):** The practice of automating the building and testing of code changes every time code is committed to the repository (e.g., unit testing, linting, building Docker image).
- **Continuous Deployment (CD):** Automating the deployment of code to staging or production environments after passing CI quality gates.

### 2. GitHub Actions Terminology

| Component | Description |
|---|---|
| **Workflow** | Automated process defined in a `.yml` file under `.github/workflows/` |
| **Event (`on`)** | Trigger that starts workflow execution (e.g., `push`, `pull_request`) |
| **Job** | Set of steps executing on the same runner runner environment |
| **Step** | Individual task (running shell script or invoking a reusable Action) |
| **Runner** | Server host executing jobs (`ubuntu-latest`, self-hosted) |
| **Secrets** | Encrypted credentials stored securely in repository settings |
| **Artifacts** | Files generated during workflow execution stored for download/sharing |

---

## Workflow Diagram

```text
 [ Developer Push ] ──► [ GitHub Trigger: push main ]
                              │
                              ▼
                ┌───────────────────────────┐
                │ Job: build-and-test (CI)  │
                │ 1. Checkout repository    │
                │ 2. Set up Python 3.12     │
                │ 3. Install dependencies   │
                │ 4. Run unit tests         │
                │ 5. Build Docker image     │
                │ 6. Upload Build Artifact  │
                └─────────────┬─────────────┘
                              │ (Success)
                              ▼
                ┌───────────────────────────┐
                │     Job: deploy (CD)      │
                │ 1. Download Artifact      │
                │ 2. Deploy to Production   │
                └───────────────────────────┘
```

---

## Project Structure & Deliverables

- `app.py`: Flask application with `/` and `/health` endpoints
- `requirements.txt`: Project Python dependencies
- `Dockerfile`: Multi-stage Docker packaging configuration
- `.github/workflows/ci-cd.yml`: Complete GitHub Actions CI/CD automation workflow

---

## Sample Pipeline Execution Logs

```text
Run actions/checkout@v4
  Syncing repository... Done.
Run python -m pytest
  =================== 2 passed in 0.42s ===================
Run docker build -t devops-app:a1b2c3d .
  Step 1/6 : FROM python:3.12-slim
  ...
  Successfully built 987654321abc
  Successfully tagged devops-app:a1b2c3d
Run deploy
  Deploying application commit a1b2c3d...
  Deployment completed successfully!
```
