# Session 11 — Kubernetes Networking & Services

## Student Details

- **Name:** Shifa
- **Enrollment Number:** 24BCS10354
- **Email:** shifa.24bcs10354@sst.scaler.com

---

## Homework Tasks

| Task | Description | Status |
|---|---|---|
| 1 | ClusterIP — internal-only service | ✅ |
| 2 | NodePort — external access via node IP | ✅ |
| 3 | LoadBalancer — cloud-provisioned external LB | ✅ |
| 4 | ExternalName — DNS alias to an external host | ✅ |
| 5 | Headless Service — direct per-pod DNS | ✅ |
| 6 | FQDN / CoreDNS resolution test | ✅ |

---

## Folder Guide

| Folder | Service Type |
|---|---|
| `01-clusterip/` | ClusterIP |
| `02-nodeport/` | NodePort |
| `03-loadbalancer/` | LoadBalancer |
| `04-externalname/` | ExternalName |
| `05-headless/` | Headless (clusterIP: None) |
| `dns-test/` | Pod used to test in-cluster DNS |
| `troubleshooting/` | Empty-endpoints (selector mismatch) |

Concept deep-dives: `service.md` (all 5 service types) and `fqdn.md` (CoreDNS/FQDN).

---

## Overview

Pods are ephemeral. When a Pod crashes, updates, or scales, it is replaced with a new Pod that receives a **brand-new, unpredictable IP address**. If microservices communicated by hardcoding Pod IPs, every restart would trigger a cascading outage.

A **Kubernetes Service** provides a stable virtual IP address (ClusterIP) and a permanent DNS name that never changes, dynamically load-balancing traffic across all healthy backend Pods.

---

## 1. ClusterIP

```bash
kubectl apply -f 01-clusterip/app-deployment.yaml
kubectl apply -f 01-clusterip/service.yaml
kubectl apply -f 01-clusterip/client-pod.yaml
kubectl exec -it curl-client -- curl web-service-clusterip:8080
```

---

## 2. NodePort

```bash
kubectl apply -f 02-nodeport/app-deployment.yaml
kubectl apply -f 02-nodeport/service.yaml
kubectl get svc web-service-nodeport
curl http://$(minikube ip):30080
```

---

## 3. LoadBalancer

```bash
kubectl apply -f 03-loadbalancer/app-deployment.yaml
kubectl apply -f 03-loadbalancer/service.yaml
kubectl get svc web-service-loadbalancer
minikube tunnel        # run in a separate terminal to assign an EXTERNAL-IP
```

---

## 4. ExternalName

```bash
kubectl apply -f 04-externalname/service.yaml
kubectl apply -f 04-externalname/client-pod.yaml
kubectl exec -it dns-test-client -- nslookup external-database-service
```

---

## 5. Headless Service

```bash
kubectl apply -f 05-headless/app-statefulset.yaml
kubectl apply -f 05-headless/service.yaml
kubectl apply -f 05-headless/client-pod.yaml
kubectl exec -it headless-dns-client -- nslookup web-service-headless
```

---

## 6. FQDN / DNS Test

```bash
kubectl apply -f dns-test/curl-test-pod.yaml
kubectl exec -it curl-test-pod -- cat /etc/resolv.conf
kubectl exec -it curl-test-pod -- nslookup web-service-clusterip.default.svc.cluster.local
```

---

## 7. Troubleshooting

```bash
kubectl apply -f troubleshooting/empty-endpoints.yaml
kubectl get endpoints broken-backend-service     # empty — selector matches no pod
kubectl describe svc broken-backend-service
kubectl delete -f troubleshooting/empty-endpoints.yaml
```

---

## Resources & Revision

- [Kubernetes Service Documentation](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kubernetes DNS Pod & Service](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
