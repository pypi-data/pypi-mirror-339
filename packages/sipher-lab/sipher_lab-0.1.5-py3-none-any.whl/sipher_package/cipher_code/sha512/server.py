# Processing of SHA-512 hash algorithm.

import socket
import threading

def rightrotate(x, n):
    return ((x >> n) | (x << (64 - n))) & 0xFFFFFFFFFFFFFFFF

def sha512(message: bytes) -> bytes:
    # Preprocessing: pad the message
    ml = len(message) * 8  # Message length in bits
    message += b'\x80'
    # Pad with zeros until message length (in bits) mod 1024 is 896
    while (len(message) * 8) % 1024 != 896:
        message += b'\x00'
    # Append original message length as 128-bit big-endian integer
    message += ml.to_bytes(16, byteorder='big')
    
    # Initial hash values (first 64 bits of the fractional parts of the square roots of the first 8 primes)
    H = [
        0x6a09e667f3bcc908,
        0xbb67ae8584caa73b,
        0x3c6ef372fe94f82b,
        0xa54ff53a5f1d36f1,
        0x510e527fade682d1,
        0x9b05688c2b3e6c1f,
        0x1f83d9abfb41bd6b,
        0x5be0cd19137e2179
    ]
    
    # SHA-512 constants (first 64 bits of the fractional parts of the cube roots of the first 80 primes)
    K = [
        0x428a2f98d728ae22, 0x7137449123ef65cd,
        0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
        0x3956c25bf348b538, 0x59f111f1b605d019,
        0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
        0xd807aa98a3030242, 0x12835b0145706fbe,
        0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
        0x72be5d74f27b896f, 0x80deb1fe3b1696b1,
        0x9bdc06a725c71235, 0xc19bf174cf692694,
        0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
        0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
        0x2de92c6f592b0275, 0x4a7484aa6ea6e483,
        0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
        0x983e5152ee66dfab, 0xa831c66d2db43210,
        0xb00327c898fb213f, 0xbf597fc7beef0ee4,
        0xc6e00bf33da88fc2, 0xd5a79147930aa725,
        0x06ca6351e003826f, 0x142929670a0e6e70,
        0x27b70a8546d22ffc, 0x2e1b21385c26c926,
        0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
        0x650a73548baf63de, 0x766a0abb3c77b2a8,
        0x81c2c92e47edaee6, 0x92722c851482353b,
        0xa2bfe8a14cf10364, 0xa81a664bbc423001,
        0xc24b8b70d0f89791, 0xc76c51a30654be30,
        0xd192e819d6ef5218, 0xd69906245565a910,
        0xf40e35855771202a, 0x106aa07032bbd1b8,
        0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
        0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
        0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
        0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
        0x748f82ee5defb2fc, 0x78a5636f43172f60,
        0x84c87814a1f0ab72, 0x8cc702081a6439ec,
        0x90befffa23631e28, 0xa4506cebde82bde9,
        0xbef9a3f7b2c67915, 0xc67178f2e372532b,
        0xca273eceea26619c, 0xd186b8c721c0c207,
        0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
        0x06f067aa72176fba, 0x0a637dc5a2c898a6,
        0x113f9804bef90dae, 0x1b710b35131c471b,
        0x28db77f523047d84, 0x32caab7b40c72493,
        0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
        0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
        0x5fcb6fab3ad6faec, 0x6c44198c4a475817
    ]
    
    # Process the message in successive 1024-bit (128-byte) chunks
    for i in range(0, len(message), 128):
        chunk = message[i:i+128]
        # Prepare the message schedule (80 words of 64 bits)
        w = [0] * 80
        for j in range(16):
            w[j] = int.from_bytes(chunk[j*8:(j+1)*8], byteorder='big')
        for j in range(16, 80):
            s0 = (rightrotate(w[j-15], 1) ^ rightrotate(w[j-15], 8) ^ (w[j-15] >> 7)) & 0xFFFFFFFFFFFFFFFF
            s1 = (rightrotate(w[j-2], 19) ^ rightrotate(w[j-2], 61) ^ (w[j-2] >> 6)) & 0xFFFFFFFFFFFFFFFF
            w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFFFFFFFFFF
        
        # Initialize working variables to current hash value
        a, b, c, d, e, f, g, h = H
        
        # Compression function main loop
        for j in range(80):
            S1 = (rightrotate(e, 14) ^ rightrotate(e, 18) ^ rightrotate(e, 41)) & 0xFFFFFFFFFFFFFFFF
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + K[j] + w[j]) & 0xFFFFFFFFFFFFFFFF
            S0 = (rightrotate(a, 28) ^ rightrotate(a, 34) ^ rightrotate(a, 39)) & 0xFFFFFFFFFFFFFFFF
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFFFFFFFFFF
            
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFFFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFFFFFFFFFF
        
        # Add the compressed chunk to the current hash value
        H = [
            (H[0] + a) & 0xFFFFFFFFFFFFFFFF,
            (H[1] + b) & 0xFFFFFFFFFFFFFFFF,
            (H[2] + c) & 0xFFFFFFFFFFFFFFFF,
            (H[3] + d) & 0xFFFFFFFFFFFFFFFF,
            (H[4] + e) & 0xFFFFFFFFFFFFFFFF,
            (H[5] + f) & 0xFFFFFFFFFFFFFFFF,
            (H[6] + g) & 0xFFFFFFFFFFFFFFFF,
            (H[7] + h) & 0xFFFFFFFFFFFFFFFF,
        ]
    # Produce the final hash value (512 bits) as a byte string
    digest = b''.join(x.to_bytes(8, byteorder='big') for x in H)
    return digest

def sha512_hex(message: bytes) -> str:
    return sha512(message).hex()

def handle_client(conn, addr):
    try:
        print(f"Connection from {addr}")
        data = conn.recv(65536)
        if not data:
            return
        # Protocol: client sends a message to hash (raw bytes)
        message = data.strip()
        hash_hex = sha512_hex(message)
        response = f"{hash_hex}\n"
        conn.send(response.encode())
    except Exception as e:
        conn.send(str(e).encode())
    finally:
        conn.close()

def server_main():
    host = '0.0.0.0'
    port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Server listening on {host}:{port}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    server_main()
