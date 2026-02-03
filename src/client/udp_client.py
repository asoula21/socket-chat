import ipaddress
from socket import socket, AF_INET, SOCK_DGRAM

BUFFER_SIZE = 2048

def get_server_info() -> tuple[str, int]:
    """Gets the server IPv4 and port from the user."""
    while True:
        try:
            server_ip = input("Enter server IPv4 address: ").strip()
            # Validate IPv4 address format
            ipaddress.IPv4Address(server_ip)
            break
        except ValueError:
            print("Invalid IPv4 address format. Please enter a valid IPv4 address.\n")

    while True:
        try:
            port = int(input("Enter server port: "))
            if 1024 <= port <= 65535:
                return server_ip, port
            print("Port must be between 1024 and 65535. Please try again.\n")
        except ValueError:
            print("You have not entered a valid port number. Please try again.\n")

def main():
    server_ip, server_port = get_server_info()

    client_socket = socket(AF_INET, SOCK_DGRAM)
    message = input("Enter a number: ")

    client_socket.sendto(message.encode(), (server_ip, server_port))
    data, server = client_socket.recvfrom(BUFFER_SIZE)

    print(data.decode())

if __name__ == "__main__":
    main()
