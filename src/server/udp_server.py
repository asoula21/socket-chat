from socket import *

server_port = 25535
server_socket = socket(AF_INET, SOCK_DGRAM)

server_socket.bind(('' , server_port))

print("Waiting...")

while True:
    data, client = server_socket.recvfrom(2048)
    message = data.decode()
    server_socket.sendto(message.encode(), client)
