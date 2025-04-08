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

def start_client(host, port, shared_key):
    """Start the HMAC client."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        # Message to send
        message = b'Hello, server!'
        
        # Send the message to server
        client_socket.sendall(message)
        
        # Receive HMAC from server
        received_hmac = client_socket.recv(1024)
        
        # Verify HMAC
        expected_hmac = hmac_sha256(shared_key, message)
        if expected_hmac == received_hmac:
            print("Message is authentic.")
        else:
            print("Message authentication failed.")

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Localhost
    PORT = 65432        # Same port as server
    SHARED_KEY = b'secret_key'  # Same shared key as server
    
    start_client(HOST, PORT, SHARED_KEY)