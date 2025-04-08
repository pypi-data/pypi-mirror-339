#  Develop the Digital Signature standard (DSS)for verifying the legal communicating parties

import socket
import threading

# Pre‑defined DSA parameters (insecure, for demonstration only)
p = 467
q = 233
g = 4
# The client’s public key (y = g^x mod p). Here x (client’s private key) is 123.
y = pow(g, 123, p)

def modinv(a, m):
    # Extended Euclidean Algorithm to find modular inverse of a modulo m
    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        else:
            g_val, x_val, y_val = egcd(b, a % b)
            return (g_val, y_val, x_val - (a // b) * y_val)
    g_val, x_val, _ = egcd(a, m)
    if g_val != 1:
        raise Exception('Modular inverse does not exist')
    return x_val % m

def simple_hash(message: bytes) -> int:
    # A simple polynomial hash mod q
    h = 0
    for b in message:
        h = (h * 31 + b) % q
    return h

def verify_signature(message: bytes, r: int, s: int) -> bool:
    # Check that r and s are in the valid range
    if r <= 0 or r >= q or s <= 0 or s >= q:
        return False
    try:
        w = modinv(s, q)
    except Exception:
        return False
    h = simple_hash(message)
    u1 = (h * w) % q
    u2 = (r * w) % q
    # Compute v = ((g^u1 * y^u2) mod p) mod q
    v = ( (pow(g, u1, p) * pow(y, u2, p)) % p ) % q
    return v == r

def handle_client(conn, addr):
    try:
        print(f"Connection from {addr}")
        data = conn.recv(4096)
        if not data:
            return
        # Protocol: first line is the message, second line is the signature in the format "r,s"
        parts = data.split(b'\n')
        if len(parts) < 2:
            conn.send(b"Error: Expecting message and signature.\n")
            return
        message = parts[0].strip()
        sig_line = parts[1].strip().decode()
        try:
            r_str, s_str = sig_line.split(',')
            r = int(r_str)
            s = int(s_str)
        except Exception:
            conn.send(b"Error: Signature format invalid. Should be r,s\n")
            return
        if verify_signature(message, r, s):
            response = "Signature valid.\n"
        else:
            response = "Signature invalid.\n"
        conn.send(response.encode())
    except Exception as e:
        conn.send(str(e).encode())
    finally:
        conn.close()

def server_main():
    host = '0.0.0.0'
    port = 7000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Server listening on {host}:{port}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    server_main()
