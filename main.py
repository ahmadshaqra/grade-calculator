"""
    main.py

    Runs the application.
"""

from view.main_window import MainWindow

def main():
    """
        Starts the application.
    """

    # initialises main window and starts application
    app = MainWindow()
    app.start()

if __name__ == "__main__":
    main()
