# Welcome to GitHub Desktop!

This is your README. READMEs are where you can communicate what your project is and how to use it.


YaoHaowen
Write your name on line 6, save it, and then head back to GitHub Desktop.

#server

#import library

import socket
import threading
from collections import defaultdict
from time import sleep

#Provide variables to store data.
tuple_info = defaultdict(str)
client_num=0
operation_num=0
read_num=0
get_num=0
put_num=0
error_num=0


def process_request(request):
    global read_num, get_num, put_num  # Declare global variables.
    key = request[5:].split(' ')[0]  # Extract key value pairs starting from the 6th character of the request string.
    command = request[3]  # Extract the operation command from the 4th character of the request string.
    if command == 'R':  # Count according to the corresponding commands.
        read_num += 1
        return process_read(key)
    elif command == 'G':
        get_num += 1
        return process_get(key)
    elif command == 'P':
        put_num += 1
        value = request[5 + len(key) + 1:]
        return process_put(key, value)
    return "Invalid command"

#Read the value of a specific key in the `tuple_info` dictionary.
def process_read(key):
    if key in tuple_info:
        return f"OK({key},{tuple_info[key]}) read"
    return f"ERR {key} does not exist"

#Retrieve and remove the value of a specific key from the `tuple_info` dictionary.
def process_get(key):
    if key in tuple_info:
        value = tuple_info.pop(key)
        return f"OK ({key}, {value}) removed"
    return f"ERR {key} does not exist"

#Insert a new key-value pair into the `tuple_info` dictionary.
def process_put(key, value):
    if key in tuple_info:
        return f"ERR {key} already exists"
    tuple_info[key] = value
    return f"OK ({key}, {value}) added"


def print_all():
    while True:
        sleep(10)  #
        tuple_num = len(tuple_info)
        total_tuple_size = sum(len(key) + len(value) for key, value in tuple_info.items())
        total_key_size = sum(len(key) for key in tuple_info.keys())
        total_value_size = sum(len(value) for value in tuple_info.values())

        average_tuple_size = total_tuple_size / tuple_num if tuple_num > 0 else 0
        average_key_size = total_key_size / tuple_num if tuple_num > 0 else 0
        average_value_size = total_value_size / tuple_num if tuple_num > 0 else 0

        print("Tuple Space Summary:")
        print(f"Number of tuples: {tuple_num}")
        print(f"Average tuple size: {average_tuple_size}")
        print(f"Average key size: {average_key_size}")
        print(f"Average value size: {average_value_size}")
        print(f"Total number of clients: {client_num}")
        print(f"Total number of operations: {operation_num}")
        print(f"Total READs: {read_num}")
        print(f"Total GETs: {get_num}")
        print(f"Total PUTs: {put_num}")
        print(f"Total errors: {error_num}")


def Cope_with_client(client_socket):
    global client_num, operation_num, read_num, get_num, put_num, error_num  # Declare global variables.
    client_num += 1
    while True:
        try:
            receive_data = client_socket.recv(1024)  # The client receives a maximum of 1024 bytes of data.
            if not receive_data:
                break
            request = receive_data.decode('utf-8')
            response = process_request(request)
            encoded_response = response.encode('utf-8')  # Send a response to the client.
            client_socket.send(encoded_response)
            operation_num += 1
        except Exception as ex:
            print("Handle errors", {ex})
            break
    client_socket.close()  # Close the client socket.


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 51234))
    server_socket.listen(5)
    print("Server started on port 51234")

    summary_thread = threading.Thread(target=print_all)
    summary_thread.daemon = True
    summary_thread.start()
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=Cope_with_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    run_server()