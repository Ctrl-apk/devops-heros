# 09 — Kubernetes Fundamentals

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full files: [../../session9-k8s/](../../session9-k8s/)

---

## Task 1: Minikube & kubectl Installation

```bash
# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
sudo snap install kubectl --classic

# Verify
minikube version
kubectl version --client
```

**Output:**
```
minikube version: v1.39.0
Client Version: v1.36.3
Kustomize Version: v5.8.1
```

---

## Task 2: Cluster Lifecycle

```bash
# Start cluster
minikube start --driver=docker

# Check status
minikube status

# Get nodes
kubectl get nodes -o wide

# Stop cluster
minikube stop
```

**minikube status output:**
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

---

## Task 3: Kubernetes Architecture

```
+─────────────────────── CONTROL PLANE ───────────────────────+
│                                                              │
│   etcd  ←→  kube-apiserver  ←→  kube-scheduler             │
│                    ↕                                         │
│          kube-controller-manager                             │
+──────────────────────────┬───────────────────────────────────+
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
+─── WORKER NODE 1 ───+    +─── WORKER NODE 2 ───+
│  kubelet            │    │  kubelet            │
│  kube-proxy         │    │  kube-proxy         │
│  containerd (CRI)   │    │  containerd (CRI)   │
│  Pod 1 | Pod 2      │    │  Pod 3 | Pod 4      │
+─────────────────────+    +─────────────────────+
```

### Control Plane Components

| Component | Role |
|---|---|
| `kube-apiserver` | Single entry point for all operations. Every `kubectl` command goes through it |
| `etcd` | Distributed key-value store holding entire cluster state |
| `kube-scheduler` | Assigns pods to nodes based on resource availability |
| `kube-controller-manager` | Runs control loops — ensures desired state matches actual state |

### Worker Node Components

| Component | Role |
|---|---|
| `kubelet` | Agent on every node. Receives PodSpecs and manages containers |
| `kube-proxy` | Manages network rules for service routing across pods |
| `containerd` | Container runtime — actually runs the containers |

---

## Resources

- [Kubernetes Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Minikube Docs](https://minikube.sigs.k8s.io/docs/start/)
