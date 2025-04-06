import socket, threading, random, sys, time

# Global shared key variable (set after DH exchange)
shared_key = None

# ---------- Helper Functions for DSS Demo ----------

def simple_hash(message):
    """A simple (and insecure) hash: sum of ASCII codes modulo 1000."""
    return sum(ord(c) for c in message) % 1000

def generate_dss_keys():
    # For demonstration choose small primes (not secure for real use)
    p = 467    # A prime number
    q = 233    # Another prime (demo only)
    g = 2      # A primitive root modulo p (demo)
    private = random.randint(2, q-1)
    public = pow(g, private, p)
    return p, q, g, private, public

def sign_message(message, private, p, g):
    # Simplified signature: compute hash(message) and raise to private exponent modulo p.
    h = simple_hash(message)
    signature = pow(h, private, p)
    return signature

def verify_signature(message, signature, public, p, g):
    h = simple_hash(message)
    # In our demo, we simulate verification by comparing two computed values.
    lhs = pow(signature, g, p)
    rhs = pow(h, public, p)
    return lhs == rhs

# ---------- Diffie–Hellman Key Exchange ----------

def diffie_hellman_shared(private, other_public, p):
    # Shared secret computed as (other's public key)^private mod p.
    return pow(other_public, private, p)

# ---------- Simple XOR Encryption Functions ----------

def simple_encrypt(message, key):
    key_byte = key % 256
    return ''.join(chr(ord(c) ^ key_byte) for c in message)

def simple_decrypt(ciphertext, key):
    # XOR is symmetric
    key_byte = key % 256
    return ''.join(chr(ord(c) ^ key_byte) for c in ciphertext)

# ---------- Socket Communication Handlers ----------

def receive_messages(s, role):
    global shared_key
    while True:
        try:
            data = s.recv(4096)
            if not data:
                break
            message = data.decode().strip()
            # Process messages based on protocol
            if message.startswith("FROM:"):
                parts = message.split(":", 2)
                sender = parts[1].strip()
                content = parts[2].strip()
                # Check if message is a DH public key (or DSS message) or an encrypted message
                if content.startswith("DH_PUBLIC:") or content.startswith("MSG:"):
                    # Simply print these messages (they are handled in main too)
                    print(message)
                elif content.startswith("ENC:"):
                    # Encrypted message received; decrypt it using the shared key
                    encrypted_text = content[len("ENC:"):]
                    if shared_key is not None:
                        decrypted_text = simple_decrypt(encrypted_text, shared_key)
                        print(f"FROM {sender} (decrypted): {decrypted_text}")
                    else:
                        print(f"FROM {sender}: {content}")
                else:
                    print(message)
            else:
                print(message)
        except Exception as e:
            print("Receive error:", e)
            break

def main():
    global shared_key
    if len(sys.argv) < 2:
        print("Usage: python client.py <ROLE> (e.g., ALICE or BOB)")
        sys.exit(1)
    role = sys.argv[1].upper()
    
    # For legitimate exchange use server port 5000.
    # For MITM demo, change this to the attacker proxy port (e.g., 6000).
    SERVER_HOST = 'localhost'
    SERVER_PORT = 6000  # Change to 6000 for MITM demo

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))
    s.sendall(role.encode())
    
    # Start a thread to continuously receive messages.
    threading.Thread(target=receive_messages, args=(s, role), daemon=True).start()

    # -------------- Diffie–Hellman Key Exchange --------------
    # Use small prime and generator for the demo.
    dh_p = 467  # In practice, use a large prime.
    dh_g = 2
    private_key = random.randint(2, 100)
    public_key = pow(dh_g, private_key, dh_p)
    
    # Determine target (ALICE sends to BOB and vice versa)
    target = "BOB" if role == "ALICE" else "ALICE"
    
    time.sleep(10)  # Allow time for both clients to be connected.
    # Send DH public key.
    s.sendall(f"TO:{target}:DH_PUBLIC:{public_key}".encode())
    print(f"{role} sent DH public key: {public_key}")

    # Wait to receive the other party's DH public key.
    other_public = None
    while other_public is None:
        data = s.recv(4096)
        if not data:
            break
        msg = data.decode().strip()
        if msg.startswith("FROM:"):
            parts = msg.split(":", 2)
            sender = parts[1].strip()
            content = parts[2].strip()
            if content.startswith("DH_PUBLIC:"):
                try:
                    other_public = int(content.split("DH_PUBLIC:")[1])
                    print(f"{role} received DH public key from {sender}: {other_public}")
                except Exception as e:
                    print("Error parsing DH public key:", e)
    if other_public is None:
        print("Did not receive a DH public key. Exiting.")
        sys.exit(1)

    # Compute shared secret
    shared_key = diffie_hellman_shared(private_key, other_public, dh_p)
    print(f"{role} computed shared secret: {shared_key}")

    # -------------- Digital Signature (DSS) Demo --------------
    # Generate DSS keys for signing and verification.
    p_dss, q_dss, g_dss, private_dss, public_dss = generate_dss_keys()
    message = f"Hello from {role}"
    signature = sign_message(message, private_dss, p_dss, g_dss)
    print(f"{role} signed message: '{message}' with signature: {signature}")

    # Send signed message along with DSS parameters so the receiver can verify.
    signed_packet = f"TO:{target}:MSG:{message}|SIG:{signature}|PUB_DSS:{public_dss}|P_DSS:{p_dss}|G_DSS:{g_dss}"
    s.sendall(signed_packet.encode())

    # Wait for a signed message from the other party and verify it.
    verified = False
    while not verified:
        data = s.recv(4096)
        if not data:
            break
        msg = data.decode().strip()
        if msg.startswith("FROM:"):
            try:
                # Expected format:
                # FROM:<sender>:MSG:<message>|SIG:<signature>|PUB_DSS:<public>|P_DSS:<p>|G_DSS:<g>
                parts = msg.split(":", 2)
                sender = parts[1].strip()
                content = parts[2].strip()
                if content.startswith("MSG:"):
                    segments = content.split("|")
                    msg_text = segments[0].split("MSG:")[1]
                    sig_val = int(segments[1].split("SIG:")[1])
                    pub_dss_other = int(segments[2].split("PUB_DSS:")[1])
                    p_dss_other = int(segments[3].split("P_DSS:")[1])
                    g_dss_other = int(segments[4].split("G_DSS:")[1])
                    verified = verify_signature(msg_text, sig_val, pub_dss_other, p_dss_other, g_dss_other)
                    if verified:
                        print(f"{role} verified signature from {sender} on message: '{msg_text}'")
                    else:
                        print(f"{role} failed to verify signature from {sender} on message: '{msg_text}'")
            except Exception as e:
                print("Error processing signed message:", e)
    
    # -------------- Secure Communication Using Shared Key --------------
    # Now that both clients have established a shared key and verified each other,
    # they can exchange encrypted messages.
    print("Secure communication established. You can now send messages (type 'exit' to quit).")
    while True:
        # Read a message from the user
        user_msg = input("Enter message: ")
        if user_msg.lower() == 'exit':
            break
        # Encrypt the message using the shared key
        encrypted_msg = simple_encrypt(user_msg, shared_key)
        # Send the encrypted message to the target using the protocol prefix "ENC:"
        s.sendall(f"TO:{target}:ENC:{encrypted_msg}".encode())
    
    s.close()

if __name__ == "__main__":
    main()
