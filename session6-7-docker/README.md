# Session 6 & 7 — Docker Fundamentals

## Student Details

- **Name:** Shifa
- **Enrollment Number:** 24BCS10354
- **Email:** shifa.24bcs10354@sst.scaler.com

---

## Folder Structure

```
session6-7-docker/
├── tasks/
│   ├── nodejs-app/        ← Hello World Node.js
│   ├── python-app/        ← Hello World Python
│   ├── java-app/          ← Hello World Java
│   ├── Apache-app/        ← Hello World Apache
│   ├── React-app/         ← Hello World React
│   └── nginx-app/         ← Hello World Nginx
├── multi-stage-dockerfile/
│   ├── Dockerfile
│   ├── server.js
│   ├── package.json
│   └── SUBMISSION.md
├── node-app/
├── nginx-web/
├── python-app/
└── docker-compose-app/
```

---

## Task 1: Hello World Docker Applications

Created Hello World web applications using Docker for 6 different stacks.

| App | Folder | Port | Image |
|---|---|---|---|
| Node.js | `tasks/nodejs-app/` | 3000 | node:20-alpine |
| Python | `tasks/python-app/` | 5000 | python:3.12-slim |
| Java | `tasks/java-app/` | 8080 | openjdk:21-jdk-slim |
| Apache | `tasks/Apache-app/` | 8081 | httpd:2.4-alpine |
| React | `tasks/React-app/` | 8082 | node:20-alpine + nginx:alpine |
| Nginx | `tasks/nginx-app/` | 8083 | nginx:alpine |

### Build and Run Commands

```bash
# Node.js
docker build -t nodejs-hello ./tasks/nodejs-app
docker run -d -p 3000:3000 --name nodejs-hello nodejs-hello

# Python
docker build -t python-hello ./tasks/python-app
docker run -d -p 5000:5000 --name python-hello python-hello

# Java
docker build -t java-hello ./tasks/java-app
docker run -d -p 8080:8080 --name java-hello java-hello

# Apache
docker build -t apache-hello ./tasks/Apache-app
docker run -d -p 8081:80 --name apache-hello apache-hello

# React (multi-stage)
docker build -t react-hello ./tasks/React-app
docker run -d -p 8082:80 --name react-hello react-hello

# Nginx
docker build -t nginx-hello ./tasks/nginx-app
docker run -d -p 8083:80 --name nginx-hello nginx-hello
```

### Verify All Running

```bash
docker ps
```

---

## Task 2: Docker Multi-Stage Build

See full documentation: [multi-stage-dockerfile/SUBMISSION.md](./multi-stage-dockerfile/SUBMISSION.md)

### Summary

- **Stage 1 (builder):** Installs all dependencies and copies source code
- **Stage 2 (production):** Copies only production deps and server file — smaller final image
- **Port:** 8080

```bash
docker build -t multi-stage-app ./multi-stage-dockerfile
docker run -d -p 8080:8080 --name multi-stage-app multi-stage-app
```

Open `http://localhost:8080` → **Hello World from Docker Multi-Stage Build!**

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
