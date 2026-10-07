# 11 — Kubernetes Networking & Services

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code: [../../session-11-kubernetes-services/](../../session-11-kubernetes-services/)

---

## 📌 Sub-Tasks & Deliverables

- **Task 1:** 5 Service Types Hands-on (ClusterIP, NodePort, LoadBalancer, ExternalName, Headless)
- **Task 2:** Kubernetes Object Comparison (Deployment vs ReplicaSet, Deployment vs DaemonSet vs StatefulSet, ReplicaSet vs Service)
- **Task 3:** [FQDN Documentation](./fqdn/README.md)
- **Task 4:** [CoreDNS Documentation](./coredns/README.md)

---

## The 5 Service Types

| Type | Scope | Use Case |
|---|---|---|
| ClusterIP | Internal only | Microservice-to-microservice communication |
| NodePort | External via node IP | Dev/testing external access |
| LoadBalancer | External via cloud LB | Production external access |
| ExternalName | DNS alias | Pointing to external services |
| Headless | Direct pod DNS | StatefulSets, databases |

---

## Task 1: 5 Service Types Hands-on

### 1. ClusterIP
Internal service — only reachable from within the cluster.

```bash
kubectl apply -f ../../session-11-kubernetes-services/01-clusterip/app-deployment.yaml
kubectl apply -f ../../session-11-kubernetes-services/01-clusterip/service.yaml
kubectl apply -f ../../session-11-kubernetes-services/01-clusterip/client-pod.yaml
kubectl get svc web-service-clusterip
kubectl get endpoints web-service-clusterip
kubectl exec -it curl-client -- curl web-service-clusterip:8080
```

### 2. NodePort
Opens a port on every node (30000–32767) for external access.

```bash
kubectl apply -f ../../session-11-kubernetes-services/02-nodeport/app-deployment.yaml
kubectl apply -f ../../session-11-kubernetes-services/02-nodeport/service.yaml
kubectl get svc web-service-nodeport
curl http://$(minikube ip):30080
```

### 3. LoadBalancer
Cloud provider assigns an external IP. `minikube tunnel` simulates this locally.

```bash
kubectl apply -f ../../session-11-kubernetes-services/03-loadbalancer/app-deployment.yaml
kubectl apply -f ../../session-11-kubernetes-services/03-loadbalancer/service.yaml
kubectl get svc web-service-loadbalancer
minikube tunnel
```

### 4. ExternalName
Pure DNS CNAME alias — no endpoints, no cluster IP. Routes to external domain.

```bash
kubectl apply -f ../../session-11-kubernetes-services/04-externalname/service.yaml
kubectl apply -f ../../session-11-kubernetes-services/04-externalname/client-pod.yaml
kubectl get svc external-database-service
kubectl exec -it dns-test-client -- nslookup external-database-service
```

### 5. Headless Service
`clusterIP: None` — CoreDNS returns all pod IPs directly instead of a single VIP. Used with StatefulSets.

```bash
kubectl apply -f ../../session-11-kubernetes-services/05-headless/service.yaml
kubectl apply -f ../../session-11-kubernetes-services/05-headless/app-statefulset.yaml
kubectl apply -f ../../session-11-kubernetes-services/05-headless/client-pod.yaml
kubectl get svc web-service-headless
kubectl exec -it headless-dns-client -- nslookup web-service-headless
```

---

## Task 2: Kubernetes Object Comparison

### 1. Deployment vs ReplicaSet

| Feature | ReplicaSet | Deployment |
|---|---|---|
| **Purpose** | Ensures a fixed number of identical Pods are running at any given time | Higher-level abstraction managing ReplicaSets declaratively with rolling updates & rollbacks |
| **Pod Management** | Manages raw Pod instances based on label selectors | Manages underlying ReplicaSets (creates new RS and scales down old RS during updates) |
| **Scaling** | Supports manual scaling (`kubectl scale rs ...`) | Supports manual and automatic scaling (via HPA) |
| **Rolling Updates** | ❌ No native support (must delete Pods manually) | ✅ Native rolling updates and rollback support (`kubectl rollout undo`) |
| **Relationship** | Direct owner of Pods | Deployment owns and manages ReplicaSets; ReplicaSet owns Pods |

### 2. Deployment vs DaemonSet vs StatefulSet

| Dimension | Deployment | DaemonSet | StatefulSet |
|---|---|---|---|
| **Use Cases** | Stateless microservices, web apps | Node agents, log collectors (Fluentd), monitoring agents (Prometheus Node Exporter) | Stateful applications (Databases, Kafka, Redis, ZooKeeper) |
| **Pod Creation** | Randomly named pods (`web-7f89d-x9q4t`) | Exactly 1 pod per node automatically | Deterministic, ordinal pod names (`db-0`, `db-1`, `db-2`) |
| **Scaling** | Arbitrary replica count across cluster | Scales dynamically with node count (1 per node) | Sequential, ordered scaling (0 → 1 → 2) |
| **Networking** | Shared ClusterIP/Service VIP | Node-level network access | Unique per-pod network identity via Headless Service |
| **Storage** | Ephemeral or shared volume | Node-local hostPath storage | Dedicated, persistent per-pod volume claims (`volumeClaimTemplates`) |
| **Examples** | `nginx`, `flask-api`, `react-ui` | `kube-proxy`, `calico-node`, `promtail` | `postgres`, `mongodb-cluster`, `elastic-node-0` |

### 3. ReplicaSet vs Service

| Dimension | ReplicaSet | Service |
|---|---|---|
| **Responsibility** | Maintains desired Pod replica count & pod health lifecycle | Provides stable networking entry point (VIP/DNS) and load-balancing |
| **Why Required?** | Prevents pod outages by recreating crashed/terminated pods | Decouples volatile pod IPs from client microservices |
| **Traffic Flow** | Does NOT route or load-balance traffic | Intercepts traffic at virtual IP/Port and forwards to healthy pod IPs matching selector |

---

## Task 3 & 4 Summary

- **FQDN Details:** Documented in [fqdn/README.md](./fqdn/README.md)
- **CoreDNS Details:** Documented in [coredns/README.md](./coredns/README.md)

---

## Resources

- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [CoreDNS / DNS for Services](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
