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
