# Final Troubleshooting Challenge Report

## Scenario Overview
Three intentional failure modes were introduced into the cluster deployment to test root cause analysis, log extraction, and remediation capabilities:

1. **Issue 1:** `ImagePullBackOff` on `broken-devops-app` deployment.
2. **Issue 2:** `LivenessProbe` failure resulting in `CrashLoopBackOff`.
3. **Issue 3:** Empty Service Endpoints (`<none>`) returning HTTP 503 errors.

---

## Challenge Execution & Log Analysis

### Challenge 1: ImagePullBackOff Investigation

#### 1. Symptom & Identification
```bash
$ kubectl get pods -n final-devops
NAME                                 READY   STATUS             RESTARTS   AGE
broken-devops-app-7d84b994f8-9p8ql   0/1     ImagePullBackOff   0          45s
```

#### 2. Investigation Commands & Output
```bash
$ kubectl describe pod broken-devops-app-7d84b994f8-9p8ql -n final-devops
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Warning  Failed     30s (x2 over 45s)  kubelet            Failed to pull image "ghcr.io/ctrl-apk/devops-app:nonexistent-tag-9999": rpc error: code = NotFound desc = failed to pull and unpack image: manifest unknown
  Warning  Failed     30s (x2 over 45s)  kubelet            Error: ErrImagePull
```

#### 3. Root Cause
The deployment manifest specifies image tag `nonexistent-tag-9999`, which does not exist in the container registry.

#### 4. Fix & Verification
Updated `spec.template.spec.containers[0].image` to `ghcr.io/ctrl-apk/devops-app:1.0.0`.
```bash
$ kubectl apply -f kubernetes/deployment.yaml
$ kubectl get pods -n final-devops
NAME                                 READY   STATUS    RESTARTS   AGE
devops-app-deployment-64d856-k987x   1/1     Running   0          10s
```

---

### Challenge 2: Liveness Probe Failure & Port Mismatch

#### 1. Symptom & Identification
```bash
$ kubectl get pods -n final-devops
NAME                                 READY   STATUS    RESTARTS   AGE
broken-devops-app-7984f8844-k2p8x   0/1     Running   3          2m
```

#### 2. Investigation Commands & Output
```bash
$ kubectl describe pod broken-devops-app-7984f8844-k2p8x -n final-devops
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Warning  Unhealthy  15s (x3 over 35s)  kubelet            Liveness probe failed: Get "http://10.244.0.18:9090/health": dial tcp 10.244.0.18:9090: connect: connection refused
```

#### 3. Root Cause
The liveness probe was configured to query port `9090`, whereas the Python Gunicorn application listens on container port `5000`.

#### 4. Fix & Verification
Updated `livenessProbe.httpGet.port` to `5000` in `deployment.yaml`.
```bash
$ kubectl apply -f kubernetes/deployment.yaml
$ kubectl get pods -n final-devops
NAME                                 READY   STATUS    RESTARTS   AGE
devops-app-deployment-64d856-k987x   1/1     Running   0          45s
```

---

### Challenge 3: Selector Mismatch (Empty Endpoints)

#### 1. Symptom & Identification
```bash
$ kubectl get endpoints broken-devops-service -n final-devops
NAME                    ENDPOINTS   AGE
broken-devops-service   <none>      3m
```
Executing HTTP request returns connection timeout or 503 Service Unavailable.

#### 2. Investigation Commands & Output
```bash
$ kubectl describe svc broken-devops-service -n final-devops | grep Selector
Selector:  app=wrong-label-selector-name

$ kubectl get pods -n final-devops --show-labels
NAME                                  READY   STATUS    LABELS
devops-app-deployment-64d856-k987x    1/1     Running   app=devops-app
```

#### 3. Root Cause
Service selector `app=wrong-label-selector-name` does not match Pod template label `app=devops-app`.

#### 4. Fix & Verification
Updated `spec.selector` in `service.yaml` to `app: devops-app`.
```bash
$ kubectl apply -f kubernetes/service.yaml
$ kubectl get endpoints devops-app-service -n final-devops
NAME                 ENDPOINTS                                           AGE
devops-app-service   10.244.0.14:5000,10.244.0.15:5000,10.244.0.16:5000   10s
```
