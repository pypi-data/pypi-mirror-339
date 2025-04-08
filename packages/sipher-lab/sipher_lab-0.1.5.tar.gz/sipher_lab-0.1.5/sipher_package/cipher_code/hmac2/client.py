# Find a Message Authentication Code (HMAC) for given variable size message by using
# SHA-128 and SHA-256 Hash algorithm Measure the Time consumptions for varying
# message size for both SHA-128 and SHA 256. 


import socket

def client_main():
    host = '127.0.0.1'
    port = 6000

    # Choose algorithm ("sha128" or "sha256")
    algo = input("Enter algorithm (sha128 or sha256): ").strip().lower()
    key = input("Enter key: ").strip()
    message = input("Enter message: ").strip()
    
    # Prepare data: three lines (algorithm, key, message)
    data = algo.encode() + b'\n' + key.encode() + b'\n' + message.encode()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(data)
    result = s.recv(4096)
    print(result.decode())
    s.close()

if __name__ == "__main__":
    client_main()
