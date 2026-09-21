# 05 — Docker Fundamentals (Hello World Apps)

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and Dockerfiles: [../../session6-7-docker/tasks/](../../session6-7-docker/tasks/)

---

## Six Hello World Applications

| App | Folder | Port | Base Image |
|---|---|---|---|
| Node.js | `nodejs-app/` | 3000 | node:20-alpine |
| Python | `python-app/` | 5000 | python:3.12-slim |
| Java | `java-app/` | 8080 | openjdk:21-jdk-slim |
| Apache | `Apache-app/` | 8081 | httpd:2.4-alpine |
| React | `React-app/` | 8082 | node:20-alpine + nginx:alpine |
| Nginx | `nginx-app/` | 8083 | nginx:alpine |

---

## Build and Run

```bash
# Node.js
docker build -t nodejs-hello ../../session6-7-docker/tasks/nodejs-app
docker run -d -p 3000:3000 --name nodejs-hello nodejs-hello

# Python
docker build -t python-hello ../../session6-7-docker/tasks/python-app
docker run -d -p 5000:5000 --name python-hello python-hello

# Java
docker build -t java-hello ../../session6-7-docker/tasks/java-app
docker run -d -p 8080:8080 --name java-hello java-hello

# Apache
docker build -t apache-hello ../../session6-7-docker/tasks/Apache-app
docker run -d -p 8081:80 --name apache-hello apache-hello

# React (multi-stage)
docker build -t react-hello ../../session6-7-docker/tasks/React-app
docker run -d -p 8082:80 --name react-hello react-hello

# Nginx
docker build -t nginx-hello ../../session6-7-docker/tasks/nginx-app
docker run -d -p 8083:80 --name nginx-hello nginx-hello

# Verify all running
docker ps
```

---

## Verify in Browser

| App | URL |
|---|---|
| Node.js | http://localhost:3000 |
| Python | http://localhost:5000 |
| Java | http://localhost:8080 |
| Apache | http://localhost:8081 |
| React | http://localhost:8082 |
| Nginx | http://localhost:8083 |

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
