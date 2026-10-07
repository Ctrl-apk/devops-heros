# AWS EC2 (Elastic Compute Cloud) Research

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## 1. What is EC2?
Amazon Elastic Compute Cloud (EC2) provides resizable compute capacity in the cloud. It allows users to launch virtual servers (instances) on demand.

## 2. Core Components

- **AMI (Amazon Machine Image):** Pre-configured template containing OS, application server, and software (e.g., Ubuntu 22.04 LTS).
- **Instance Types:** Combinations of CPU, memory, storage, and networking capacity (e.g., `t3.micro`, `c6g.large`).
- **Key Pairs:** Public/Private key pairs used to securely SSH into Linux instances.
- **Security Groups:** Virtual firewalls controlling inbound and outbound network traffic to instances.
- **EBS (Elastic Block Store):** High-performance block storage volumes attached to EC2 instances.
- **Public vs Private IP:** Public IPs are reachable over the internet; Private IPs are routed within the VPC.

## 3. Instance Lifecycle
`Pending` ──► `Running` ──► `Stopping` ──► `Stopped` ──► `Terminated`

## 4. Common Use Cases
Hosting web servers, application backend microservices, database clusters, and batch processing nodes.
