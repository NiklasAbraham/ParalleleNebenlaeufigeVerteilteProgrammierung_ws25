#!/usr/bin/env python3
import requests
import socket

SERVICE_NAME = "counter-service"
SERVICE_PORT = 8080

def put(value):
    _, _, pod_ips = socket.gethostbyname_ex(SERVICE_NAME)
    for ip in pod_ips:
        try:
            response = requests.get(f"http://{ip}:{SERVICE_PORT}/put/{value}", timeout=2)
            print(response.text, end='')
        except Exception as e:
            print(f"Failed to reach pod {ip}: {e}")

def get():
    _, _, pod_ips = socket.gethostbyname_ex(SERVICE_NAME)
    ip = pod_ips[0]
    response = requests.get(f"http://{ip}:{SERVICE_PORT}/get")
    print(response.text, end='')

if __name__ == "__main__":
    while True:
        try:
            line = input("> ").strip()
            if not line:
                continue
            parts = line.split()
            command = parts[0]
            if command == "quit":
                break
            elif command == "put":
                if len(parts) != 2:
                    print("Usage: put <value>")
                    continue
                put(int(parts[1]))
            elif command == "get":
                get()
            else:
                print(f"Unknown command: {command}")
        except (EOFError, KeyboardInterrupt):
            break
