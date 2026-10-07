# 12 — Kubernetes Storage, HPA & Probes

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and manifests: [../../session-13-storage-hpa-probes/](../../session-13-storage-hpa-probes/)

---

## 📌 Tasks Summary

- **Task 1:** [Kubernetes Volumes Documentation](./01-kubernetes-volumes/README.md) (`emptyDir`, `hostPath`, `PV`, `PVC`, `StorageClass`, Dynamic Provisioning)
- **Task 2:** HPA Hands-on Demo & Load Testing
- **Task 3:** Session 13 Mini Project (Stateful + Auto-scaling Application)

---

## Task 2: HPA Hands-on Demo

### 1. Application & HPA Manifest (`hpa.yaml`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hpa-demo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hpa-demo
  template:
    metadata:
      labels:
        app: hpa-demo
    spec:
      containers:
      - name: php-apache
        image: registry.k8s.io/hpa-example
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: 500m
          requests:
            cpu: 200m
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-demo-autoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hpa-demo-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

### 2. Execution Commands & Verification

```bash
# 1. Apply deployment and HPA
kubectl apply -f hpa.yaml

# 2. Verify HPA status
kubectl get hpa
```

### 3. Load Generator Command
Run a load generator pod in a busy loop:

```bash
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://hpa-demo-app; done"
```

### 4. Observed Auto-scaling Output

```text
$ kubectl get hpa --watch
NAME                  REFERENCE                 TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo-autoscaler   Deployment/hpa-demo-app   0%/50%     1         10        1          30s
hpa-demo-autoscaler   Deployment/hpa-demo-app   120%/50%   1         10        1          60s
hpa-demo-autoscaler   Deployment/hpa-demo-app   120%/50%   1         10        3          90s
hpa-demo-autoscaler   Deployment/hpa-demo-app   80%/50%    1         10        5          2m

$ kubectl get pods
NAME                            READY   STATUS    RESTARTS   AGE
hpa-demo-app-75675f5897-4m8qg   1/1     Running   0          3m
hpa-demo-app-75675f5897-8d2xk   1/1     Running   0          90s
hpa-demo-app-75675f5897-k92ls   1/1     Running   0          90s
hpa-demo-app-75675f5897-x71pq   1/1     Running   0          60s
hpa-demo-app-75675f5897-z90ab   1/1     Running   0          60s
```

---

## Task 3: Mini Project — Scalable Stateful Application

The mini project integrates:
1. Namespace isolation (`namespace.yaml`)
2. Persistent Storage Request (`pvc.yaml`)
3. Multi-replica Deployment with Liveness & Readiness Probes (`deployment.yaml`)
4. ClusterIP Service (`service.yaml`)
5. Horizontal Pod Autoscaler (`hpa.yaml`)

### Manifest Files:

#### `pvc.yaml`
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-pvc
  namespace: session13-demo
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

#### `deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: session13-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 250m
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: storage
          mountPath: /usr/share/nginx/html
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: app-pvc
```

#### `hpa.yaml`
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: session13-demo
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

---

## Useful Verification Commands

```bash
kubectl get hpa -n session13-demo
kubectl get pods -n session13-demo
kubectl top pods -n session13-demo
kubectl describe hpa web-app-hpa -n session13-demo
```
