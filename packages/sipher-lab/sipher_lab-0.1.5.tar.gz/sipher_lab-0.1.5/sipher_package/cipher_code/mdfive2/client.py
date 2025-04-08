# Develop a MD5 hash algorithm that finds the Message Authentication Code (MAC) 

import socket

def client_main():
    host = '127.0.0.1'
    port = 5000

    key = input("Enter key: ").strip()
    message = input("Enter message: ").strip()
    # Prepare data: key and message separated by a newline
    data = key.encode() + b'\n' + message.encode()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(data)
    result = s.recv(4096)
    print("HMAC-MD5:", result.decode().strip())
    s.close()

if __name__ == "__main__":
    client_main()
