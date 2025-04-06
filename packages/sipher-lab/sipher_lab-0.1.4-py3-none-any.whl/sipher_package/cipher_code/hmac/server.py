import hashlib
import socket

def hmac_sha256(key, message):
    """Generate HMAC-SHA256."""
    block_size = 64  # Block size for SHA-256
    if len(key) > block_size:
        key = hashlib.sha256(key).digest()
    key = key.ljust(block_size, b'\x00')
    o_key_pad = bytes((x ^ 0x5C) for x in key)
    i_key_pad = bytes((x ^ 0x36) for x in key)
    return hashlib.sha256(o_key_pad + hashlib.sha256(i_key_pad + message).digest()).digest()

def start_server(host, port, shared_key):
    """Start the HMAC server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            # Receive message from client
            data = conn.recv(1024)
            if not data:
                return

            # Generate HMAC for the received message
            hmac = hmac_sha256(shared_key, data)

            # Send the HMAC back to the client
            conn.sendall(hmac)

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Localhost
    PORT = 65432        # Arbitrary non-privileged port
    SHARED_KEY = b'secret_key'  # Shared secret key

    start_server(HOST, PORT, SHARED_KEY)
