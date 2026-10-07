# GitOps Declarative Workflow Architecture

## Core GitOps Principles

1. **Declarative Configuration:** All Kubernetes resources are defined declaratively using Helm charts stored in Git.
2. **Git as Source of Truth:** Cluster state changes must be committed to the Git repository.
3. **Automated Continuous Reconciliation:** ArgoCD continually compares desired state in Git against live cluster state.
4. **Self-Healing:** Manual out-of-band drift (`kubectl edit/delete`) is automatically reverted back to the Git state.

```text
[ Developer Commit ] ──► [ GitHub Repository ]
                                │
                                ▼
                       [ ArgoCD Controller ] ◄── Continuous Drift Monitoring
                                │
                                ▼
                     [ Target K8s Cluster ]
```
