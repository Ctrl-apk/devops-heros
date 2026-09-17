# Docker Multi-Stage Build - Submission

## Student Details

- **Name:** Shifa
- **Enrollment Number:** 24bcs10354

---

## Task 1: Multi-Stage Build

### Dockerfile

The multi-stage Dockerfile has two stages:

- **Stage 1 (builder):** Installs all dependencies (including dev) and copies source code.
- **Stage 2 (production):** Copies only production dependencies and the server file, keeping the final image lean.

```dockerfile
# Stage 1: Build
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Stage 2: Production
FROM node:24-alpine AS production
WORKDIR /app
COPY --from=builder /app/package*.json ./
RUN npm install --omit=dev
COPY --from=builder /app/server.js ./
EXPOSE 8080
CMD ["npm", "start"]
```

### Commands Used

**Build the image:**
```bash
docker build -t multi-stage-app .
```

**Run the container:**
```bash
docker run -d -p 8080:8080 --name multi-stage-app multi-stage-app
```

**Verify running container:**
```bash
docker ps
```

### Application Output

Accessing `http://localhost:8080` displays:

![Application Running](../screenshots/ouput.png)

### docker ps Output

![Docker PS](../screenshots/docker%20ps.png)

---

## Task 2: Deployed Applications

Three different types of applications deployed using Docker:

### 1. Node.js Application
- **Folder:** `tasks/nodejs-app/`
- **Port:** 3000
- **Command:**
```bash
docker build -t nodejs-hello ./tasks/nodejs-app
docker run -d -p 3000:3000 --name nodejs-hello nodejs-hello
```

### 2. Python Application
- **Folder:** `tasks/python-app/`
- **Port:** 5000
- **Command:**
```bash
docker build -t python-hello ./tasks/python-app
docker run -d -p 5000:5000 --name python-hello python-hello
```

### 3. Java Application
- **Folder:** `tasks/java-app/`
- **Port:** 8080
- **Command:**
```bash
docker build -t java-hello ./tasks/java-app
docker run -d -p 8080:8080 --name java-hello java-hello
```

---

## Folder Structure

```
session6-7-docker/
├── multi-stage-dockerfile/
│   ├── Dockerfile
│   ├── server.js
│   ├── package.json
│   └── SUBMISSION.md
├── screenshots/
│   ├── ouput.png
│   └── docker ps.png
└── tasks/
    ├── nodejs-app/
    ├── python-app/
    ├── java-app/
    ├── Apache-app/
    ├── React-app/
    └── nginx-app/
```
