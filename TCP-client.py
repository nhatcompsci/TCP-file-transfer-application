import socket, struct

FORMAT = "utf-8"

def send_file(remote_ip, remote_port, local_file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((remote_ip, remote_port))

        with open(local_file, 'rb') as f:
            file_size = len(f)
            client.send(struct.pack('!I', file_size))
            print(f"server: {client.recv(1024).decode(FORMAT)}")

            file_name = local_file
            client.send(file_name.encode(FORMAT))
            print(f"server: {client.recv(1024).decode(FORMAT)}")

            file_data = f.read()
            client.send(file_data.encode(FORMAT))
            print(f"server: {client.recv(1024).decode(FORMAT)}")
            
            print(f"File {local_file} sent.")
            f.close()

        client.close()

        

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 TCP-client.py <remote-IP-on-machine-1> <remote-port-on-machine-1> <local-file-on-machine-2-to-transfer>")
        sys.exit(1)

    remote_ip, remote_port, local_file = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    send_file(remote_ip, remote_port, local_file)
