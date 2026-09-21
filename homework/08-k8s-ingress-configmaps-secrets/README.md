# 08 — Kubernetes Ingress, ConfigMaps & Secrets

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code: [../../session-12-ingress-configmaps-secrets/](../../session-12-ingress-configmaps-secrets/)

---

## Task 1: ConfigMap

Decouples non-sensitive config (env, log level, port) from the container image.

```bash
kubectl apply -f ../../session-12-ingress-configmaps-secrets/01-configmap/app-config.yaml
kubectl describe configmap yatri-app-config
kubectl get configmap yatri-app-config -o jsonpath='{.data.ENVIRONMENT}' && echo ""
```

---

## Task 2: ConfigMap Live Update

Updating a ConfigMap does **not** auto-update running pods. A rolling restart is needed.

```bash
kubectl patch configmap yatri-app-config --type merge -p '{"data":{"ENVIRONMENT":"staging"}}'
kubectl exec -it deploy/yatri-backend -- env | grep ENVIRONMENT   # still production
kubectl rollout restart deployment/yatri-backend
kubectl exec -it deploy/yatri-backend -- env | grep ENVIRONMENT   # now staging
```

---

## Task 3: Secrets & Base64

```bash
kubectl apply -f ../../session-12-ingress-configmaps-secrets/02-secret/db-secret.yaml
kubectl describe secret yatri-db-secret   # values masked
kubectl get secret yatri-db-secret -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 --decode && echo ""
```

---

## Task 4: Trailing Newline Gotcha

`echo` appends a `\n` byte to the string — corrupts passwords when encoded.

```bash
echo "secretpassword" | base64    # c2VjcmV0cGFzc3dvcmQK  (has newline 0x0a)
echo -n "secretpassword" | base64 # c2VjcmV0cGFzc3dvcmQ=  (correct)
```

Always use `echo -n` when encoding secrets.

---

## Task 5: Enterprise Secret Management

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
Pod Environment Variable / Volume
```

Never commit Base64 secrets to Git — use an external secret operator instead.

---

## Task 6: Combined Injection

```bash
kubectl apply -f ../../session-12-ingress-configmaps-secrets/04-full-demo/configmap.yaml
kubectl apply -f ../../session-12-ingress-configmaps-secrets/04-full-demo/secret.yaml
kubectl apply -f ../../session-12-ingress-configmaps-secrets/04-full-demo/backend.yaml
kubectl exec -it deploy/yatri-backend -- env | grep -E "ENVIRONMENT|POSTGRES"
```

---

## Task 7: Ingress Resource vs Ingress Controller

| Component | Role |
|---|---|
| **Ingress Resource** | Declarative routing rules (YAML). Does nothing by itself |
| **Ingress Controller** | Active NGINX/Traefik pod that reads rules and routes real traffic |

---

## Task 8: Enable NGINX Ingress Controller

```bash
minikube addons enable ingress
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

---

## Task 9: Local DNS

```bash
echo "$(minikube ip)  yatri.local" | sudo tee -a /etc/hosts
```

---

## Task 10: Path-Based Routing

```bash
kubectl apply -f ../../session-12-ingress-configmaps-secrets/04-full-demo/ingress.yaml
curl http://yatri.local/        # → frontend
curl http://yatri.local/api/    # → backend
```

---

## Task 11: Virtual Host Routing

```bash
curl -H "Host: portal.campus.local" http://$(minikube ip)/
curl -H "Host: api.campus.local" http://$(minikube ip)/api/
```

---

## Task 13: TLS/HTTPS Termination

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt -subj "/CN=campus.local/O=CampusDevOps"
kubectl create secret tls campus-tls-cert --cert=tls.crt --key=tls.key
curl -k https://portal.campus.local/
```

---

## Resources

- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
