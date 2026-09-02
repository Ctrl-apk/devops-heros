# Docker Overlay Networks

## What is an Overlay Network?

An overlay network is a Docker network type that allows containers running on **different Docker hosts** (different physical or virtual machines) to communicate with each other as if they were on the same local network.

It is built on top of the existing host network infrastructure — hence the name "overlay".

---

## Use Cases

- **Docker Swarm clusters** — the primary use case. Overlay networks are used by default when you deploy services in a Swarm.
- **Microservices across multiple hosts** — services like frontend, backend, and database can run on different machines but still communicate securely.
- **Multi-host deployments** — when a single host is not enough and you need to scale across servers.
- **Encrypted communication** — overlay networks support built-in encryption between nodes.

---

## How Overlay Networks Work

### Prerequisites
- Docker must be running in **Swarm mode** (`docker swarm init`)
- All hosts must be part of the same Swarm cluster

### Key Components

| Component | Role |
|---|---|
| Swarm Manager | Controls the cluster and manages network state |
| Worker Nodes | Run containers and join the overlay network |
| VXLAN | Virtual Extensible LAN — tunnels traffic between hosts |
| Control Plane | Uses gossip protocol to share network state |
| Data Plane | Actual container-to-container traffic via VXLAN tunnels |

### How it works step by step

1. You run `docker swarm init` on the manager node
2. Worker nodes join using `docker swarm join`
3. You create an overlay network: `docker network create -d overlay my-network`
4. Services attached to this network can reach each other by **container name**, regardless of which host they run on
5. Docker handles all the routing — containers use DNS to resolve service names

### Diagram

```
Host A                          Host B
┌─────────────────┐             ┌─────────────────┐
│  Container 1    │             │  Container 2    │
│  (frontend)     │◄───────────►│  (backend)      │
└────────┬────────┘   VXLAN     └────────┬────────┘
         │           Tunnel              │
    Docker Engine                   Docker Engine
         │                              │
    ─────┴──────────────────────────────┴─────
                Physical Network
```

---

## Key Commands

```bash
# Initialize swarm
docker swarm init

# Join a worker node (run on worker)
docker swarm join --token <token> <manager-ip>:2377

# Create an overlay network
docker network create -d overlay my-overlay

# Deploy a service on overlay network
docker service create --name web --network my-overlay nginx

# List networks
docker network ls

# Inspect overlay network
docker network inspect my-overlay
```

---

## Overlay vs Bridge Network

| Feature | Bridge | Overlay |
|---|---|---|
| Scope | Single host | Multi-host |
| Use case | Local dev / single server | Swarm / production clusters |
| Requires Swarm | No | Yes |
| Encryption | No | Optional (--opt encrypted) |
