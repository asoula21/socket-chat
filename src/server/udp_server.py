from socket import *

while True:
    try:
        server_port = int(input("Enter your server port: "))
        break
    except ValueError:
        print("You have not entered valid port number. Please try again.")

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('' , server_port))

print(f"Listening on port: {server_port}")

while True:
    data, client = server_socket.recvfrom(2048)
    message = data.decode()
    server_socket.sendto(message.encode(), client)
