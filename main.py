#!/usr/bin/env python
import subprocess
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("input_file", type=str)
parser.add_argument("output_file", type=str)

args = parser.parse_args()

# Read the number of machines
worker_count = None
with open(args.input_file, "r") as file:
    worker_count = int(file.readline().strip())

# Create number of machines + 1 worker processes.
worker_count += 1
worker_file = "worker.py"
command = f"mpiexec -n {worker_count} python3 {worker_file} {args.input_file} {args.output_file}"
subprocess.run(command.split())
