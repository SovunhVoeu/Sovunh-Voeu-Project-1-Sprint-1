"""
Author: Sovunh Voeu
Date: 3/4/2025
"""
from mainWindow import MainWindow
import sys
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
