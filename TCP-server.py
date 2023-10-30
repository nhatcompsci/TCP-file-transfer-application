import socket

FORMAT = "utf-8"

def get_local_ip():
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80)) 
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None

def receive_file(server_port, ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        
        server.bind((ip, server_port))
        server.listen()
        print(f"Server ({ip}) is listening on port {server_port}...")
        while True:
            conn, addr = server.accept()
            print(f'Connected by {addr}')

            file_size = conn.recv(4)  # 4 bytes for file size, 
            conn.send("Receive filesize".encode(FORMAT))

            file_name = conn.recv(20).decode(FORMAT) # 20 bytes for file name
            print("Receive file: ", file_name)
            conn.send("Receive filename".encode(FORMAT))

            with open(f'received_files/{file_name}', 'wb') as received_file:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    received_file.write(data.decode(FORMAT))
                received_file.close()
                conn.send("Received filedata".encode(FORMAT))
                print(f"File {file_name} received. Stored as received_files/{file_name}")
                
            conn.close()
            print(f'{addr} disconnected.')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 TCP-server.py <local-port-on-machine-1>")
        sys.exit(1)
    print("Server is starting.")

    ip = get_local_ip()
    if not ip:
        sys.exit(1)
    receive_file(int(sys.argv[1]), ip)