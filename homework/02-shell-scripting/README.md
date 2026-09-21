# 02 — Shell Scripting

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

> Full code and files: [../../session3-shell-scripting/](../../session3-shell-scripting/)

---

## Task: System Information Script

### Script — `script1.sh`

```bash
#!/bin/bash

# Variables
current_date=$(date)
current_hostname=$(hostname)
current_user=$(whoami)

# Print system information
echo "Date: $current_date"
echo "Hostname: $current_hostname"
echo "Username: $current_user"

# Disk usage
echo ""
echo "Disk Usage:"
df -h

# Take user input
read -p "Enter your name: " name
read -p "Enter your roll number: " roll_no
read -p "Enter a comment: " comment

echo ""
echo "My name is $name"
echo "My roll number is $roll_no"
echo "My comment is: $comment"

# Create directory and file
mkdir -p system_info
touch system_info/processes.txt

# Store running processes in file
ps > system_info/processes.txt

echo ""
echo "Running processes saved to system_info/processes.txt"
cat system_info/processes.txt
```

### How to Run

```bash
chmod +x script1.sh
./script1.sh
```

---

## Commands Used

| Command | Purpose |
|---|---|
| `date` | Print current date and time |
| `hostname` | Print the system hostname |
| `whoami` | Print the current username |
| `df -h` | Print disk usage in human-readable format |
| `ps` | Print running processes |
| `read -p` | Take user input with a prompt |
| `mkdir` | Create a directory |
| `touch` | Create an empty file |
| `echo` | Print output to terminal |
| `>` | Redirect output to a file |

---

## Sample Output

```
Date: Wed Sep 17 23:00:00 UTC 2026
Hostname: DESKTOP-V0T8VEH
Username: shifa

Disk Usage:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   20G   28G  42% /

Enter your name: Shifa
Enter your roll number: 24BCS10354
Enter a comment: DevOps is awesome

My name is Shifa
My roll number is 24BCS10354
My comment is: DevOps is awesome

Running processes saved to system_info/processes.txt
  PID TTY          TIME CMD
 1234 pts/0    00:00:00 bash
 1235 pts/0    00:00:00 ps
```

---

## Resources

- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
