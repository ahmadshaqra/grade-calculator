"""
    main.py

    Runs the application.
"""

from controller.app import App

def main() -> None:
    """
        Starts the application.
    """

    # initialises main window and starts application
    app = App()
    app.start()

if __name__ == "__main__":
    main()
