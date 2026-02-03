from socket import *
from datetime import datetime

def get_server_port() -> int:
    while True:
        try:
            port = int(input("Enter your server port: "))
            # Ports below 1024 are usually reserved for the OS
            if 1024 <= port <= 65535:
                return port
            print("Port must be between 1 and 65535. Please try again.")
        except ValueError:
            print("You have not entered a valid port number. Please try again.")

def main():
    server_port = get_server_port()
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(("", server_port))

    print(f"\nServer listening on port: {server_port}\n")

    try:
        while True:
            data, client = server_socket.recvfrom(2048)
            message = data.decode()

            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            print(f"{timestamp} | Received message from [{client[0]}:{client[1]}]: {message}")

            if message.lower() == "stop":
                print("\nReceived stop command. Shutting down server...")
                response = "The server has shut down."

                server_socket.sendto(response.encode(), client)
                break

            if message.isdigit():
                number = int(message)
                response = "The number you've entered is even.\n" if number % 2 == 0 else "The number you've entered is odd.\n"
            else:
                response = "You have not entered a number. Please try again.\n"

            server_socket.sendto(response.encode(), client)
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
