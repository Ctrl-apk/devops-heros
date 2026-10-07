# Task 4: CoreDNS in Kubernetes

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## What is CoreDNS?

**CoreDNS** is a flexible, extensible DNS server written in Go. In Kubernetes (since v1.13), CoreDNS is the default cluster DNS server responsible for internal name resolution and service discovery.

CoreDNS runs as a deployment in the `kube-system` namespace exposed via a ClusterIP service named `kube-dns`.

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

---

## Why Kubernetes Uses CoreDNS

1. **Automatic Service Discovery:** CoreDNS dynamically watches the Kubernetes API for Service and Pod lifecycle events and updates DNS records in real time.
2. **Decoupled Architecture:** Pods connect to services using static domain names rather than volatile ephemeral pod IPs.
3. **Pluggable Architecture:** Supports custom plugins for logging, caching, metrics (Prometheus integration), and upstream DNS forwarding.

---

## How Service Discovery Works

1. A developer creates a Service `backend` in namespace `default`.
2. CoreDNS registers `backend.default.svc.cluster.local` pointing to the assigned `ClusterIP` (e.g., `10.96.45.12`).
3. When any Pod queries `backend`, CoreDNS returns `10.96.45.12`.
4. Kube-proxy load balances packets arriving at `10.96.45.12` to healthy backend Pods.

---

## How DNS Queries are Resolved inside a Pod

Inside every Kubernetes Pod, `/etc/resolv.conf` is automatically configured:

```ini
nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

- `nameserver 10.96.0.10`: The IP address of the `kube-dns` Service.
- `search`: The list of domain suffixes tested automatically for short names.
- `ndots:5`: Specifies that names with fewer than 5 dots are checked against search paths first.

---

## CoreDNS Configuration (Corefile)

CoreDNS is configured via a ConfigMap named `coredns` in `kube-system`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

---

## How to Troubleshoot DNS Issues

1. **Test DNS resolution using a utility pod:**
   ```bash
   kubectl run dns-test --rm -it --image=busybox:1.28 -- nslookup kubernetes.default
   ```

2. **Check CoreDNS Pod status:**
   ```bash
   kubectl get pods -n kube-system -l k8s-app=kube-dns
   ```

3. **Check CoreDNS logs:**
   ```bash
   kubectl logs -n kube-system -l k8s-app=kube-dns
   ```

4. **Verify `/etc/resolv.conf` in failing container:**
   ```bash
   kubectl exec -it <pod-name> -- cat /etc/resolv.conf
   ```
