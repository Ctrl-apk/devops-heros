# AWS VPC (Virtual Private Cloud) Research

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## 1. What is VPC?
Amazon Virtual Private Cloud (VPC) lets you provision a logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define.

## 2. Core Building Blocks

- **CIDR Block:** Classless Inter-Domain Routing IP range assigned to VPC (e.g., `10.0.0.0/16`).
- **Subnets:** Range of IP addresses in your VPC.
  - *Public Subnet*: Has direct route to Internet Gateway.
  - *Private Subnet*: Isolated from direct internet access.
- **Route Tables:** Set of rules (routes) determining where network traffic is directed.
- **Internet Gateway (IGW):** Enables communication between VPC resources and the internet.
- **NAT Gateway:** Allows private subnet resources to connect to the internet while preventing external outbound connections.
- **Security Groups vs Network ACLs:**
  - *Security Group*: Stateful firewall at the EC2 instance level.
  - *Network ACL (NACL)*: Stateless firewall at the subnet level.
