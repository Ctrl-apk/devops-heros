# 14 — Helm Package Manager

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and chart files: [../../session-15-helm/](../../session-15-helm/)

---

## Task 1: Essential Helm Commands Cheat Sheet

| Command | Purpose | Example |
|---|---|---|
| `helm create` | Scaffold a new Helm chart template directory structure | `helm create my-chart` |
| `helm install` | Install a Helm chart package onto Kubernetes | `helm install my-app ./my-chart` |
| `helm list` | List all installed releases in current namespace | `helm list -A` |
| `helm status` | Display status and detailed deployment notes of a release | `helm status my-app` |
| `helm get` | Fetch manifests, values, or hooks of a release | `helm get manifest my-app` |
| `helm upgrade` | Upgrade release configuration or image version | `helm upgrade my-app ./my-chart --set replicaCount=3` |
| `helm history` | Show release revision history and rollout status | `helm history my-app` |
| `helm rollback` | Roll back release to a previous revision | `helm rollback my-app 1` |
| `helm uninstall` | Delete a release and purge associated Kubernetes resources | `helm uninstall my-app` |
| `helm repo` | Add, update, or list remote Helm chart repositories | `helm repo add bitnami https://charts.bitnami.com/bitnami` |
| `helm search` | Search for charts in artifact hub or local repositories | `helm search repo nginx` |

---

## Task 2: Complete Helm Rollback Workflow

```text
Install (Rev 1) ──► Upgrade (Rev 2) ──► Verify (Rev 2) ──► Upgrade (Rev 3 - Faulty) ──► Verify (Failing) ──► Rollback to Rev 2 ──► Verify (Healthy!)
```

### Execution Steps & Command Log

```bash
# 1. Initial Installation (Revision 1)
$ helm install notes-app ./notes-chart --set image.tag=1.25.3-alpine
NAME: notes-app
LAST DEPLOYED: Tue Oct  6 20:00:00 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1

# 2. First Upgrade (Revision 2 - Increase Replicas)
$ helm upgrade notes-app ./notes-chart --set replicaCount=3 --set image.tag=1.25.3-alpine
Release "notes-app" has been upgraded. Happy Helming!
STATUS: deployed
REVISION: 2

# 3. Verify Revision 2
$ helm history notes-app
REVISION    UPDATED                     STATUS      CHART               APP VERSION DESCRIPTION
1           Tue Oct  6 20:00:00 2026    superseded  notes-chart-0.1.0   1.0.0       Install complete
2           Tue Oct  6 20:05:00 2026    deployed    notes-chart-0.1.0   1.0.0       Upgrade complete

# 4. Faulty Upgrade (Revision 3 - Invalid Image Tag)
$ helm upgrade notes-app ./notes-chart --set image.tag=nonexistent-tag-999
Release "notes-app" has been upgraded.
REVISION: 3

# 5. Observe Failure in Cluster
$ kubectl get pods
NAME                                   READY   STATUS             RESTARTS   AGE
notes-app-deployment-5d8f6448c-k987x   0/1     ImagePullBackOff   0          45s

# 6. Execute Rollback to Revision 2
$ helm rollback notes-app 2
Rollback release notes-app to revision 2 successful.

# 7. Final Verification
$ helm history notes-app
REVISION    UPDATED                     STATUS      CHART               APP VERSION DESCRIPTION
1           Tue Oct  6 20:00:00 2026    superseded  notes-chart-0.1.0   1.0.0       Install complete
2           Tue Oct  6 20:05:00 2026    superseded  notes-chart-0.1.0   1.0.0       Upgrade complete
3           Tue Oct  6 20:10:00 2026    superseded  notes-chart-0.1.0   1.0.0       Upgrade complete
4           Tue Oct  6 20:12:00 2026    deployed    notes-chart-0.1.0   1.0.0       Rollback to 2

$ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
notes-app-deployment-6869446fc-2k7p9   1/1     Running   0          10s
notes-app-deployment-6869446fc-89m2l   1/1     Running   0          10s
notes-app-deployment-6869446fc-w4l1q   1/1     Running   0          10s
```

---

## Task 3: Mini Project — Parameterized Helm Chart

The mini project is organized in [./mini-project/notes-chart](./mini-project/notes-chart):
- `Chart.yaml`: Metadata configuration
- `values.yaml`: Default parameters (replicas, image, service configuration)
- `templates/deployment.yaml`: Parameterized Kubernetes deployment template
- `templates/service.yaml`: Parameterized Kubernetes service template
