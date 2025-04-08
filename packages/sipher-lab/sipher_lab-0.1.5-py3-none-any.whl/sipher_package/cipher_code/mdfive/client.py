import socket
import hashlib  # Built-in module

def main():
    host = 'localhost'
    port = 5000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    try:
        while True:
            msg = input("Enter message (type 'exit' to quit): ")
            if msg.lower() == 'exit':
                break
            
            # Compute MD5 hash of the message
            md5 = hashlib.md5()
            md5.update(msg.encode())
            msg_hash = md5.hexdigest()
            
            # Send message and hash to server
            client.send(f"{msg}|{msg_hash}".encode())
            
            # Get server response
            response = client.recv(1024).decode()
            print("Server:", response)
    finally:
        client.close()

if __name__ == "__main__":
    main()