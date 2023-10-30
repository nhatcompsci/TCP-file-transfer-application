import socket, struct

FORMAT = "utf-8"

def send_file(remote_ip, remote_port, local_file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((remote_ip, remote_port))

        with open(local_file, 'rb') as f:
            file_data = f.read()
            file_size = len(file_data)
            file_name = local_file[:20]

            client.send(struct.pack('!I', file_size))
            print(f"server: {client.recv(1024).decode(FORMAT)}")

            client.send(struct.pack('20s', file_name.encode(FORMAT)))
            print(f"server: {client.recv(1024).decode(FORMAT)}")

            client.send(struct.pack(f'{file_size}s', file_name.encode(FORMAT)))
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
