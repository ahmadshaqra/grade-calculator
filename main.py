"""
    main.py

    Runs the application.
"""

from app.main_window import MainWindow

def main() -> None:
    """
        Starts the application.
    """

    # initialises main window and starts application
    app = MainWindow()
    app.start()

if __name__ == "__main__":
    main()
