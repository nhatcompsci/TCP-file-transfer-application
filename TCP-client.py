import socket
import struct

def send_file(remote_ip, remote_port, local_file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((remote_ip, remote_port))

        with open(local_file, 'rb') as f:
            file_data = f.read()
            file_size = len(file_data)
            file_name = local_file.split('/')[-1].encode().ljust(20, b'\x00')

            s.sendall(struct.pack('!I20s', file_size, file_name))
            s.sendall(file_data)

        print(f"File {local_file} sent.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 TCP-client.py <remote-IP-on-machine-1> <remote-port-on-machine-1> <local-file-on-machine-2-to-transfer>")
        sys.exit(1)

    remote_ip, remote_port, local_file = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    send_file(remote_ip, remote_port, local_file)
