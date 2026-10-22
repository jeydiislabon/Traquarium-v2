"""Register page -- matching split layout with login page."""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame,
    QLineEdit, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPainter, QColor, QLinearGradient, QPointF
from auth import UserManager
from ui.helpers import ValidationHelper


class RegisterPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.user_manager   = UserManager()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----------------------------------------------------------------
        # LEFT -- brand panel
        # ----------------------------------------------------------------
        self.left_panel = QFrame()
        self.left_panel.setMinimumWidth(420)
        self.left_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_panel.setStyleSheet("background: transparent;")

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(50, 60, 50, 60)
        left_layout.setSpacing(0)

        logo_row = QHBoxLayout()
        logo_box = QLabel("T")
        logo_box.setFixedSize(52, 52)
        logo_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_box.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        logo_box.setStyleSheet("""
            background: rgba(255,255,255,0.2);
            color: white; border-radius: 12px;
        """)
        brand_name = QLabel("Traquarium")
        brand_name.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        brand_name.setStyleSheet("color: white; background: transparent;")
        logo_row.addWidget(logo_box)
        logo_row.addSpacing(12)
        logo_row.addWidget(brand_name)
        logo_row.addStretch()
        left_layout.addLayout(logo_row)
        left_layout.addStretch()

        headline = QLabel("Create your\nfree account.")
        headline.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        headline.setStyleSheet("color: white; background: transparent;")
        headline.setWordWrap(True)
        left_layout.addWidget(headline)
        left_layout.addSpacing(20)

        sub = QLabel(
            "Start tracking your tank water quality\n"
            "with full NH3 toxicity analysis."
        )
        sub.setFont(QFont("Segoe UI", 11))
        sub.setStyleSheet("color: rgba(255,255,255,0.75); background: transparent;")
        sub.setWordWrap(True)
        left_layout.addWidget(sub)
        left_layout.addStretch()

        tagline = QLabel("Powered by Emerson (1975) NH3 Equilibrium + PSO Optimization")
        tagline.setFont(QFont("Segoe UI", 9))
        tagline.setStyleSheet("color: rgba(255,255,255,0.5); background: transparent;")
        tagline.setWordWrap(True)
        left_layout.addWidget(tagline)

        # ----------------------------------------------------------------
        # RIGHT -- form panel
        # ----------------------------------------------------------------
        right_panel = QFrame()
        right_panel.setMinimumWidth(400)
        right_panel.setMaximumWidth(520)
        right_panel.setStyleSheet("background: #F9FAFB;")

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(55, 0, 55, 0)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setSpacing(0)

        title = QLabel("Create Account")
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: #111827;")
        right_layout.addWidget(title)
        right_layout.addSpacing(6)

        sub2 = QLabel("Fill in the details below to get started.")
        sub2.setFont(QFont("Segoe UI", 11))
        sub2.setStyleSheet("color: #6B7BB0;")
        right_layout.addWidget(sub2)
        right_layout.addSpacing(28)

        for attr, label_text, placeholder, is_pw in [
            ("username_input", "USERNAME",         "Choose a username",        False),
            ("password_input", "PASSWORD",         "Choose a password",        True),
            ("confirm_input",  "CONFIRM PASSWORD", "Re-enter your password",   True),
        ]:
            lbl = QLabel(label_text)
            lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #374151; letter-spacing: 1px;")
            right_layout.addWidget(lbl)
            right_layout.addSpacing(6)

            field = QLineEdit()
            field.setPlaceholderText(placeholder)
            field.setFixedHeight(46)
            field.setFont(QFont("Segoe UI", 11))
            if is_pw:
                field.setEchoMode(QLineEdit.EchoMode.Password)
            field.setStyleSheet(self._field_style())
            field.returnPressed.connect(self.register_user)
            right_layout.addWidget(field)
            setattr(self, attr, field)
            right_layout.addSpacing(14)

        right_layout.addSpacing(10)

        self.register_btn = QPushButton("Create Account  ->")
        self.register_btn.setFixedHeight(48)
        self.register_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #B01040, stop:1 #8B1A3A);
                color: #FFFFFF; border: none; border-radius: 8px;
                font-weight: bold; letter-spacing: 1px;
            }
            QPushButton:hover { background: #C01550; }
            QPushButton:pressed { background: #6B0020; }
        """)
        self.register_btn.clicked.connect(self.register_user)
        right_layout.addWidget(self.register_btn)
        right_layout.addSpacing(20)

        login_row = QHBoxLayout()
        login_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        has_acc = QLabel("Already have an account?")
        has_acc.setFont(QFont("Segoe UI", 10))
        has_acc.setStyleSheet("color: #6B7BB0;")
        login_link = QPushButton("Sign In")
        login_link.setFlat(True)
        login_link.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        login_link.setStyleSheet("""
            QPushButton { color: #111827; background: transparent;
                          border: none; text-decoration: underline; }
            QPushButton:hover { color: #374151; }
        """)
        login_link.setCursor(Qt.CursorShape.PointingHandCursor)
        login_link.clicked.connect(self.go_to_login)
        login_row.addWidget(has_acc)
        login_row.addSpacing(4)
        login_row.addWidget(login_link)
        right_layout.addLayout(login_row)
        right_layout.addSpacing(12)

        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Segoe UI", 10))
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setWordWrap(True)
        right_layout.addWidget(self.feedback_label)

        main_layout.addWidget(self.left_panel, stretch=55)
        main_layout.addWidget(right_panel,     stretch=45)

    @staticmethod
    def _field_style():
        return """
            QLineEdit {
                border: 1.5px solid #D1D5DB; border-radius: 8px;
                padding: 0 14px; background: white;
                color: #111827; font-size: 13px;
            }
            QLineEdit:focus { border: 2px solid #111827; }
        """

    def paintEvent(self, event):
        painter = QPainter(self)
        panel_rect = self.left_panel.geometry()
        grad = QLinearGradient(
            QPointF(panel_rect.left(), 0),
            QPointF(panel_rect.right(), self.height())
        )
        grad.setColorAt(0.0, QColor("#1A2472"))
        grad.setColorAt(0.45, QColor("#673888"))
        grad.setColorAt(1.0, QColor("#8B1A3A"))
        painter.fillRect(panel_rect, grad)
        from PyQt6.QtCore import QRect
        right_rect = QRect(panel_rect.right(), 0,
                           self.width() - panel_rect.right(), self.height())
        painter.fillRect(right_rect, QColor("#F3F4F6"))
        super().paintEvent(event)

    def go_to_login(self):
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_input.clear()
        self.feedback_label.clear()
        self.stacked_widget.setCurrentIndex(1)

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm  = self.confirm_input.text().strip()

        for val, name in [
            (username, "Username"), (password, "Password"), (confirm, "Confirm Password")
        ]:
            ok, msg = ValidationHelper.validate_not_empty(val, name)
            if not ok:
                self._err("Please fill in all fields."); return
            ok, msg = ValidationHelper.validate_no_spaces(val, name)
            if not ok:
                self._err(msg); return

        if password != confirm:
            self._err("Passwords do not match."); return

        success, msg = self.user_manager.register_user(username, password)
        if success:
            self.feedback_label.setStyleSheet("color: #059669;")
            self.feedback_label.setText("Account created! Redirecting to login...")
            self.username_input.clear()
            self.password_input.clear()
            self.confirm_input.clear()
            QTimer.singleShot(1500, lambda: self.stacked_widget.setCurrentIndex(1))
        else:
            self._err(msg)

    def _err(self, msg):
        self.feedback_label.setStyleSheet("color: #DC2626;")
        self.feedback_label.setText(msg)
