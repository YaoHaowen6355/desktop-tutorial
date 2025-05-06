# Welcome to GitHub Desktop!

This is your README. READMEs are where you can communicate what your project is and how to use it.


YaoHaowen
Write your name on line 6, save it, and then head back to GitHub Desktop.

#server

#import library
import socket
import threading
from collections import defualtdict

#Provide variables to store data.
tuple_info = 0
client_num=0
operation_num=0
read_num=0
get_num=0
put_num=0
error_num=0

def Cope_with_client(client_socket):
    global client_num,operation_num,read_num,get_num,put_num=0,error_num  #Declare global variables.
    client_num+=1
    while True:
      try:  
        receive_data = client_socket.recv(1024)  #The client receives a maximum of 1024 bytes of data.
        if not receive_data:
            break
        request=receive_data.decode('utf-8')
        response = process_request(request)
        encoded_response = response.encode('utf - 8')#Send a response to the client.
        client_socket.send(encoded_response)
        operation_num+=1
      except Exception as ex:
        print("Handle errors",{ex})
        break
    client_socket.close()#Close the client socket.

    def process_request(request):
        global read_num, get_num,put_num  #Declare global variables.
        key=request[5:].split('')[0]  #Extract key value pairs starting from the 6th character of the request string.
        command=request[3]  #Extract the operation command from the 4th character of the request string.
        if command == 'R':  #Count according to the corresponding commands.
          read_num+= 1
          return process_read()
        elif command == 'G':
          get_num+= 1
          return process_get()
        elif command == 'P':
          put+num+=1
          return def process_put()
        return "Invalid command"

    def process_read():

    def process_get():

    def process_put():

    def print_all():



