# 13 — Kubernetes Troubleshooting

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and scenarios: [../../session-14-kubernetes-troubleshooting/](../../session-14-kubernetes-troubleshooting/)

---

## Task 1: Essential Kubernetes Troubleshooting Commands

| Command | Purpose / Use Case | Example |
|---|---|---|
| `kubectl get` | List resource status across cluster or namespace | `kubectl get pods -n default` |
| `kubectl describe` | Inspect detailed events, conditions, volume mounts, and status | `kubectl describe pod web-pod` |
| `kubectl logs` | View container stderr/stdout application logs | `kubectl logs web-pod -c app-container --tail=50` |
| `kubectl exec` | Execute interactive debugging command inside a container | `kubectl exec -it web-pod -- sh` |
| `kubectl events` | Stream cluster-wide events (warnings, errors, scheduling failures) | `kubectl get events --sort-by='.metadata.creationTimestamp'` |
| `kubectl explain` | Read documentation and field specs directly from terminal | `kubectl explain pod.spec.containers.livenessProbe` |
| `kubectl top` | View CPU and Memory consumption per node or pod | `kubectl top pods` |
| `kubectl get -o wide` | View extended info (Pod IP, Host Node Name, Nominated Node) | `kubectl get pods -o wide` |

---

## Task 2: Troubleshooting Common Kubernetes Issues

### 1. CrashLoopBackOff
- **Problem Statement:** Pod starts, fails/crashes, and Kubernetes keeps restarting it with exponential backoff delay.
- **Investigation Steps:**
  1. `kubectl get pod crash-pod` -> Status `CrashLoopBackOff`
  2. `kubectl logs crash-pod --previous` -> Check previous crashed container logs
  3. `kubectl describe pod crash-pod` -> Check exit code (e.g., Exit Code 1 or 137 OOMKilled)
- **Root Cause:** Missing environment variable, application code panic, or OOMKilled (out of memory).
- **Solution & Fix:** Pass correct ConfigMap/Secret environment variables or adjust memory request/limit in pod YAML.
- **Verification:** `kubectl get pod crash-pod` -> Status `Running` (RESTARTS stops incrementing).

### 2. ImagePullBackOff / ErrImagePull
- **Problem Statement:** Kubernetes cannot pull the container image specified in the pod manifest.
- **Investigation Steps:**
  1. `kubectl get pod img-pod` -> Status `ErrImagePull` / `ImagePullBackOff`
  2. `kubectl describe pod img-pod` -> Inspect `Events:` section at bottom
- **Root Cause:** Typo in image name/tag (`nginx:1.99999`) or private image registry lacking `imagePullSecrets`.
- **Solution & Fix:** Correct image tag in manifest or create docker-registry secret and link to `imagePullSecrets`.
- **Verification:** `kubectl apply -f pod.yaml` -> `Events: Successfully pulled image`.

### 3. Pending Pods
- **Problem Statement:** Pod remains in `Pending` state and is never scheduled onto any node.
- **Investigation Steps:**
  1. `kubectl get pods` -> Status `Pending`
  2. `kubectl describe pod pending-pod` -> Look at `Events:` for scheduler messages
- **Root Cause:** Insufficient CPU/Memory on cluster nodes (`0/3 nodes are available: insufficient cpu`), or unmet `nodeSelector` / `taint` / `toleration`.
- **Solution & Fix:** Reduce resource requests or scale up cluster nodes.
- **Verification:** `kubectl get pods -o wide` -> Assigned to node, status `Running`.

### 4. ContainerCreating
- **Problem Statement:** Container stuck in `ContainerCreating` state.
- **Investigation Steps:**
  1. `kubectl describe pod cc-pod`
- **Root Cause:** CNI network plugin issue or PVC failed to attach/mount to node (`Volume load failed`).
- **Solution & Fix:** Verify CNI pod health (`kube-flannel` / `calico`) and ensure PVC storage provider is active.

### 5. Service Connectivity & DNS Issues
- **Problem Statement:** Pod A cannot talk to Service B (`curl: (6) Could not resolve host`).
- **Investigation Steps:**
  1. Test DNS: `kubectl run tmp --rm -it --image=busybox:1.28 -- nslookup service-b`
  2. Check Service endpoints: `kubectl get endpoints service-b`
- **Root Cause:** Service `selector` labels do not match Deployment template `labels`, resulting in 0 active endpoints.
- **Solution & Fix:** Align labels in Service and Deployment manifests.

---

## Task 3: Session 14 Mini Project — Debugging Broken Deployment

### Problem Statement
A critical deployment `broken-app` is stuck in `CrashLoopBackOff` and its service `broken-service` returns `503 Service Unavailable`.

### Investigation Steps & Log Outputs

```bash
# Step 1: Check Pod Status
$ kubectl get pods
NAME                         READY   STATUS             RESTARTS   AGE
broken-app-6c9b5d7d9-4kx2p   0/1     CrashLoopBackOff   4          2m

# Step 2: Read Container Logs
$ kubectl logs broken-app-6c9b5d7d9-4kx2p
Error: DATABASE_URL environment variable is missing!
Fatal application exit code 1.

# Step 3: Check Service Endpoints
$ kubectl get endpoints broken-service
NAME             ENDPOINTS   AGE
broken-service   <none>      5m
```

### Root Cause Analysis
1. Application crashed because `DATABASE_URL` env variable was omitted from `deployment.yaml`.
2. Service selector was set to `app: web` while Deployment pod label was `app: broken-web`, leaving endpoints empty.

### Fixed Manifests & Solution

```yaml
# deployment.yaml (Fixed)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: broken-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: app
        image: nginx:alpine
        env:
        - name: DATABASE_URL
          value: "postgres://db:5432/production"
```

### Verification Output

```bash
$ kubectl apply -f deployment.yaml -f service.yaml

$ kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
broken-app-7984f8844-9pxz1   1/1     Running   0          12s

$ kubectl get endpoints broken-service
NAME             ENDPOINTS          AGE
broken-service   10.244.0.15:8080   6m
```
