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
            download_msg = f"DOWNLOAD {filename}"  # Send download request
            response = self.send_and_receive(download_msg, (self.server_host, self.server_port))

            if not response:
                print(f"No server response received")
                return False
            file_size = 0
            if response.startswith("OK"):
                parts = response.split()
                try:
                    file_size = int(parts[parts.index("SIZE") + 1])  # Get file size
                    data_port = int(parts[parts.index("PORT") + 1])  # Extract data port
                    print(f"file size: {file_size} byte，Data port: {data_port}")
                except (ValueError, IndexError):
                    print(f"Server response format error")
                    return False
            elif response.startswith("ERR"):
                print(f"Server response: {response}")
                return False
            else:
                print(f"unknown response: {response}")
                return False

            with open(save_path, 'wb') as f:
                downloaded = 0
                block_size = 8192  # 8KB block size
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data_socket.settimeout(self.current_timeout / 1000)

                print(f"[process] 0.00% (0/{file_size} byte)", end="", flush=True)
                while downloaded < file_size:
                    end = min(downloaded + block_size - 1, file_size - 1)
                    request_msg = f"FILE {filename} GET START {downloaded} END {end}"

                    response = self.send_and_receive(request_msg, (self.server_host, data_port))

        except Exception as e:
            print(f"Download error: {str(e)}")
            return False

