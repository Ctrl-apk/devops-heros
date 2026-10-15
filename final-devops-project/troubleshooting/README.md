# Troubleshooting Labs & Post-Mortem Guide

This directory contains deliberately broken manifests designed to practice real-world Kubernetes incident response and troubleshooting workflows.

---

## Lab 1: ImagePullBackOff / ErrImagePull

### Scenario
A deployment was rolled out with a typo or missing tag in the container image specification.

### Apply the broken manifest
```bash
kubectl apply -f troubleshooting/broken-image.yaml
```

### Symptoms & Investigation Steps
1. **Inspect Pod status:**
   ```bash
   kubectl get pods -n taskboard -l app=broken-image
   ```
   *Observed status:* `ImagePullBackOff` or `ErrImagePull`.

2. **Describe the failing Pod:**
   ```bash
   kubectl describe pod -n taskboard -l app=broken-image
   ```
   *Look at the Events section at the bottom:*
   ```text
   Events:
     Type     Reason   Age                From               Message
     ----     ------   ----               ----               -------
     Normal   Scheduled 45s               default-scheduler  Successfully assigned taskboard/taskboard-broken-image-xxx to node-1
     Normal   Pulling   12s (x3 over 44s) kubelet            Pulling image "ghcr.io/example/taskboard-backend:does-not-exist"
     Warning  Failed    10s (x3 over 42s) kubelet            Failed to pull image "ghcr.io/example/taskboard-backend:does-not-exist": rpc error: code = NotFound
     Warning  Failed    10s (x3 over 42s) kubelet            Error: ErrImagePull
     Normal   BackOff   2s (x4 over 40s)  kubelet            Back-off pulling image "ghcr.io/example/taskboard-backend:does-not-exist"
   ```

3. **Root Cause:**
   The image tag `does-not-exist` does not exist in GHCR, or the cluster lacks image pull secrets for private repositories.

4. **Remediation:**
   Update the deployment container image to a valid published tag (e.g. Git commit SHA or valid version):
   ```bash
   kubectl set image deployment/taskboard-broken-image \
     backend=ghcr.io/ctrl-apk/taskboard-backend:latest -n taskboard
   ```

5. **Clean up:**
   ```bash
   kubectl delete -f troubleshooting/broken-image.yaml
   ```

---

## Lab 2: Service Routing Failure (Empty Endpoints)

### Scenario
Traffic sent to a Kubernetes Service fails to reach any Pods (HTTP 502/503 or connection timeout), even though backend Pods are healthy and running.

### Apply the broken manifest
```bash
kubectl apply -f troubleshooting/broken-service.yaml
```

### Symptoms & Investigation Steps
1. **Inspect the Service and its Endpoints:**
   ```bash
   kubectl get svc taskboard-broken-svc -n taskboard
   kubectl get endpoints taskboard-broken-svc -n taskboard
   ```
   *Observed output:*
   ```text
   NAME                   ENDPOINTS   AGE
   taskboard-broken-svc   <none>      30s
   ```
   Notice that `ENDPOINTS` is `<none>`!

2. **Compare Service selector with running Pod labels:**
   *Inspect Service selector:*
   ```bash
   kubectl get svc taskboard-broken-svc -n taskboard -o jsonpath='{.spec.selector}'
   # Output: {"app":"wrong-label"}
   ```

   *Inspect actual running backend Pod labels:*
   ```bash
   kubectl get pods -n taskboard --show-labels
   # Output: app=taskboard-backend, release=taskboard...
   ```

3. **Root Cause:**
   A Service uses `spec.selector` to dynamically select Pods and register their IP addresses into an `Endpoints` object. The selector `app: wrong-label` matches zero Pods in the namespace, resulting in an empty endpoint list and broken routing.

4. **Remediation:**
   Patch the Service selector to match the actual Pod label:
   ```bash
   kubectl patch svc taskboard-broken-svc -n taskboard \
     -p '{"spec":{"selector":{"app":"taskboard-backend"}}}'
   ```

   *Verify endpoints populated:*
   ```bash
   kubectl get endpoints taskboard-broken-svc -n taskboard
   # Output: 10.244.1.12:8000, 10.244.2.15:8000
   ```

5. **Clean up:**
   ```bash
   kubectl delete -f troubleshooting/broken-service.yaml
   ```
