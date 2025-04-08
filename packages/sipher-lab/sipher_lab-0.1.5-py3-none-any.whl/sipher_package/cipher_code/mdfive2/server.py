# Develop a MD5 hash algorithm that finds the Message Authentication Code (MAC) 

import socket
import threading
import math

# --- MD5 Implementation ---
def leftrotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

def md5(message: bytes) -> bytes:
    # Save original message length in bits
    original_length = len(message) * 8

    # Pre-processing: padding the message
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += original_length.to_bytes(8, byteorder='little')

    # Initialize MD5 buffer variables
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    # Per-round shift amounts
    S = ([7, 12, 17, 22] * 4 +
         [5, 9, 14, 20] * 4 +
         [4, 11, 16, 23] * 4 +
         [6, 10, 15, 21] * 4)

    # Precompute the 64 T values
    T = [0] * 64
    for i in range(64):
        T[i] = int((2**32) * abs(math.sin(i + 1))) & 0xFFFFFFFF

    # Process the message in successive 512-bit (64-byte) chunks
    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset + 64]
        M = [int.from_bytes(chunk[i:i+4], byteorder='little') for i in range(0, 64, 4)]
        a, b, c, d = A, B, C, D

        for i in range(64):
            if 0 <= i <= 15:
                f = (b & c) | ((~b) & d)
                g = i
            elif 16 <= i <= 31:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16

            temp = d
            d = c
            c = b
            b = (b + leftrotate((a + f + T[i] + M[g]) & 0xFFFFFFFF, S[i])) & 0xFFFFFFFF
            a = temp

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    # Produce the final hash value (little-endian) as 16-byte digest
    digest = (A.to_bytes(4, byteorder='little') +
              B.to_bytes(4, byteorder='little') +
              C.to_bytes(4, byteorder='little') +
              D.to_bytes(4, byteorder='little'))
    return digest

def md5_hex(message: bytes) -> str:
    return md5(message).hex()

# --- HMAC-MD5 Implementation ---
def hmac_md5(key: bytes, message: bytes) -> bytes:
    block_size = 64  # MD5 block size in bytes
    # If key is longer than block size, shorten it
    if len(key) > block_size:
        key = md5(key)
    # Pad key to block size
    if len(key) < block_size:
        key += b'\x00' * (block_size - len(key))

    o_key_pad = bytes((b ^ 0x5c) for b in key)
    i_key_pad = bytes((b ^ 0x36) for b in key)

    inner_hash = md5(i_key_pad + message)
    return md5(o_key_pad + inner_hash)

# --- Server Code ---
def handle_client(conn, addr):
    try:
        print(f"Connection from {addr}")
        data = conn.recv(4096)
        if not data:
            return

        # Protocol: first line is key, second line is message
        parts = data.split(b'\n', 1)
        if len(parts) < 2:
            conn.send(b"Error: Please send key and message separated by a newline.\n")
            return

        key = parts[0].strip()
        message = parts[1].strip()
        mac = hmac_md5(key, message)
        response = mac.hex().encode() + b'\n'
        conn.send(response)
    except Exception as e:
        conn.send(str(e).encode())
    finally:
        conn.close()

def server_main():
    host = '0.0.0.0'
    port = 5000
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
