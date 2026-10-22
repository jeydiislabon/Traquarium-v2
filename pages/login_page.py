"""Login page -- SENSE-inspired split layout (left brand panel + right form)"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPainter, QColor, QLinearGradient
from PyQt6.QtCore import Qt, QTimer, QPointF
from auth import UserManager
from ui.components import ButtonFactory, InputFieldFactory, LabelFactory
from ui.helpers import ValidationHelper


class LoginPage(QWidget):
    def __init__(self, stacked_widget, main_window=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.user_manager   = UserManager()
        self.main_window    = main_window

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----------------------------------------------------------------
        # LEFT -- brand panel (teal/blue gradient)
        # ----------------------------------------------------------------
        self.left_panel = QFrame()
        self.left_panel.setMinimumWidth(420)
        self.left_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_panel.setStyleSheet("background: transparent;")

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(50, 60, 50, 60)
        left_layout.setSpacing(0)

        # Logo / wordmark area
        logo_row = QHBoxLayout()
        logo_box = QLabel("T")
        logo_box.setFixedSize(52, 52)
        logo_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_box.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        logo_box.setStyleSheet("""
            background: rgba(255,255,255,0.2);
            color: white;
            border-radius: 12px;
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

        # Headline
        headline = QLabel("Every tank,\nevery reading,\nprecisely safe.")
        headline.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        headline.setStyleSheet("color: white; background: transparent; line-height: 1.2;")
        headline.setWordWrap(True)
        left_layout.addWidget(headline)

        left_layout.addSpacing(20)

        # Sub-text
        sub = QLabel(
            "Ammonia Toxicity Decision Support System.\n"
            "Offline, precise, and built for local fish retail."
        )
        sub.setFont(QFont("Segoe UI", 11))
        sub.setStyleSheet("color: rgba(255,255,255,0.75); background: transparent;")
        sub.setWordWrap(True)
        left_layout.addWidget(sub)

        left_layout.addStretch()

        # Bottom tagline
        tagline = QLabel("Powered by Emerson (1975) NH3 Equilibrium + PSO Optimization")
        tagline.setFont(QFont("Segoe UI", 9))
        tagline.setStyleSheet("color: rgba(255,255,255,0.5); background: transparent;")
        tagline.setWordWrap(True)
        left_layout.addWidget(tagline)

        # ----------------------------------------------------------------
        # RIGHT -- form panel (white / light)
        # ----------------------------------------------------------------
        right_panel = QFrame()
        right_panel.setMinimumWidth(400)
        right_panel.setMaximumWidth(520)
        right_panel.setStyleSheet("background: #F9FAFB;")

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(55, 0, 55, 0)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setSpacing(0)

        sign_in_title = QLabel("Sign In")
        sign_in_title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        sign_in_title.setStyleSheet("color: #111827;")
        right_layout.addWidget(sign_in_title)

        right_layout.addSpacing(6)

        sign_in_sub = QLabel("Enter your credentials to continue.")
        sign_in_sub.setFont(QFont("Segoe UI", 11))
        sign_in_sub.setStyleSheet("color: #6B7BB0;")
        right_layout.addWidget(sign_in_sub)

        right_layout.addSpacing(32)

        # Username
        un_label = QLabel("USERNAME")
        un_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        un_label.setStyleSheet("color: #374151; letter-spacing: 1px;")
        right_layout.addWidget(un_label)
        right_layout.addSpacing(6)

        self.username_input = QLabel.__new__(QLabel)  # placeholder -- replaced below
        from PyQt6.QtWidgets import QLineEdit
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(46)
        self.username_input.setFont(QFont("Segoe UI", 11))
        self.username_input.setStyleSheet(self._field_style())
        right_layout.addWidget(self.username_input)

        right_layout.addSpacing(16)

        pw_label = QLabel("PASSWORD")
        pw_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        pw_label.setStyleSheet("color: #374151; letter-spacing: 1px;")
        right_layout.addWidget(pw_label)
        right_layout.addSpacing(6)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(46)
        self.password_input.setFont(QFont("Segoe UI", 11))
        self.password_input.setStyleSheet(self._field_style())
        right_layout.addWidget(self.password_input)

        right_layout.addSpacing(28)

        # Sign in button
        self.login_btn = QLabel.__new__(QLabel)
        from PyQt6.QtWidgets import QPushButton
        self.login_btn = QPushButton("Sign in  ->")
        self.login_btn.setFixedHeight(48)
        self.login_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #B01040, stop:1 #8B1A3A);
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover { background: #C01550; }
            QPushButton:pressed { background: #6B0020; }
        """)
        self.login_btn.clicked.connect(self.login_user)
        right_layout.addWidget(self.login_btn)

        right_layout.addSpacing(20)

        # Sign up link
        from PyQt6.QtWidgets import QHBoxLayout as QHL
        signup_row = QHL()
        signup_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        no_acc = QLabel("Don't have an account?")
        no_acc.setFont(QFont("Segoe UI", 10))
        no_acc.setStyleSheet("color: #6B7BB0;")
        self.register_btn = QPushButton("Sign Up")
        self.register_btn.setFlat(True)
        self.register_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.register_btn.setStyleSheet("""
            QPushButton { color: #673888; background: transparent;
                          border: none; text-decoration: underline; }
            QPushButton:hover { color: #C06090; }
        """)
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_btn.clicked.connect(self.go_to_register)
        signup_row.addWidget(no_acc)
        signup_row.addSpacing(4)
        signup_row.addWidget(self.register_btn)
        right_layout.addLayout(signup_row)

        right_layout.addSpacing(12)

        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Segoe UI", 10))
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setWordWrap(True)
        right_layout.addWidget(self.feedback_label)

        # ----------------------------------------------------------------
        # Assemble
        # ----------------------------------------------------------------
        main_layout.addWidget(self.left_panel, stretch=55)
        main_layout.addWidget(right_panel,     stretch=45)

        self.username_input.returnPressed.connect(self.login_user)
        self.password_input.returnPressed.connect(self.login_user)

    # ----------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------

    @staticmethod
    def _field_style():
        return """
            QLineEdit {
                border: 1.5px solid #D1D5DB;
                border-radius: 8px;
                padding: 0 14px;
                background: white;
                color: #111827;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #111827;
            }
        """

    def paintEvent(self, event):
        """Paint the left panel with the aquarium palette gradient."""
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
        # Dark background for right side
        from PyQt6.QtCore import QRect
        right_rect = QRect(panel_rect.right(), 0,
                           self.width() - panel_rect.right(), self.height())
        painter.fillRect(right_rect, QColor("#F3F4F6"))
        super().paintEvent(event)

    # ----------------------------------------------------------------
    # Navigation
    # ----------------------------------------------------------------

    def go_to_register(self):
        for i in range(self.stacked_widget.count()):
            if self.stacked_widget.widget(i).__class__.__name__ == "RegisterPage":
                self._clear()
                self.stacked_widget.setCurrentIndex(i)
                return
        from pages.register_page import RegisterPage
        rp = RegisterPage(self.stacked_widget)
        self.stacked_widget.addWidget(rp)
        self._clear()
        self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)

    def _clear(self):
        self.username_input.clear()
        self.password_input.clear()
        self.feedback_label.clear()

    # ----------------------------------------------------------------
    # Auth
    # ----------------------------------------------------------------

    def login_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        for val, name in [(username, "Username"), (password, "Password")]:
            ok, msg = ValidationHelper.validate_not_empty(val, name)
            if not ok:
                self._err(msg); return
            ok, msg = ValidationHelper.validate_no_spaces(val, name)
            if not ok:
                self._err(msg); return

        try:
            success, msg = self.user_manager.validate_user(username, password)
            if success:
                self.feedback_label.setStyleSheet("color: #059669;")
                self.feedback_label.setText("Login successful!")
                if self.main_window and hasattr(self.main_window, "set_current_user"):
                    self.main_window.set_current_user(username)
                    QTimer.singleShot(600, lambda: self.stacked_widget.setCurrentIndex(2))
            else:
                self._err(msg)
        except Exception as e:
            self._err(f"Error: {e}")

    def _err(self, msg):
        self.feedback_label.setStyleSheet("color: #DC2626;")
        self.feedback_label.setText(msg)
