# Linux Homework Tasks

## Student Details

- **Name:** Shifa
- **Enrollment Number:** 24bcs10354

---

## Task 1: Soft Link & Hard Link

### Difference

| Feature | Hard Link | Soft Link (Symbolic Link) |
|---|---|---|
| Points to | Inode (actual data) | File path/name |
| Works across filesystems | No | Yes |
| Works with directories | No | Yes |
| Original file deleted | Link still works | Link breaks |
| Command | `ln` | `ln -s` |

### Commands

```bash
# Create a hard link
ln original.txt hardlink.txt

# Create a soft link
ln -s original.txt softlink.txt

# View links
ls -li

# Delete a link (both soft and hard)
rm softlink.txt
rm hardlink.txt
```

### Practice Example

```bash
# Create original file
echo "Hello" > original.txt

# Create hard link
ln original.txt hardlink.txt

# Create soft link
ln -s original.txt softlink.txt

# Check inode numbers (hard link shares same inode as original)
ls -li

# Delete original file
rm original.txt

# Hard link still works
cat hardlink.txt   # outputs: Hello

# Soft link is broken
cat softlink.txt   # Error: No such file or directory
```

### Interview Tip
> A hard link is another name for the same file (same inode). A soft link is just a pointer to a path — if the original is deleted, the soft link breaks.

---

## Task 2: adduser vs useradd

### Difference

| Feature | `useradd` | `adduser` |
|---|---|---|
| Type | Low-level binary | High-level script (Perl/shell) |
| Home directory | Not created by default | Created automatically |
| Password prompt | No | Yes (interactive) |
| User-friendly | No | Yes |
| Available on | All Linux distros | Debian/Ubuntu based |
| Preferred on Ubuntu | No | **Yes** |

### Why `adduser` is preferred on Ubuntu
`adduser` is a friendly wrapper around `useradd`. It automatically:
- Creates the home directory
- Sets default shell
- Prompts for password
- Copies skeleton files (`/etc/skel`)

### Commands

```bash
# Create a user using adduser (recommended on Ubuntu)
sudo adduser testuser

# Create a user using useradd (manual steps required)
sudo useradd -m -s /bin/bash testuser
sudo passwd testuser

# Verify user was created
id testuser
cat /etc/passwd | grep testuser

# Delete test user
sudo deluser testuser
sudo rm -rf /home/testuser
```

---

## Task 3: journalctl

### What is journalctl?
`journalctl` is a command-line tool to query and view logs collected by **systemd-journald** — the logging service that captures system and service logs on modern Linux systems.

### Common Commands

```bash
# View all logs
journalctl

# View logs in real time (like tail -f)
journalctl -f

# View logs for a specific service
journalctl -u nginx
journalctl -u ssh
journalctl -u docker

# View logs since last boot
journalctl -b

# View logs from the previous boot
journalctl -b -1

# View logs for a specific time range
journalctl --since "2024-01-01 00:00:00" --until "2024-01-02 00:00:00"

# Show last 50 lines
journalctl -n 50

# Show only errors
journalctl -p err

# Show logs for a specific process ID
journalctl _PID=1234

# Disk usage of journal logs
journalctl --disk-usage

# Clear old logs
sudo journalctl --vacuum-time=7d
```

### Practice Example

```bash
# Check logs for SSH service
journalctl -u ssh -n 20

# Follow Docker logs in real time
journalctl -u docker -f

# Check for any errors in the system
journalctl -p err -b
```

---

## Task 4: Linux Command Cheat Sheet

### File & Directory Commands

```bash
ls -la          # List files with details and hidden files
pwd             # Print current directory
cd /path        # Change directory
mkdir dir       # Create directory
mkdir -p a/b/c  # Create nested directories
rm file         # Remove file
rm -rf dir      # Remove directory recursively
cp src dst      # Copy file
mv src dst      # Move or rename file
touch file      # Create empty file
cat file        # View file content
less file       # View file with scrolling
head -n 10 file # First 10 lines
tail -n 10 file # Last 10 lines
tail -f file    # Follow file in real time
```

### File Permissions

```bash
chmod 755 file      # Set permissions (rwxr-xr-x)
chmod +x file       # Add execute permission
chown user:group f  # Change owner
ls -l               # View permissions
```

### User Management

```bash
whoami              # Current user
id                  # User ID and groups
sudo adduser name   # Add new user
sudo deluser name   # Delete user
su - username       # Switch user
sudo command        # Run as root
```

### Process Management

```bash
ps aux              # List all processes
top                 # Real-time process viewer
htop                # Interactive process viewer
kill PID            # Kill process by ID
kill -9 PID         # Force kill
pkill name          # Kill by process name
jobs                # List background jobs
bg                  # Resume in background
fg                  # Bring to foreground
```

### Networking

```bash
ifconfig            # Network interfaces (older)
ip a                # Network interfaces (modern)
ping host           # Test connectivity
curl url            # HTTP request
wget url            # Download file
netstat -tulnp      # Open ports
ss -tulnp           # Open ports (modern)
ssh user@host       # Connect via SSH
```

### Search & Filter

```bash
grep "text" file        # Search in file
grep -r "text" dir      # Search recursively
grep -i "text" file     # Case insensitive
find / -name "file"     # Find file by name
find . -type f          # Find all files
locate filename         # Quick file search
which command           # Path of command
```

### Disk & System

```bash
df -h               # Disk usage
du -sh dir          # Directory size
free -h             # Memory usage
uname -a            # System info
uptime              # System uptime
history             # Command history
echo $VAR           # Print variable
export VAR=value    # Set environment variable
```

### Text Processing

```bash
cut -d: -f1 file    # Cut fields
awk '{print $1}' f  # Print first column
sed 's/old/new/g' f # Replace text
sort file           # Sort lines
uniq file           # Remove duplicates
wc -l file          # Count lines
```

### Package Management (Ubuntu/Debian)

```bash
sudo apt update             # Update package list
sudo apt upgrade            # Upgrade packages
sudo apt install pkg        # Install package
sudo apt remove pkg         # Remove package
sudo apt autoremove         # Remove unused packages
dpkg -l | grep pkg          # Check if installed
```

---

## Resources

- [Linux Command Cheat Sheet](./Linux%20Networking%20Cheat%20Sheet.pdf)
- [Basic Linux Guide](./basic-linux.pdf)
- [Advanced Linux Guide](./ad-linux.pdf)
