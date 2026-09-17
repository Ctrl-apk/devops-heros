# Session 12 — Kubernetes Ingress, ConfigMaps & Secrets

## Student Details

- **Name:** Shifa
- **Enrollment Number:** 24BCS10354
- **Email:** shifa.24bcs10354@sst.scaler.com

---

## Homework Tasks

| Task | Description | Status |
|---|---|---|
| 1 | ConfigMap — non-sensitive configuration decoupling | ✅ |
| 2 | ConfigMap live update & pod immobility verification | ✅ |
| 3 | Secrets — sensitive data isolation & Base64 mechanics | ✅ |
| 4 | Trailing newline secret gotcha analysis | ✅ |
| 5 | Enterprise secret management & pipeline integration | ✅ |
| 6 | Combined ConfigMap and Secret pod injection | ✅ |
| 7 | Ingress Resource vs Ingress Controller architecture | ✅ |
| 8 | NGINX Ingress Controller activation & verification | ✅ |
| 9 | Local DNS resolution & hosts file mapping | ✅ |
| 10 | Layer 7 path-based routing | ✅ |
| 11 | Virtual host-based routing (subdomain routing) | ✅ |
| 12 | Hybrid Ingress routing architecture | ✅ |
| 13 | Ingress TLS/HTTPS termination & Secret binding | ✅ |
| 14 | End-to-end multi-tier microservice integration | ✅ |

---

## Folder Guide

| Folder | Covers |
|---|---|
| `01-configmap/` | ConfigMap creation and injection |
| `02-secret/` | Kubernetes Secrets and Base64 |
| `03-ingress/` | Ingress with TLS and virtual hosts |
| `04-full-demo/` | Full end-to-end demo with all components |
| `troubleshooting/` | Common Ingress/ConfigMap issues |

---

## Task 1: ConfigMap

```bash
kubectl apply -f 01-configmap/app-config.yaml
kubectl get configmap yatri-app-config
kubectl describe configmap yatri-app-config
kubectl get configmap yatri-app-config -o jsonpath='{.data.ENVIRONMENT}' && echo ""
```

📸 screenshots/configmap.png

---

## Task 2: ConfigMap Live Update

```bash
kubectl patch configmap yatri-app-config --type merge -p '{"data":{"ENVIRONMENT":"staging"}}'
kubectl exec -it deploy/yatri-backend -- env | grep ENVIRONMENT
kubectl rollout restart deployment/yatri-backend
kubectl rollout status deployment/yatri-backend
kubectl exec -it deploy/yatri-backend -- env | grep ENVIRONMENT
```

📸 screenshots/configmap-update.png

---

## Task 3: Secrets

```bash
kubectl apply -f 02-secret/db-secret.yaml
kubectl get secret yatri-db-secret
kubectl describe secret yatri-db-secret
kubectl get secret yatri-db-secret -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 --decode && echo ""
```

📸 screenshots/secret.png

---

## Task 4: Trailing Newline Gotcha

```bash
# Wrong — appends newline byte 0x0a
echo "secretpassword" | base64

# Correct — no newline
echo -n "secretpassword" | base64
```

📸 screenshots/base64-newline.png

---

## Task 5: Enterprise Secret Management

External secret management flow:

```
AWS Secrets Manager / HashiCorp Vault
        │
        ▼
External Secrets Operator (ESO)
        │
        ▼
Kubernetes Secret (ephemeral, auto-rotated)
        │
        ▼
Pod Volume / Environment Variable
```

---

## Task 6: Combined ConfigMap + Secret Injection

```bash
kubectl apply -f 04-full-demo/configmap.yaml
kubectl apply -f 04-full-demo/secret.yaml
kubectl apply -f 04-full-demo/backend.yaml
kubectl rollout status deployment/yatri-backend
kubectl exec -it deploy/yatri-backend -- env | grep -E "ENVIRONMENT|LOG_LEVEL|POSTGRES|DEFAULT_CURRENCY"
```

📸 screenshots/combined-injection.png

---

## Task 7: Ingress Resource vs Ingress Controller

| Component | Role |
|---|---|
| **Ingress Resource** | Declarative Layer 7 routing rules (hostnames, paths, TLS). Does nothing by itself |
| **Ingress Controller** | Active reverse proxy (NGINX, Traefik) that reads Ingress rules and routes real traffic |

---

## Task 8: NGINX Ingress Controller

```bash
minikube addons enable ingress
kubectl get pods -n ingress-nginx
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

📸 screenshots/ingress-controller.png

---

## Task 9: Local DNS Setup

```bash
MINIKUBE_IP=$(minikube ip)
echo "${MINIKUBE_IP}  yatri.local" | sudo tee -a /etc/hosts
grep "yatri.local" /etc/hosts
```

📸 screenshots/hosts-dns.png

---

## Task 10: Path-Based Routing

```bash
kubectl apply -f 04-full-demo/frontend.yaml
kubectl apply -f 04-full-demo/backend.yaml
kubectl apply -f 04-full-demo/ingress.yaml
kubectl get ingress yatri-ingress
curl -s http://yatri.local/
curl -s http://yatri.local/api/
```

📸 screenshots/path-routing.png

---

## Task 11: Virtual Host Routing

```bash
echo "${MINIKUBE_IP}  portal.campus.local api.campus.local" | sudo tee -a /etc/hosts
curl -s -H "Host: portal.campus.local" http://${MINIKUBE_IP}/
curl -s -H "Host: api.campus.local" http://${MINIKUBE_IP}/api/
```

📸 screenshots/vhost-routing.png

---

## Task 12: Hybrid Ingress Routing

```bash
kubectl apply -f 03-ingress/ingress-tls.yaml
kubectl get ingress campus-ingress-tls
kubectl describe ingress campus-ingress-tls
```

📸 screenshots/hybrid-routing.png

---

## Task 13: TLS/HTTPS Termination

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=campus.local/O=CampusDevOps"

kubectl create secret tls campus-tls-cert --cert=tls.crt --key=tls.key
kubectl apply -f 03-ingress/ingress-tls.yaml

INGRESS_IP=$(minikube ip)
curl -k -v --resolve portal.campus.local:443:${INGRESS_IP} https://portal.campus.local/
```

📸 screenshots/tls-https.png

---

## Task 14: End-to-End Demo

```bash
bash 04-full-demo/run-demo.sh
kubectl get configmap,secret,ingress,deploy,svc,pods -l app=yatri-app
bash 04-full-demo/cleanup.sh
```

📸 screenshots/full-demo.png

---

## Cleanup

```bash
kubectl delete -f 01-configmap/app-config.yaml
kubectl delete -f 02-secret/db-secret.yaml
kubectl delete -f 03-ingress/ingress-tls.yaml
kubectl delete -f 04-full-demo/
```

---

## Resources

- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
