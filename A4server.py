import socket
import sys
import threading
import os
from random import randint
import base64

class UDPServer:
    def __init__(self, port):
        self.server_port = int(port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', self.server_port))
        print(f"The server starts and listens on the specified port {self.server_port}")

    def handle_client(self, filename, client_address):
        try:  #Check if the requested file exists
            if not os.path.exists(filename):
                error_msg = f"{filename} Not_Found"
                self.server_socket.sendto(error_msg.encode(), client_address)
                return

            file_size = os.path.getsize(filename)  #Get file size
            data_port = randint(50000, 51000)  #Randomly select a port between 50000 and 51000
            data_socket.settimeout(5)
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data_socket.bind(('0.0.0.0', data_port))
            ok_msg = f"OK {filename} SIZE {file_size} PORT {data_port}"
            self.server_socket.sendto(ok_msg.encode(), client_address)

            with open(filename, 'rb') as f:  #Open the file in binary mode
                running = True
                while running:
                    try:
                        request, _ = data_socket.recvfrom(65535)
                        request_str = request.decode().strip()
                        parts = request_str.split()
                        if not parts:
                            continue
                        if parts[0] == "FILE" and parts[-1] == "CLOSE":
                            close_ok_msg = f"FILE {filename} CLOSE_OK"
                            data_socket.sendto(close_ok_msg.encode(), client_address)
                            running = False

                        elif parts[0] == "FILE" and parts[1] == filename and parts[2] == "GET":
                            try:
                                start_idx = parts.index("START") + 1
                                end_idx = parts.index("END") + 1
                                start = int(parts[start_idx])
                                end = int(parts[end_idx])

                                if start < 0 or end >= file_size or start > end:
                                    continue

                                f.seek(start)
                                data = f.read(end - start + 1)
                                if not data:
                                    error_msg = f"ERR {filename} EMPTY_DATA START {start} END {end}"
                                    data_socket.sendto(error_msg.encode(), client_address)
                                    continue
                                base64_data = base64.b64encode(data).decode()#Encode binary file data as a Base64 byte string
                                response_msg = f"FILE {filename} OK START {start} END {end} DATA {base64_data}"
                                data_socket.sendto(response_msg.encode(), client_address)
                            except (ValueError, IndexError):
                                continue

                    except socket.timeout:
                        continue
                    except Exception:
                        continue
            data_socket.close()
        except Exception:
            pass

    def run(self):
        try:
            while True:
                request, client_address = self.server_socket.recvfrom(65535)#Receive a maximum of 65535 bytes of data each time
                request_str = request.decode().strip()
                if request_str.startswith("DOWNLOAD"):
                    parts = request_str.split()
                    if len(parts) >= 2:
                        filename = parts[1]
                        client_thread = threading.Thread(
                            target=self.handle_client,
                            args=(filename, client_address)
                        )
                        client_thread.daemon = True
                        client_thread.start()

        except KeyboardInterrupt:
            print("The server is stopped by the user.")
