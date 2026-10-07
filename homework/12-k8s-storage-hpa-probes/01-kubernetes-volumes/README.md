# Task 1: Kubernetes Volumes & Storage

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## 1. Volume Types Overview

| Volume Type | Scope / Lifetime | Access Modes | Use Case |
|---|---|---|---|
| **`emptyDir`** | Tied to Pod lifecycle | Read/Write | Scratch space, cache, temp file processing |
| **`hostPath`** | Tied to Host Node filesystem | Read/Write | Node monitoring agents, daemonsets, single-node storage |
| **`PersistentVolume` (PV)** | Cluster-wide resource | ReadWriteOnce (RWO), ReadOnlyMany (ROX), ReadWriteMany (RWX) | Long-term persistent storage (Databases, State) |
| **`PersistentVolumeClaim` (PVC)** | Namespace request for PV | Depends on requested PV | Application request for storage |
| **`StorageClass`** | Storage provisioner configuration | Dynamic | Auto-provisioning storage on demand |

---

## 2. emptyDir Example

A temporary directory created when a Pod is assigned to a Node. Erased when Pod is removed.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-demo
spec:
  containers:
  - name: writer
    image: busybox
    command: ["sh", "-c", "echo 'Hello from emptyDir' > /cache/data.txt && sleep 3600"]
    volumeMounts:
    - name: cache-vol
      mountPath: /cache
  volumes:
  - name: cache-vol
    emptyDir: {}
```

---

## 3. hostPath Example

Mounts a file or directory from the host node's filesystem into the Pod container.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-demo
spec:
  containers:
  - name: log-reader
    image: busybox
    command: ["sh", "-c", "tail -f /host-logs/syslog"]
    volumeMounts:
    - name: node-logs
      mountPath: /host-logs
  volumes:
  - name: node-logs
    hostPath:
      path: /var/log
      type: Directory
```

---

## 4. PersistentVolume (PV) & PersistentVolumeClaim (PVC)

### PersistentVolume (`pv.yaml`)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-local-demo
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: "/data/pv-demo"
```

### PersistentVolumeClaim (`pvc.yaml`)
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-demo
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

---

## 5. StorageClass & Dynamic Provisioning

StorageClass defines the provisioner and parameters for dynamic volume creation without pre-provisioning PVs manually.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard-dynamic
provisioner: k8s.io/minikube-hostpath
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

When a PVC requests `storageClassName: standard-dynamic`, Kubernetes automatically provisions a matching PV on the fly!
