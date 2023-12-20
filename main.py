#!/usr/bin/env python
import subprocess

# Read the number of machines
worker_count = None
with open("input.txt", "r") as file:
    worker_count = int(file.readline().strip())

# Create number of machines + 1 worker processes.
worker_count += 1
worker_file = "worker.py"
command = f"mpiexec -n {worker_count} python3 {worker_file}"
subprocess.run(command.split())
