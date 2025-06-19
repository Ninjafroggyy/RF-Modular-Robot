""" Handles communication between the laptop and Raspberry Pi. """

import socket
import json


HOST = "192.168.1.42"  # Placeholder IP
PORT = 9000

client_socket = None


def connect_to_robot(host=HOST, port=PORT):
    """Establish a socket connection to the robot."""
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("[INFO] Connected to robot.")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")


def send_data(data: dict):
    """Send data (as JSON) to the robot."""
    if not client_socket:
        print("[ERROR] Not connected to robot.")
        return
    try:
        message = json.dumps(data).encode()
        client_socket.sendall(message)
    except Exception as e:
        print(f"[ERROR] Failed to send data: {e}")
