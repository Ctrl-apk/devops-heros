#!/bin/bash

# Take user input
read -p "Enter your name: " name

# Store information in variables
current_date=$(date)
hostname=$(hostname)
disk_usage=$(df -h)

# Create a directory
mkdir -p system_info

# Create a file
touch system_info/processes.txt

# Store running processes in the file
ps > system_info/processes.txt

# Display system information
echo "===== SYSTEM INFORMATION ====="
echo "Name: $name"
echo "Date: $current_date"
echo "Hostname: $hostname"

echo ""
echo "===== DISK USAGE ====="
echo "$disk_usage"

echo ""
echo "===== RUNNING PROCESSES ====="
ps

echo ""
echo "Process information saved to system_info/processes.txt"