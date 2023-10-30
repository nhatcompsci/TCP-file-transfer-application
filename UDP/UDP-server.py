import socket, os, struct

FORMAT = "utf-8"
BUFFER_ADDR_SIZE = 1024

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
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((ip, server_port))
        print(f"Server ({ip}) is listening on port {server_port}...")

        while True:
            (file_size, file_name), client = server.recvfrom(24+BUFFER_ADDR_SIZE)
            server.sendto("Receive file's name and size'".encode(FORMAT))
            file_name = file_name.decode(FORMAT).strip('\x00')
            print(f"Receive {file_name} with size {file_size} from {client}")

            if not os.path.exists("received_files"):
                os.makedirs("received_files")

            with open(f'received_files/{str(file_name)}', 'wb') as received_file:
                (file_data, ), client = server.recvfrom(file_size+BUFFER_ADDR_SIZE)
                server.sendto("Receive file data".encode(FORMAT))
                print(f"Receive file data from {client}")
                received_file.write(file_data)
                
                received_file.close()

                print(f"File {file_name} received. Stored as received_files/{file_name}")
                
            server.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 UDP-server.py <local-port-on-machine-1>")
        sys.exit(1)
    print("Server is starting.")

    ip = get_local_ip()
    if not ip:
        sys.exit(1)
    receive_file(int(sys.argv[1]), ip)