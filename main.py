from app_setup import create_tracker_and_storage
from frontend.terminal_ui import TerminalUI


def main():
    tracker, storage = create_tracker_and_storage()

    ui = TerminalUI(tracker, storage)
    ui.run()


if __name__ == "__main__":
    main()
