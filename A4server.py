import socket
import sys
import threading
import os
from random import randint

class UDPServer:
    def __init__(self, port):
        self.server_port = int(port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', self.server_port))
        print(f"The server starts and listens on the specified port {self.server_port}")

    def handle_client(self, filename, client_address):
        try:  #Check if the requested file exists
            if not os.path.exists(filename):
                error = f"{filename} Not_Found"
                self.server_socket.sendto(error.encode(), client_address)
                return

            file_size = os.path.getsize(filename)  #Get file size
            data_port = randint(50000, 51000)  #Randomly select a port between 50000 and 51000
            data_socket.settimeout(5)
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data_socket.bind(('0.0.0.0', data_port))
            ok = f"OK {filename} SIZE {file_size} PORT {data_port}"
            self.server_socket.sendto(ok.encode(), client_address)
