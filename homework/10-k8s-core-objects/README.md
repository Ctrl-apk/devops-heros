# 10 — Kubernetes Pods, ReplicaSets & Deployments

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code: [../../session10-k8s-core-objects/](../../session10-k8s-core-objects/)

---

## Task 1: Core Objects

```bash
kubectl apply -f ../../session10-k8s-core-objects/pod/nginx-pod.yaml
kubectl apply -f ../../session10-k8s-core-objects/replicaset/backend-rs.yaml
kubectl apply -f ../../session10-k8s-core-objects/deployment/deployment-v1.yaml
kubectl apply -f ../../session10-k8s-core-objects/daemonset/node-agent-ds.yaml
kubectl get pods,rs,deployment,daemonset
```

📸 screenshots/core-objects.png

---

## Task 2: Pod Lifecycle (12 states)

```bash
cd ../../session10-k8s-core-objects/pod-lifecycle
kubectl apply -f 01-running.yaml -f 02-pending.yaml -f 04-failed.yaml \
  -f 05-crashloopbackoff.yaml -f 06-imagepullbackoff.yaml
kubectl get pods -w
```

| State | Cause |
|---|---|
| Running | Container started successfully |
| Pending | Waiting for scheduling or image pull |
| Succeeded | Container exited with code 0 |
| Failed | Container exited with non-zero code |
| CrashLoopBackOff | Container keeps crashing — exponential backoff |
| ImagePullBackOff | Image doesn't exist or registry unreachable |

📸 screenshots/pod-lifecycle.png

---

## Task 3: Rolling Update

```bash
kubectl apply -f ../../session10-k8s-core-objects/01-rolling-update/deployment-v1.yaml
kubectl apply -f ../../session10-k8s-core-objects/01-rolling-update/service.yaml
kubectl apply -f ../../session10-k8s-core-objects/01-rolling-update/deployment-v2.yaml
kubectl rollout status deployment/app-rolling
kubectl get pods -l app=app-rolling --show-labels -w
kubectl rollout history deployment/app-rolling
kubectl rollout undo deployment/app-rolling
```

📸 screenshots/rolling-update.png

---

## Task 4: Blue-Green Deployment

```bash
kubectl apply -f ../../session10-k8s-core-objects/02-blue-green/deployment-blue.yaml
kubectl apply -f ../../session10-k8s-core-objects/02-blue-green/deployment-green.yaml
kubectl apply -f ../../session10-k8s-core-objects/02-blue-green/service-blue.yaml
kubectl describe svc myapp-service | grep Selector   # slot=blue
kubectl apply -f ../../session10-k8s-core-objects/02-blue-green/service-green.yaml
kubectl describe svc myapp-service | grep Selector   # slot=green
```

📸 screenshots/blue-green.png

---

## Task 5: Canary Deployment

```bash
kubectl apply -f ../../session10-k8s-core-objects/03-canary/deployment-stable.yaml
kubectl apply -f ../../session10-k8s-core-objects/03-canary/deployment-canary.yaml
kubectl apply -f ../../session10-k8s-core-objects/03-canary/service.yaml
kubectl scale deployment app-stable --replicas=7
kubectl scale deployment app-canary --replicas=3
kubectl get pods --show-labels
```

📸 screenshots/canary.png

---

## Task 6: Recreate Deployment

```bash
kubectl apply -f ../../session10-k8s-core-objects/04-recreate/deployment-v1.yaml
kubectl apply -f ../../session10-k8s-core-objects/04-recreate/deployment-v2.yaml
kubectl get pods -l app=app-recreate -w
# All v1 pods terminate BEFORE any v2 pod starts — brief downtime
```

📸 screenshots/recreate.png

---

## Task 7: Troubleshooting

```bash
kubectl apply -f ../../session10-k8s-core-objects/troubleshooting/broken-image.yaml
kubectl get pods                                      # ImagePullBackOff
kubectl describe pod <pod-name> | grep -A5 Events

kubectl apply -f ../../session10-k8s-core-objects/troubleshooting/selector-mismatch.yaml
kubectl get endpoints selector-error-demo             # empty
```

📸 screenshots/troubleshooting.png

---

## Deployment Strategy Comparison

| Strategy | Downtime | Rollback Speed | Use Case |
|---|---|---|---|
| RollingUpdate | None | Fast | Default — most apps |
| Recreate | Brief | Fast | Apps that can't run two versions |
| Blue-Green | None | Instant | High-traffic production |
| Canary | None | Instant | Risk-controlled rollout |

---

## Resources

- https://github.com/Nency-Ravaliya/Kubernetes
- https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
