# TCP-file-transfer-application
Server and client applications can be running on two different machines. 
You need to first start the server application using the following command:

    python3 TCP-server.py <local-port-on-machine-1>

Then you need to start the client application using the following command:

    python3 TCP-client.py <remote-IP-on-machine-1> <remote-port-on-machine-1> <local-file-on-machine-2-to-transfer>

The TCP-client.py program sends all bytes of the local file, and server application
should receive the file and store it in a different directory to avoid overwriting the
original file. Use diff or md5sum at the terminal to ensure that the transferred
file is the same as the original one.

we will use a simple file transfer protocol: the first 4 bytes (in network
byte order) contains the number of bytes in the file to follow, and then the next 20
bytes should contain the name of the file (assume the name fits in 20 bytes). The rest
of the bytes in the TCP stream to follow will contain the data in the file.