import socket
import threading
import hashlib  # Built-in module

def handle_client(conn):
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            # Split message and MD5 hash (format: "message|hash")
            if '|' in data:
                msg, received_hash = data.split('|', 1)
                
                # Compute MD5 hash of received message
                md5 = hashlib.md5()
                md5.update(msg.encode())
                computed_hash = md5.hexdigest()
                
                # Verify integrity
                if computed_hash == received_hash:
                    response = f"[VALID] Message: {msg}"
                else:
                    response = "[TAMPERED] Hash mismatch!"
            else:
                response = "[ERROR] Invalid format."
            
            conn.send(response.encode())
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def main():
    host = 'localhost'
    port = 5000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server listening on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        print(f"Connected to {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    main()