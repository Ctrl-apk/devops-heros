# 19 — Monitoring, Observability & GitOps

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and manifests: [../../session20-monitoring-observability-gitops/](../../session20-monitoring-observability-gitops/)

---

## Task 1: Monitoring vs Observability

- **Monitoring:** Tells you *when* a system is failing (e.g., CPU > 90%, HTTP 500 error rate spikes). Answers **"What is broken?"**
- **Observability:** Provides deep internal visibility into *why* a system is failing by correlating telemetry data. Answers **"Why is it broken?"**

---

## Task 2: The Three Pillars of Observability (MELT)

```text
               ┌─────────────────────────────────────────┐
               │    Observability Telemetry (MELT)       │
               └────────────────────┬────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
   [ 1. Metrics ]            [ 2. Logs ]                [ 3. Traces ]
 Numeric aggregations     Timestamped record of      End-to-end request flow
 (e.g. CPU, Memory,      discrete system events     across microservices (Jaeger,
 Throughput, Prometheus) (Loki, Fluentd, ELK)        OpenTelemetry, Zipkin)
```

### 1. Metrics
Numeric representations of data measured over intervals of time (e.g., CPU utilization %, Memory usage, HTTP request counter, error rate).
- *Tools:* Prometheus, Grafana, Datadog.

### 2. Logs
Timestamped text records emitted by containers or applications detailing runtime events and stack traces.
- *Tools:* Grafana Loki, Elasticsearch, Logstash, Fluentd (EFK/ELK).

### 3. Traces
Tracks the lifecycle of a single request as it propagates through distributed microservices.
- *Tools:* Jaeger, Zipkin, OpenTelemetry.

---

## Task 3: GitOps Architecture

**GitOps** is an operational framework that uses Git repositories as the **single source of truth** for infrastructure and application code.

### Key Principles of GitOps
1. **Declarative Specification:** System state defined declaratively in Git (YAML manifests/Helm).
2. **Version Controlled State:** Every state change is a Git commit with auditing and rollback capability.
3. **Continuous Reconciliation:** GitOps controller (ArgoCD / Flux) automatically syncs cluster state to match Git.
4. **Self-Healing:** If someone manually modifies cluster resources (`kubectl edit`), ArgoCD automatically reverts the drift back to Git state!

```text
[ Developer Commit ] ──► [ Git Repository (Source of Truth) ]
                                    │
                                    ▼ (Polls or Webhook)
                        [ ArgoCD Operator ]
                                    │ (Reconciles Drift)
                                    ▼
                      [ Kubernetes Cluster State ]
```

---

## Deliverables & Manifest Files

1. `app/prometheus-deployment.yaml`: Application with Prometheus metrics annotations (`prometheus.io/scrape: "true"`).
2. `app/argocd-application.yaml`: Declarative ArgoCD GitOps Application resource pointing to Git repo.

---

## Sample Command Outputs

```bash
# Verify metrics scraping endpoint inside cluster
$ kubectl exec -it metrics-demo-app-7d6f5485-k987x -- curl http://localhost:8080/metrics
# HELP http_requests_total Total HTTP requests handled.
# TYPE http_requests_total counter
http_requests_total{code="200",handler="prometheus"} 1024

# Check ArgoCD Sync Status
$ argocd app get devops-hero-gitops-app
Name:               devops-hero-gitops-app
Project:            default
Server:             https://kubernetes.default.svc
Namespace:          default
URL:                https://argocd.example.com/applications/devops-hero-gitops-app
Repo:               https://github.com/Ctrl-apk/devops-heros.git
Target:             HEAD
Path:               homework/19-monitoring-observability-gitops/app
Sync Status:        Synced to HEAD (a1b2c3d)
Health Status:      Healthy
```
