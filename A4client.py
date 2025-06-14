import socket
import sys
import threading
import time
import base64

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

    def send_and_receive(self, message, address):
        retries = 0
        while retries <= self.max_retries:#Send requests and receive responses with support for retransmission mechanism
            try:
                self.client_socket.sendto(message.encode(), address)
                response, _ = self.client_socket.recvfrom(65535)
                return response.decode().strip()

            except socket.timeout:
                retries += 1
                wait_time = self.retry_sleep * (2 ** (retries - 1))
                self.current_timeout *= 2
                self.client_socket.settimeout(self.current_timeout / 1000)
                print(f"Retry {retries}/{self.max_retries}, waiting {wait_time} seconds")
                sleep(wait_time) #set sleep time for retry
                if retries > self.max_retries:
                    print("Max retries reached")
                    return None #input nothing due to retry times error
            except Exception as e:
                print(f"Other error: {str(e)}")
                return None

    def download_file(self, filename, data_port):
        try:
            # Determine the save path
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            save_path = os.path.join(desktop, filename)
            #Verify directory writability
            if not os.path.exists(desktop):
                os.makedirs(desktop)
            if not os.access(desktop, os.W_OK):
                print(f"Cannot write to desktop directory")
                return False

            print(f"Starting download: {filename}")
        except Exception as e:
            print(f"Download error: {str(e)}")
            return False