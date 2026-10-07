# Task 3: Kubernetes FQDN (Fully Qualified Domain Name)

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## What is an FQDN?

In Kubernetes, **FQDN** stands for **Fully Qualified Domain Name**. It is the absolute, complete domain address assigned to an internal Kubernetes resource (such as a Service or StatefulSet Pod).

While short names (`backend`) only work within the same namespace, an FQDN provides an unambiguous address that can be resolved from **any namespace** inside the cluster.

---

## Kubernetes Service DNS Naming Convention

Every Service in a Kubernetes cluster gets an official FQDN formatted as follows:

```text
<service-name>.<namespace>.svc.cluster.local
```

### Breakdown of FQDN Segments

| Segment | Description | Example |
| :--- | :--- | :--- |
| `<service-name>` | The name defined in `metadata.name` of the Service | `payment-service` |
| `<namespace>` | The namespace where the Service is deployed | `production` |
| `svc` | Indicates that the resource type is a Service | `svc` |
| `cluster.local` | The default base domain of the Kubernetes cluster | `cluster.local` |

**Full Example:** `payment-service.production.svc.cluster.local`

---

## Namespace-Based DNS Resolution

### 1. Pods in the SAME Namespace
When `frontend` and `backend` are both in namespace `production`:
```bash
curl http://backend
```
- Linux appends `production.svc.cluster.local` automatically via `/etc/resolv.conf`.

### 2. Pods in DIFFERENT Namespaces
When a test runner in namespace `dev` wants to connect to `backend` in namespace `production`:
```bash
# Option 1: Service + Namespace
curl http://backend.production

# Option 2: Full FQDN
curl http://backend.production.svc.cluster.local
```

---

## Pod-to-Service Communication

```text
[ Pod A (Namespace: dev) ] ─── curl http://backend.production ───► [ CoreDNS (10.96.0.10) ]
                                                                             │
[ Pod A ] ◄── Resolves IP: 10.96.200.55 (Service ClusterIP) ─────────────────┘
    │
    └─── HTTP Request ───► [ Kube-Proxy ] ───► [ Pod B (Backend in production) ]
```

---

## Examples of Kubernetes FQDNs

1. **Standard ClusterIP Service:**
   `mysql.database.svc.cluster.local`
2. **NodePort / LoadBalancer Service:**
   `web-frontend.default.svc.cluster.local`
3. **Headless Service Pod (StatefulSet):**
   `kafka-0.kafka-headless.prod.svc.cluster.local`
4. **Pod IP FQDN:**
   `10-244-1-15.default.pod.cluster.local`
