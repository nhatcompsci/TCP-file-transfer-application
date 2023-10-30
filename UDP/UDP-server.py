import socket, os, struct

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
        print(f"Server ({ip}) is listening on port {server_port}...")
        while True:

            (file_size,) = struct.unpack("!I", server.recvfrom(4))  # 4 bytes for file size, 
            server.sendto("Receive filesize".encode(FORMAT))

            file_name = server.recvfrom(20).decode(FORMAT).strip('\x00') # 20 bytes for file name
            print(f"Receive {file_name} with size {file_size}")
            server.sendto("Receive filename".encode(FORMAT))

            if not os.path.exists("received_files"):
                os.makedirs("received_files")

            with open(f'received_files/{str(file_name)}', 'wb') as received_file:
                data = server.recvfrom(file_size)
                received_file.write(data)
                received_file.close()
                server.sendto("Received filedata".encode(FORMAT))
                print(f"File {file_name} received. Stored as received_files/{file_name}")
                
            server.close()

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