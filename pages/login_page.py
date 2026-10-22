"""Login page"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from auth import UserManager
from ui.components import ButtonFactory, InputFieldFactory, LabelFactory
from ui.helpers import PaintHelper, ValidationHelper


class LoginPage(QWidget):
    def __init__(self, stacked_widget, main_window=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.user_manager = UserManager()
        self.main_window = main_window

        self.setWindowTitle("Login / Register - Traquarium")
        self.setMinimumSize(900, 650)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title = LabelFactory.create_title("Traquarium", QFont("Segoe UI", 42, QFont.Weight.Bold))
        title.setStyleSheet("color: #E8E8E8; margin-bottom: 30px;")
        layout.addWidget(title)

        self.username_input = InputFieldFactory.create_login_input("Enter your Username")
        self.password_input = InputFieldFactory.create_login_input("Enter your Password", is_password=True)

        layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)

        # Login button
        self.login_btn = ButtonFactory.create_primary_button("LOGIN", QFont("Segoe UI", 13, QFont.Weight.Bold), (380, 50))
        self.login_btn.clicked.connect(self.login_user)
        layout.addWidget(self.login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)
        
        signup_container = QHBoxLayout()
        signup_text = LabelFactory.create_subtitle("Don't have an account?", QFont("Segoe UI", 11))
        self.register_btn = ButtonFactory.create_secondary_button("Sign Up", QFont("Segoe UI", 11, QFont.Weight.DemiBold), (None, 30))
        self.register_btn.clicked.connect(self.go_to_register)
        
        signup_container.addStretch()
        signup_container.addWidget(signup_text)
        signup_container.addSpacing(5)
        signup_container.addWidget(self.register_btn)
        signup_container.addStretch()
        layout.addLayout(signup_container)

        layout.addSpacing(10)
        self.feedback_label = LabelFactory.create_feedback(QFont("Segoe UI", 11))
        layout.addWidget(self.feedback_label)

        self.username_input.returnPressed.connect(self.login_user)
        self.password_input.returnPressed.connect(self.login_user)

    def paintEvent(self, event):
        PaintHelper.paint_blue_gradient(self, event)
        super().paintEvent(event)

    def go_to_register(self):
        register_page_index = None
        
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if widget.__class__.__name__ == 'RegisterPage':
                register_page_index = i
                break
        
        if register_page_index is None:
            from pages.register_page import RegisterPage
            register_page = RegisterPage(self.stacked_widget)
            self.stacked_widget.addWidget(register_page)
            register_page_index = self.stacked_widget.count() - 1
        
        self.username_input.clear()
        self.password_input.clear()
        self.feedback_label.clear()
        self.stacked_widget.setCurrentIndex(register_page_index)

    def login_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validate inputs
        for value, field_name in [(username, "Username"), (password, "Password")]:
            valid, msg = ValidationHelper.validate_not_empty(value, field_name)
            if not valid:
                self.feedback_label.setStyleSheet("color: #EF5350;")
                self.feedback_label.setText(msg)
                return
            valid, msg = ValidationHelper.validate_no_spaces(value, field_name)
            if not valid:
                self.feedback_label.setStyleSheet("color: #EF5350;")
                self.feedback_label.setText(msg)
                return
        
        try:
            success, msg = self.user_manager.validate_user(username, password)
            color = "#66BB6A" if success else "#EF5350"
            self.feedback_label.setStyleSheet(f"color: {color};")
            self.feedback_label.setText(msg)
            if success:
                if self.main_window and hasattr(self.main_window, "set_current_user"):
                    self.main_window.set_current_user(username)
                    QTimer.singleShot(800, lambda: self.stacked_widget.setCurrentIndex(2))
        except Exception as e:
            self.feedback_label.setStyleSheet("color: #EF5350;")
            self.feedback_label.setText(f"Error: {str(e)}")
