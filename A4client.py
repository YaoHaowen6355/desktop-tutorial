import socket
import sys
import threading

class UDPClient:
    def __init__(self, server_host, server_port, file_list_path):
        self.server_host = server_host
        self.server_port = int(server_port)
        self.file_list_path = file_list_path
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(2)  # Initial timeout value (in seconds)
        self.max_retries = 5  # Maximum number of retries
        self.retry_sleep = 1  # Initial retry interval (in seconds)
        self.current_timeout = 2000

