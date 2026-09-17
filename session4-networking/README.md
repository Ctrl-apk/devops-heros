# Session 4 — Networking

## Student Details

- **Name:** Shifa
- **Enrollment Number:** 24BCS10354
- **Email:** shifa.24bcs10354@sst.scaler.com

---

## Homework Tasks

### Task 1: Practice Networking Commands

Practiced the networking commands provided in the DevOps-Hero GitHub repository.

### Task 2: Networking Commands with Output and Explanation

---

## Commands

### 1. `ping`

```bash
ping google.com
```

**What I understood:**
The `ping` command checks whether a device or website is reachable over a network. It sends packets to the destination and shows the response time, helping understand network connectivity and latency.

---

### 2. `traceroute`

```bash
traceroute google.com
```

**What I understood:**
`traceroute` shows the path taken by network packets from my computer to the destination. It displays each network hop and its response time, helping identify where delays or connection problems may occur.

---

### 3. `netstat`

```bash
netstat -tulnp
```

**What I understood:**
`netstat` displays network connections, listening ports, and network-related information. It helps identify which ports are open and which services are using them.

---

### 4. `telnet`

```bash
telnet google.com 80
```

**What I understood:**
`telnet` tests whether a connection can be established to a particular host and port. Port `80` is used to test HTTP connectivity.

---

### 5. `tcpdump`

```bash
sudo tcpdump -i eth0
```

**What I understood:**
`tcpdump` captures and displays network packets traveling through a network interface. It is useful for monitoring network traffic and troubleshooting connectivity problems.

---

### 6. `nslookup`

```bash
nslookup google.com
```

**What I understood:**
`nslookup` queries DNS to find information about a domain name. It shows the IP address associated with a domain and helps troubleshoot DNS resolution problems.

---

### 7. `dig`

```bash
dig google.com
```

**What I understood:**
`dig` performs DNS queries and provides detailed information about the DNS response. It is useful for understanding how domain names are resolved.

---

### 8. `curl`

```bash
curl -I https://google.com
```

**What I understood:**
`curl` communicates with web servers using HTTP/HTTPS. The `-I` flag displays only the response headers, helping check if a website is reachable and inspect the server's HTTP response.

---

## Screenshots

![Networking Commands Output](image-1.png)
![Networking Commands Output 2](image.png)

---

## Conclusion

Through this task, I practiced different networking commands and learned how to:
- Check network connectivity (`ping`)
- Trace network routes (`traceroute`)
- Inspect open ports (`netstat`)
- Test specific ports (`telnet`)
- Capture network packets (`tcpdump`)
- Perform DNS queries (`nslookup`, `dig`)
- Test HTTP connectivity (`curl`)

---

## Resources

- [DevOps-Hero GitHub Repository](https://github.com/Nency-Ravaliya/devops-heros)
- Session 4 Networking Notes
