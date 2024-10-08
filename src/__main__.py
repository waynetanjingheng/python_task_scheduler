import logging
from src.view import UserOptions

LOG = logging.getLogger("src")


def main() -> None:
    LOG.info("Starting Program...")

    UserOptions.display_options_and_accept_input()

    LOG.info("Program exiting!")


if __name__ == "__main__":
    main()
