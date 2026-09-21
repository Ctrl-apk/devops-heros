# 11 — Kubernetes Networking & Services

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code: [../../session-11-kubernetes-services/](../../session-11-kubernetes-services/)

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

## Task 1: ClusterIP

Internal service — only reachable from within the cluster.

```bash
kubectl apply -f ../../session-11-kubernetes-services/01-clusterip/app-deployment.yaml
kubectl apply -f ../../session-11-kubernetes-services/01-clusterip/service.yaml
kubectl apply -f ../../session-11-kubernetes-services/01-clusterip/client-pod.yaml
kubectl get svc web-service-clusterip
kubectl get endpoints web-service-clusterip
kubectl exec -it curl-client -- curl web-service-clusterip:8080
```

📸 screenshots/clusterip.png

> *Screenshot to be added after running the commands*

---

## Task 2: NodePort

Opens a port on every node (30000–32767) for external access.

```bash
kubectl apply -f ../../session-11-kubernetes-services/02-nodeport/app-deployment.yaml
kubectl apply -f ../../session-11-kubernetes-services/02-nodeport/service.yaml
kubectl get svc web-service-nodeport
curl http://$(minikube ip):30080
```

📸 screenshots/nodeport.png

> *Screenshot to be added after running the commands*

---

## Task 3: LoadBalancer

Cloud provider assigns an external IP. `minikube tunnel` simulates this locally.

```bash
kubectl apply -f ../../session-11-kubernetes-services/03-loadbalancer/app-deployment.yaml
kubectl apply -f ../../session-11-kubernetes-services/03-loadbalancer/service.yaml
kubectl get svc web-service-loadbalancer   # shows <pending> without tunnel
minikube tunnel                            # run in separate terminal
kubectl get svc web-service-loadbalancer   # now shows EXTERNAL-IP
```

📸 screenshots/loadbalancer.png

> *Screenshot to be added after running the commands*

---

## Task 4: ExternalName

Pure DNS CNAME alias — no endpoints, no cluster IP. Routes to external domain.

```bash
kubectl apply -f ../../session-11-kubernetes-services/04-externalname/service.yaml
kubectl apply -f ../../session-11-kubernetes-services/04-externalname/client-pod.yaml
kubectl get svc external-database-service   # CLUSTER-IP: <none>
kubectl exec -it dns-test-client -- nslookup external-database-service
# Returns: canonical name = <external-domain>
```

📸 screenshots/externalname.png

> *Screenshot to be added after running the commands*

---

## Task 5: Headless Service

`clusterIP: None` — CoreDNS returns all pod IPs directly instead of a single VIP. Used with StatefulSets.

```bash
kubectl apply -f ../../session-11-kubernetes-services/05-headless/service.yaml
kubectl apply -f ../../session-11-kubernetes-services/05-headless/app-statefulset.yaml
kubectl apply -f ../../session-11-kubernetes-services/05-headless/client-pod.yaml
kubectl get svc web-service-headless   # CLUSTER-IP: None
kubectl exec -it headless-dns-client -- nslookup web-service-headless
# Returns 3 separate A records (one per pod IP)
kubectl exec -it headless-dns-client -- curl web-stateful-0.web-service-headless:80
```

📸 screenshots/headless.png

---

## Task 6: FQDN / CoreDNS

```bash
kubectl exec -it curl-test-pod -- cat /etc/resolv.conf
# nameserver 10.96.0.10
# search default.svc.cluster.local svc.cluster.local cluster.local
# options ndots:5

kubectl exec -it curl-test-pod -- nslookup web-service-clusterip.default.svc.cluster.local
```

Full FQDN format: `<service>.<namespace>.svc.cluster.local`

📸 screenshots/fqdn-dns-test.png

> *Screenshot to be added after running the commands*

---

## Task 7: Troubleshooting — Empty Endpoints

```bash
kubectl apply -f ../../session-11-kubernetes-services/troubleshooting/empty-endpoints.yaml
kubectl get endpoints broken-backend-service   # empty — selector matches no pod
kubectl describe svc broken-backend-service
```

**Cause:** Service selector label doesn't match any pod label.
**Fix:** Align `spec.selector` in the Service with `metadata.labels` in the Pod/Deployment.

📸 screenshots/troubleshooting.png

> *Screenshot to be added after running the commands*

---

## Resources

- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [CoreDNS / DNS for Services](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
