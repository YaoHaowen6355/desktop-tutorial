import socket
import sys
import threading

class UDPServer:
    def __init__(self, port):
        self.server_port = int(port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', self.server_port))
        print(f"服务器启动，监听端口 {self.server_port}")

    def handle_client(self, filename, client_address):
