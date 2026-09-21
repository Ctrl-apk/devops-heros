# 01 — Linux Fundamentals

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and files: [../../session2-linux/](../../session2-linux/)

---

## Task 1: Soft Link vs Hard Link

| Feature | Hard Link | Soft Link (Symbolic Link) |
|---|---|---|
| Points to | Inode (actual data) | File path/name |
| Works across filesystems | No | Yes |
| Works with directories | No | Yes |
| Original file deleted | Link still works | Link breaks |
| Command | `ln` | `ln -s` |

### Commands

```bash
# Create original file
echo "Hello" > original.txt

# Hard link — same inode
ln original.txt hardlink.txt

# Soft link — pointer to path
ln -s original.txt softlink.txt

# Check inode numbers
ls -li

# Delete original
rm original.txt

# Hard link still works
cat hardlink.txt        # outputs: Hello

# Soft link is broken
cat softlink.txt        # Error: No such file or directory

# Delete links
rm hardlink.txt softlink.txt
```

**Interview tip:** A hard link is another name for the same file (same inode). A soft link is just a pointer to a path — if the original is deleted, the soft link breaks.

---

## Task 2: adduser vs useradd

| Feature | `useradd` | `adduser` |
|---|---|---|
| Type | Low-level binary | High-level script |
| Home directory | Not created by default | Created automatically |
| Password prompt | No | Yes (interactive) |
| User-friendly | No | Yes |
| Preferred on Ubuntu | No | **Yes** |

### Commands

```bash
# Recommended on Ubuntu
sudo adduser testuser

# Verify
id testuser
cat /etc/passwd | grep testuser

# Cleanup
sudo deluser testuser
sudo rm -rf /home/testuser
```

---

## Task 3: journalctl

`journalctl` queries logs collected by **systemd-journald**.

```bash
journalctl              # all logs
journalctl -f           # follow in real time
journalctl -u docker    # logs for docker service
journalctl -u ssh -n 20 # last 20 lines for SSH
journalctl -b           # logs since last boot
journalctl -p err -b    # only errors since last boot
journalctl --disk-usage # disk usage of journal
```

---

## Task 4: Linux Command Cheat Sheet

```bash
# Files & Directories
ls -la        pwd         cd /path      mkdir dir
rm file       rm -rf dir  cp src dst    mv src dst
touch file    cat file    head -10 file tail -10 file

# Permissions
chmod 755 file    chmod +x file    chown user:group file

# Users
whoami    id    sudo adduser name    su - username

# Processes
ps aux    top    kill PID    kill -9 PID    pkill name

# Networking
ip a    ping host    curl url    ss -tulnp    ssh user@host

# Search
grep "text" file    grep -r "text" dir    find / -name "file"

# Disk & System
df -h    du -sh dir    free -h    uname -a    uptime

# Text Processing
cut -d: -f1 file    awk '{print $1}' f    sed 's/old/new/g' f
sort file    uniq file    wc -l file

# Packages (Ubuntu)
sudo apt update    sudo apt install pkg    sudo apt remove pkg
```

---

## Resources

- [Basic Linux Guide](../../session2-linux/basic-linux.pdf)
- [Advanced Linux Guide](../../session2-linux/ad-linux.pdf)
- [Linux Networking Cheat Sheet](../../session2-linux/Linux%20Networking%20Cheat%20Sheet.pdf)
