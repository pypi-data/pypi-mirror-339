# Find a Message Authentication Code (HMAC) for given variable size message by using
# SHA-128 and SHA-256 Hash algorithm Measure the Time consumptions for varying
# message size for both SHA-128 and SHA 256. 


import socket
import threading
import time
import math

# ---------------------------
# SHA-256 Implementation
# ---------------------------
def _rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def sha256(message: bytes) -> bytes:
    # Pre-processing: padding the message
    ml = len(message) * 8  # message length in bits
    message += b'\x80'
    while ((len(message) * 8) % 512) != 448:
        message += b'\x00'
    message += ml.to_bytes(8, byteorder='big')

    # Initial hash values (first 32 bits of the fractional parts of the square roots of the first 8 primes)
    H = [
        0x6a09e667,
        0xbb67ae85,
        0x3c6ef372,
        0xa54ff53a,
        0x510e527f,
        0x9b05688c,
        0x1f83d9ab,
        0x5be0cd19
    ]

    # Constants (first 32 bits of the fractional parts of the cube roots of the first 64 primes)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    # Process the message in successive 512-bit chunks
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        w = [0] * 64
        # Prepare the message schedule
        for t in range(16):
            w[t] = int.from_bytes(chunk[t*4:(t+1)*4], byteorder='big')
        for t in range(16, 64):
            s0 = _rotr(w[t-15], 7) ^ _rotr(w[t-15], 18) ^ (w[t-15] >> 3)
            s1 = _rotr(w[t-2], 17) ^ _rotr(w[t-2], 19) ^ (w[t-2] >> 10)
            w[t] = (w[t-16] + s0 + w[t-7] + s1) & 0xFFFFFFFF

        # Initialize working variables
        a, b, c, d, e, f, g, h = H

        # Main compression loop
        for t in range(64):
            S1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + K[t] + w[t]) & 0xFFFFFFFF
            S0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        # Update hash values
        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

    # Produce the final hash value (big-endian)
    digest = b''.join(hv.to_bytes(4, byteorder='big') for hv in H)
    return digest

# ---------------------------
# SHA-128 “Variant”
# ---------------------------
def sha128(message: bytes) -> bytes:
    # We use the SHA-256 algorithm and then truncate the output to 128 bits (16 bytes)
    return sha256(message)[:16]

# ---------------------------
# HMAC Implementation
# ---------------------------
def hmac(hash_func, block_size, key: bytes, message: bytes) -> bytes:
    # If key is longer than block size, shorten it by hashing it first.
    if len(key) > block_size:
        key = hash_func(key)
    # Pad key to block size if necessary.
    if len(key) < block_size:
        key = key + b'\x00' * (block_size - len(key))
    
    o_key_pad = bytes((b ^ 0x5c) for b in key)
    i_key_pad = bytes((b ^ 0x36) for b in key)
    
    inner_hash = hash_func(i_key_pad + message)
    return hash_func(o_key_pad + inner_hash)

def hmac_sha256(key: bytes, message: bytes) -> bytes:
    return hmac(sha256, 64, key, message)

def hmac_sha128(key: bytes, message: bytes) -> bytes:
    return hmac(sha128, 64, key, message)

# ---------------------------
# Server Code
# ---------------------------
def handle_client(conn, addr):
    try:
        print(f"Connection from {addr}")
        data = conn.recv(65536)  # receive up to 64KB
        if not data:
            return

        # Protocol: first line is algorithm, second line is key, third line is message.
        lines = data.split(b'\n', 2)
        if len(lines) < 3:
            conn.send(b"Error: Expecting algorithm, key, and message each on a new line.\n")
            return

        algo = lines[0].strip().decode().lower()
        key = lines[1].strip()
        message = lines[2].strip()

        # Measure time consumption for HMAC computation.
        start_time = time.perf_counter()
        if algo == "sha256":
            digest = hmac_sha256(key, message)
        elif algo == "sha128":
            digest = hmac_sha128(key, message)
        else:
            conn.send(b"Error: Unknown algorithm. Use 'sha128' or 'sha256'.\n")
            return
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        # Prepare response: digest (hex) and time in seconds.
        response = f"Digest: {digest.hex()}\nTime: {elapsed:.6f} sec\n"
        conn.send(response.encode())
    except Exception as e:
        conn.send(str(e).encode())
    finally:
        conn.close()

def server_main():
    host = '0.0.0.0'
    port = 6000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    server_main()
