"""Loading screen"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from ui.constants import MAIN_FONT
from ui.utils import find_logo_path


class LoadingPage(QWidget):
    def __init__(self, stacked_widget, delay_ms: int = 5000):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.delay_ms = delay_ms

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(0)

        # Circular logo
        self.logo_label = CircularLogoLabel()
        self.logo_label.setFixedSize(250, 250)
        logo_path = find_logo_path()
        if logo_path:
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap)
        
        layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(40)
        
        loading_text = QLabel("Loading...")
        loading_text.setFont(MAIN_FONT)
        loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_text.setStyleSheet("color: #B8B8B8;")
        layout.addWidget(loading_text)
        layout.addSpacing(15)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(400, 8)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        from ui.styles import PROGRESS_BAR_STYLE
        self.progress_bar.setStyleSheet(PROGRESS_BAR_STYLE)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self._progress = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_progress)
        self._timer.start(50)
        
        QTimer.singleShot(self.delay_ms, self._go_to_login)

    def _update_progress(self):
        self._progress += 2
        if self._progress > 100:
            self._progress = 100
        self.progress_bar.setValue(self._progress)

    def _go_to_login(self):
        self._timer.stop()
        self.stacked_widget.setCurrentIndex(1)

    def paintEvent(self, event):
        from ui.helpers import PaintHelper
        PaintHelper.paint_blue_gradient(self, event)
        super().paintEvent(event)


class CircularLogoLabel(QLabel):
    def __init__(self):
        super().__init__()
        self._pixmap = None
        
    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self.update()
    
    def paintEvent(self, event):
        if self._pixmap is None or self._pixmap.isNull():
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        painter.setClipPath(path)
        
        scaled_pixmap = self._pixmap.scaled(
            self.width(), 
            self.height(), 
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        
        x = (self.width() - scaled_pixmap.width()) // 2
        y = (self.height() - scaled_pixmap.height()) // 2
        
        painter.drawPixmap(x, y, scaled_pixmap)
