from socket import socket, AF_INET, SOCK_DGRAM

BUFFER_SIZE = 2048

def main():
    server_ip = "127.0.0.1"
    server_port = 12000

    client_socket = socket(AF_INET, SOCK_DGRAM)
    message = input("Enter a number: ")

    client_socket.sendto(message.encode(), (server_ip, server_port))
    data, server = client_socket.recvfrom(BUFFER_SIZE)

    print(data.decode())

if __name__ == "__main__":
    main()
