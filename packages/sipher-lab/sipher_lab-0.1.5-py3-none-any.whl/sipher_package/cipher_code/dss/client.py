#  Develop the Digital Signature standard (DSS)for verifying the legal communicating parties

import socket
import random

# Pre‑defined DSA parameters (must match server’s)
p = 467
q = 233
g = 4
# Client’s private key (should remain secret)
x = 123

def modinv(a, m):
    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        else:
            g_val, x_val, y_val = egcd(b, a % b)
            return (g_val, y_val, x_val - (a // b) * y_val)
    g_val, x_val, _ = egcd(a, m)
    if g_val != 1:
        raise Exception("Modular inverse does not exist")
    return x_val % m

def simple_hash(message: bytes) -> int:
    h = 0
    for b in message:
        h = (h * 31 + b) % q
    return h

def sign_message(message: bytes) -> tuple[int, int]:
    # Choose a random ephemeral key k (1 <= k < q)
    while True:
        k = random.randint(1, q - 1)
        # (Since q is prime, every nonzero k is invertible mod q)
        if k % q != 0:
            break
    r = pow(g, k, p) % q
    if r == 0:
        return sign_message(message)
    k_inv = modinv(k, q)
    h = simple_hash(message)
    s = (k_inv * (h + x * r)) % q
    if s == 0:
        return sign_message(message)
    return r, s

def client_main():
    host = '127.0.0.1'
    port = 7000
    message = input("Enter message to sign: ").strip().encode()
    r, s = sign_message(message)
    print(f"Generated Signature: r = {r}, s = {s}")
    # Send the message and signature (as "r,s") on separate lines.
    data = message + b'\n' + f"{r},{s}".encode()
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect((host, port))
    sck.send(data)
    response = sck.recv(4096)
    print("Server response:", response.decode())
    sck.close()

if __name__ == "__main__":
    client_main()
