import logging
import sys

BUFFER_SIZE = 1024
MAX_CONNECTIONS = 1

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)


def set_port() -> int:
    prompt = "Enter the port number to listen on (1024 - 65535): "
    while True:
        try:
            port = int(input(prompt).strip())
            # Anything below 1024 is generally reserved for the operating system
            if 1024 <= port <= 65535:
                return port
            else:
                print("\nEnter a valid port number between 1024 and 65535.")
        except ValueError:
            print("\nInvalid input. Enter a numeric value for the port number.")
        except KeyboardInterrupt:
            sys.exit(0)

        prompt = "Please try again: "


def stop_server(message: str) -> bool:
    return message.strip().lower() == "stop"


def process_message(message: str) -> str:
    if stop_server(message):
        return "The server has shut down."

    try:
        number = int(message)
        parity = "even" if number % 2 == 0 else "odd"
        return f"The number {number} is {parity}."
    except ValueError:
        return "Invalid input. Please send a valid integer or 'stop' to shut down the server."
