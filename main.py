import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from main_app import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 12))
    app.setStyleSheet("* { outline: none; }")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())