import socket
import struct

def receive_file(server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', server_port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(24)  # 4 bytes for file size, 20 bytes for file name
            file_size, file_name = struct.unpack('!I20s', data)
            file_name = file_name.decode().strip('\x00')  # Remove trailing null bytes

            with open(f'received_files/{file_name}', 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)

            print(f"File {file_name} received. Stored as received_files/{file_name}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 TCP-server.py <local-port-on-machine-1>")
        sys.exit(1)

    receive_file(int(sys.argv[1]))