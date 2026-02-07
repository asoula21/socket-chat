import logging
import sys

BUFFER_SIZE = 1024
DEFAULT_PORT = 25535

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)


def config_port() -> int:
    try:
        while True:
            port_input = input(
                f"Enter a port number from 1024 - 65535 to listen on (default: {DEFAULT_PORT}): "
            ).strip()

            if not port_input:
                return DEFAULT_PORT

            try:
                server_port = int(port_input)
                # Anything below 1024 is generally reserved for the operating system
                if 1024 <= server_port <= 65535:
                    return server_port
                print("\nEnter a valid port number between 1024 and 65535.")
            except ValueError:
                print("\nInvalid input. Enter a numeric value for the port number.")

    except KeyboardInterrupt:
        print("\nServer setup cancelled.")
        sys.exit()


def stop_server(message: str) -> bool:
    return message.strip().lower() == "stop"


def process_message(message: str) -> str:
    if stop_server(message):
        return "The server has shut down.\n"

    try:
        number = int(message)
        parity = "even" if number % 2 == 0 else "odd"
        return f"The number {number} is {parity}.\n"
    except ValueError:
        return "Invalid input. Please send a valid integer or 'stop' to shut down the server.\n"
