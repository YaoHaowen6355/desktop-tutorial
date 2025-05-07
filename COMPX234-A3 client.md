
import socket
import sys

def optimize_input(line):
    parts = line.split(' ')  #Split the input `line` into multiple parts by spaces.
    command = parts[0]
    key = parts[1]
    if command == 'PUT':
        value = parts[2]
        size = 7 + len(key) + len(value)
        return f"{size:03d} {command} {key} {value}"
    else:
        size = 7 + len(key)
        return f"{size:03d} {command} {key}"

def run_client(hostname, port, request_file):
      #Create a TCP socket object. `socket.AF_INET` indicates using the IPv4 address family. Try to connect to the specified server.
     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     client_socket.connect((hostname, port))

     with open(request_file,'r') as file:
         for line in file:
             if line:
                 request=optimize_input(line)
                 client_socket.send(request.encode('utf- 8'))
                 #Receive up to 1024 bytes of response data from the server and decode it into a UTF-8 string.
                 data=client_socket.recv(1024)
                 response=data.decode('utf- 8')
                 print(f"{line}: {response}")
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:  #Set it so that the client can only run when the number of parameters is 4.
        print("Usage: python Client.py <hostname> <port> <requestFile>")
        sys.exit(1)
    
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]
    start_client(hostname, port, request_file)