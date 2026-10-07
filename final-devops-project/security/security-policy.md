# DevSecOps Security Policy & Architecture

## Security Pillars

| Security Stage | Tool | Enforcement Level | Pipeline Behavior |
|---|---|---|---|
| **SAST** (Static Application Security Testing) | Bandit | High / Critical Flaws | Fails build on High severity security flaws |
| **SCA** (Software Composition Analysis) | Safety | CVE Vulnerabilities | Flags known vulnerable Python packages |
| **Secret Scanning** | Gitleaks | Zero Tolerance | Blocks commits containing API keys or tokens |
| **Container Scanning** | Trivy | CRITICAL, HIGH | Fails container build on unfixed CVEs |
| **Security Gates** | GitHub Actions Policy | Policy Threshold | Prevents deployment if any gate fails |

---

## Container Security Controls

1. **Non-root Execution:** `USER appuser` (UID: 10001, GID: 10001).
2. **Minimal Base Image:** Python 3.12 Slim on Debian/Alpine.
3. **ReadOnly Root Filesystem Readiness:** Application writes only to explicit temp/data volumes.
4. **Pod Security Context:**
   ```yaml
   securityContext:
     runAsNonRoot: true
     runAsUser: 10001
     runAsGroup: 10001
     fsGroup: 10001
   ```
