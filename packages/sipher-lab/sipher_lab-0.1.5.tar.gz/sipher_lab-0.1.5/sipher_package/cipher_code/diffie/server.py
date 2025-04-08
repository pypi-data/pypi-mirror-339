import socket
import threading

clients = {}
lock = threading.Lock()

def client_handler(conn, addr):
    try:
        # The first message should be the client's identifier (e.g., ALICE, BOB)
        role = conn.recv(1024).decode().strip()
        print(f"{role} connected from {addr}")
        with lock:
            clients[role] = conn

        while True:
            data = conn.recv(4096)
            if not data:
                break
            message = data.decode().strip()
            print(f"Received from {role}: {message}")
            # Message protocol: messages start with "TO:<target>:"
            if message.startswith("TO:"):
                parts = message.split(":", 2)
                if len(parts) >= 3:
                    target = parts[1].strip()
                    msg = parts[2]
                    with lock:
                        if target in clients:
                            clients[target].sendall(f"FROM:{role}:{msg}".encode())
                        else:
                            print(f"Target {target} not connected.")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()
        with lock:
            if role in clients:
                del clients[role]
        print(f"{role} disconnected.")

def main():
    host = 'localhost'
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print("Server listening on port", port)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_handler, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()

# if attacker is required then go with this attacker.py instead of server.py and change the host of client.py to localhost and port to 6000.

import socket, threading, random

SERVER_HOST = 'localhost'
SERVER_PORT = 5000  # Actual server
PROXY_PORT = 6000   # Attacker's listening port

def handle_connection(client_conn, client_addr):
    # Connect to the actual server.
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect((SERVER_HOST, SERVER_PORT))
    
    def forward(src, dst, direction):
        while True:
            try:
                data = src.recv(4096)
                if not data:
                    break
                message = data.decode()
                # --- MITM Modification ---
                # When a DH public key is seen, replace it with a fake key.
                if "DH_PUBLIC:" in message:
                    parts = message.split("DH_PUBLIC:")
                    # Replace original key with attacker's fake key.
                    fake_key = random.randint(100, 200)
                    message = parts[0] + "DH_PUBLIC:" + str(fake_key)
                    print(f"[MITM] Modified {direction} DH_PUBLIC to {fake_key}")
                dst.sendall(message.encode())
            except Exception as e:
                break
        src.close()
        dst.close()
    
    threading.Thread(target=forward, args=(client_conn, server_conn, "client->server"), daemon=True).start()
    threading.Thread(target=forward, args=(server_conn, client_conn, "server->client"), daemon=True).start()

def main():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind(('localhost', PROXY_PORT))
    proxy.listen(5)
    print("MITM Attacker Proxy listening on port", PROXY_PORT)
    while True:
        client_conn, client_addr = proxy.accept()
        print(f"Accepted connection from {client_addr}")
        threading.Thread(target=handle_connection, args=(client_conn, client_addr), daemon=True).start()

if __name__ == "__main__":
    main()
