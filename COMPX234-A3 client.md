
import socket
import sys

def optimize_input(line):
    parts = line.split(' ')  #Split the input `line` into multiple parts by spaces.
    command = parts[0]
    key = parts[1]
    value = parts[2]
    size = 7 + len(key) + len(value)
    return f"{size:03d} {command} {key} {value}"

def run_client():
    