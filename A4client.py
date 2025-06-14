import socket
import sys
import threading
import time
import base64
import os

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
                time.sleep(wait_time) #set sleep time for retry
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


                print(f"[process] 0.00% (0/{file_size} byte)", end="", flush=True)
                while downloaded < file_size:
                    end = min(downloaded + block_size - 1, file_size - 1)
                    request_msg = f"FILE {filename} GET START {downloaded} END {end}"
                    response = self.send_and_receive(request_msg, (self.server_host, data_port))


                    if response.startswith("FILE") and "OK" in response:
                        try:
                            parts = response.split()
                            start_idx = parts.index("START") + 1
                            end_idx = parts.index("END") + 1
                            resp_start = int(parts[start_idx])
                            resp_end = int(parts[end_idx])

                            if resp_start != downloaded or resp_end < resp_start:
                                print(f"Response range mismatch")
                                continue
                            # Extract Base64-encoded data from response
                            data_idx = parts.index("DATA") + 1
                            base64_data = " ".join(parts[data_idx:])
                            try:
                                file_data = base64.b64decode(base64_data)
                                if len(file_data) == 0:
                                    print("Received empty data block")
                                    continue
                            except base64.binascii.Error:
                                print(f"Base64 decoding failed")
                                continue
                            f.write(file_data)   # Write data to file and update progress
                            f.flush()   # Ensure data is written immediately
                            previous_downloaded = downloaded
                            downloaded = resp_end + 1

                            if (downloaded // (file_size // 10)) > (
                                    previous_downloaded // (file_size // 10)):  # Display progress (update every 10%)
                                progress = (downloaded / file_size) * 100
                                print(f"\r[progress] {progress:.2f}% ({downloaded}/{file_size} byte)", end="", flush=True)

                        except (ValueError, IndexError):
                            print(f"\nResponse format error")
                            data_socket.close()
                            return False
                    else:
                        print(f"\nUnknown response format")
                        data_socket.close()
                        return False
                print(f"\r[progress] 100.00% ({file_size}/{file_size} byte) - download successfully")
                # Send close request
                close_msg = f"FILE {filename} CLOSE"
                close_response = self.send_and_receive(close_msg, (self.server_host, data_port))
                if close_response and close_response.startswith("FILE") and "CLOSE_OK" in close_response:
                    print("Connection closed")
                else:
                    print("No closure confirmation received")
                data_socket.close()
                return True
        except Exception as e:
            print(f"Download error: {str(e)}")
            return False

    def run(self):
            try:
                with open(self.file_list_path, 'r') as f: # Read file list
                    file_list = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
                if not file_list:
                    print("file list is empty")
                    return
                print(f"begin to download {len(file_list)} files")
                for i, filename in enumerate(file_list): #output detail information for files
                    print(f"\n===== file {i + 1}/{len(file_list)}: {filename} =====")
                    if self.download_file(filename, 0):
                        print(f"file {filename} download successfully")
                    else:
                        print(f"file {filename} download failed")
            except FileNotFoundError:
                print(f"file list is not exist: {self.file_list_path}")
            finally:
                self.client_socket.close()
                print("client is closed")
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("method: python A4client.py localhost 51234 files.txt") #the order in my computer
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = sys.argv[2]
    file_list_path = sys.argv[3]

    client = UDPClient(server_host, server_port, file_list_path)
    client.run()