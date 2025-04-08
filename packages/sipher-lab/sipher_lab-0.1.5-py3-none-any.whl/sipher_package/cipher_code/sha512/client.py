# Processing of SHA-512 hash algorithm.


import socket

def client_main():
    host = '127.0.0.1'
    port = 8000
    message = input("Enter message to hash: ").strip().encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(message)
    result = s.recv(4096)
    print("SHA-512 hash:", result.decode().strip())
    s.close()

if __name__ == "__main__":
    client_main()
