"""Welcome screen"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from ui.constants import TITLE_FONT, SUBTITLE_FONT, MAIN_FONT
from ui.utils import find_logo_path


class WelcomePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        logo = QLabel()
        logo_path = find_logo_path()
        if logo_path:
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(220, Qt.TransformationMode.SmoothTransformation)
                logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        self.title = QLabel("Welcome to Traquarium")
        self.title.setFont(TITLE_FONT)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.title)

        self.subtitle = QLabel("Let's explore your aquarium data!")
        self.subtitle.setFont(SUBTITLE_FONT)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet("color: #A8DADC;")
        layout.addWidget(self.subtitle)

        btn_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #293438, stop:1 #1D2429);
                color: #FFFFFF; padding: 12px 28px; border-radius: 12px;
                font-weight: bold; border: none; outline: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #242C30, stop:1 #0F1314);
            }
        """
        
        for text, callback in [("Home", self._go_dashboard), ("About Us", self._show_about)]:
            btn = QPushButton(text)
            btn.setFont(MAIN_FONT)
            btn.setFixedSize(200, 50)
            btn.setStyleSheet(btn_style)
            btn.clicked.connect(callback)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def paintEvent(self, event):
        from ui.helpers import PaintHelper
        PaintHelper.paint_blue_gradient(self, event)
        super().paintEvent(event)

    def _go_dashboard(self):
        self.stacked_widget.setCurrentIndex(3 if self.stacked_widget.count() > 3 else 0)

    def _show_about(self):
        about_text = """
        <h2>Traquarium</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Description:</b> A modern aquarium monitoring and management system.</p>
        <p><b>Features:</b></p>
        <ul>
            <li>Real-time water quality monitoring</li>
            <li>Historical data tracking and visualization</li>
            <li>Intuitive dashboard with key metrics</li>
            <li>Data input and management tools</li>
        </ul>
        <p><b>Developed by:</b> Traquarium Team</p>
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("About Traquarium")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2B2B2B;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 12px;
            }
            QPushButton {
                background-color: #293438;
                color: #FFFFFF;
                padding: 8px 16px;
                border-radius: 8px;
                border: none;
                outline: none;
            }
            QPushButton:hover {
                background-color: #242C30;
            }
        """)
        msg.exec()