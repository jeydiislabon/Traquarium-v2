"""UI utilities"""

import os
from PyQt6.QtGui import QPalette, QLinearGradient, QBrush, QColor


def find_logo_path():
    possible_paths = [
        "aquarium_logo.png",
        "./aquarium_logo.png",
        os.path.join(os.getcwd(), "aquarium_logo.png"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "aquarium_logo.png"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def background(widget):
    palette = QPalette()
    bg = QLinearGradient(0, 0, 0, widget.height())
    bg.setColorAt(0.0, QColor("#1e3c72"))
    bg.setColorAt(0.5, QColor("#2a5298"))
    bg.setColorAt(1.0, QColor("#1e3c72"))
    palette.setBrush(QPalette.ColorRole.Window, QBrush(bg))
    widget.setAutoFillBackground(True)
    widget.setPalette(palette)