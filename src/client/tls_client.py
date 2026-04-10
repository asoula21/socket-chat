import ssl
from socket import AF_INET, SOCK_STREAM, socket, timeout

from src.client.common import BUFFER_SIZE, CERTS_DIR, MESSAGE, TIMEOUT, config_server


def create_tls_context() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=CERTS_DIR / "server.crt")
    return context


def main():
    server_ip, server_port = config_server()
    context = create_tls_context()

    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.settimeout(TIMEOUT)

        with context.wrap_socket(
            client_socket, server_hostname=server_ip
        ) as tls_socket:
            try:
                print(f"Connecting to server at {server_ip}:{server_port}...")
                tls_socket.connect((server_ip, server_port))
                print("Successfully connected to server.")

                peer_cert = tls_socket.getpeercert()
                subject = dict(item[0] for item in peer_cert["subject"])
                print(
                    f"Server certificate verified: CN={subject.get('commonName', '?')}, "
                    f"TLS={tls_socket.version()}, cipher={tls_socket.cipher()[0]}"
                )
            except (timeout, ConnectionRefusedError):
                print(
                    "Connection timeout: server is not reachable. The client will now exit."
                )
                return
            except ssl.SSLError as e:
                print(f"TLS handshake failed: {e}")
                return

            print(MESSAGE)
            try:
                while True:
                    message = input("Enter a number: ").strip()

                    if not message:
                        continue

                    encoded = message.encode("utf-8")
                    if len(encoded) > BUFFER_SIZE:
                        print(
                            f"Message length: {len(encoded)}, max allowed: {BUFFER_SIZE}."
                        )
                        print("Your input was too long. Please try again.")
                        continue

                    try:
                        tls_socket.sendall(encoded)
                        data = tls_socket.recv(BUFFER_SIZE)

                        if not data:
                            print("Server closed the connection.")
                            break

                        print(data.decode("utf-8"))

                        if message.lower() == "stop":
                            print(
                                "The server has stopped. The client will also stop running."
                            )
                            break
                    except timeout:
                        print(
                            f"Server did not respond within {TIMEOUT} seconds.\nConnection timeout. Server may be busy.\n"
                        )
                    except OSError as e:
                        print(f"Network error occurred: {e}\n")
                        break
            except KeyboardInterrupt:
                print("\nStopping client...")


if __name__ == "__main__":
    main()
