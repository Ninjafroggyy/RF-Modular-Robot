""" Handles communication between the laptop and Raspberry Pi. """


import socket
import json
import time

# ─── Config Constants ─────────────────────────────────────────────
# DEFAULT_HOST = "10.15.239.187"  # Replace with your Pi’s IP address
DEFAULT_HOST = '192.168.0.13'
DEFAULT_PORT = 5000
RECONNECT_DELAY = 3  # seconds

# ─── Connection State ─────────────────────────────────────────────
client_socket = None
is_connected = False


def connect_to_robot(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Establish a socket connection to the robot."""
    global client_socket, is_connected
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        is_connected = True
        print(f"[✓] Connected to robot at {host}:{port}")
    except Exception as e:
        is_connected = False
        print(f"[✗] Connection failed: {e}")


def send_data(data: dict):
    """Send data (as JSON) to the robot."""
    global client_socket, is_connected
    if not is_connected:
        print("[!] Not connected. Trying to reconnect...")
        connect_to_robot()
        if not is_connected:
            return

    try:
        json_data = json.dumps(data).encode('utf-8')
        client_socket.sendall(json_data + b"\n")  # \n as message delimiter
        print(f"[→] Sent: {data}")

    except Exception as e:
        print(f"[✗] Send failed: {e}")
        is_connected = False
        reconnect()


def receive_data():
    global client_socket
    try:
        response = client_socket.recv(4096)
        return json.loads(response.decode('utf-8'))
    except Exception as e:
        print(f"[✗] Receive failed: {e}")
        return None


def reconnect():
    global is_connected
    print(f"[↻] Reconnecting in {RECONNECT_DELAY} seconds...")
    time.sleep(RECONNECT_DELAY)
    connect_to_robot()


def disconnect():
    global client_socket, is_connected
    if client_socket:
        client_socket.close()
        print("[–] Disconnected from robot.")
    is_connected = False


if __name__ == "__main__":
    connect_to_robot()
    send_data({"command": "MOVE", "direction": "FORWARD"})
    send_data({"command": "STOP"})
    disconnect()
