# 16 — Complete CI/CD & DevSecOps

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and workflow files: [../../session-17-devsecops/](../../session-17-devsecops/)

---

## 📌 Overview

This project implements a complete **DevSecOps Pipeline** that shifts security left by integrating automated security scans directly into every stage of the software development lifecycle before code deployment.

---

## DevSecOps Pipeline Flow

```text
Code Commit
    │
    ▼
Unit Testing & App Build
    │
    ▼
[ 1. SAST Scan (Bandit) ] ── Static Application Security Testing
    │
    ▼
[ 2. SCA Scan (Safety) ] ── Software Composition Analysis (Dependencies)
    │
    ▼
[ 3. Secret Scan (Gitleaks) ] ── Hardcoded API Keys / Tokens Scan
    │
    ▼
Docker Image Build
    │
    ▼
[ 4. Container Scan (Trivy) ] ── Vulnerability Scanning on Base Image
    │
    ▼
[ 5. Security Gate ] ── Enforces Quality/Security Policy Thresholds
    │
    ▼
Image Registry Push ──► Kubernetes Deployment
```

---

## Security Tools Breakdown

| Security Pillar | Tool Used | Purpose |
|---|---|---|
| **SAST** | Bandit | Analyzes Python source code for security flaws (SQL injection, hardcoded passwords) |
| **SCA** | Safety | Scans `requirements.txt` for known vulnerable package versions |
| **Secret Scanning** | Gitleaks / TruffleHog | Detects committed API keys, private SSH keys, or secrets |
| **Container Image Scanning** | Trivy | Scans Docker layers for CVEs (Common Vulnerability Enumerations) |
| **Security Gates** | GitHub Actions Policy | Fails the pipeline if Critical/High vulnerabilities are found |

---

## Deliverables & Files

- `app/main.py`: Hardened Flask web microservice running as non-root user
- `Dockerfile`: Multi-stage, non-root Alpine container spec
- `.github/workflows/devsecops.yml`: GitHub Actions pipeline with integrated security steps
- `k8s/deployment.yaml`: Production Kubernetes deployment with Pod `securityContext`

---

## Sample Pipeline Execution Output

```text
Run Gitleaks Secret Scan
  No leaks found. Secret scan passed!
Run Bandit SAST Scan
  Test results: No high severity issues detected.
Run Safety SCA Scan
  0 known vulnerabilities found in dependencies.
Run Trivy Container Scan
  devsecops-app:latest (alpine 3.20.0)
  Total: 0 (CRITICAL: 0, HIGH: 0)
Run Security Gate Validation
  All security checks passed successfully!
```
