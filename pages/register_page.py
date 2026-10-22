"""Registration page"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from auth import UserManager
from ui.components import ButtonFactory, InputFieldFactory, LabelFactory
from ui.helpers import PaintHelper, ValidationHelper


class RegisterPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.user_manager = UserManager()

        self.setWindowTitle("Register - Traquarium")
        self.setMinimumSize(900, 650)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title = LabelFactory.create_title("Create Account", QFont("Segoe UI", 42, QFont.Weight.Bold))
        title.setStyleSheet("color: #E8E8E8; margin-bottom: 30px;")
        layout.addWidget(title)

        self.username_input = InputFieldFactory.create_login_input("Enter your Username")
        self.password_input = InputFieldFactory.create_login_input("Enter your Password", is_password=True)
        self.confirm_password_input = InputFieldFactory.create_login_input("Confirm your Password", is_password=True)

        layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.confirm_password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)

        # Register button
        self.register_btn = ButtonFactory.create_primary_button("SIGN UP", QFont("Segoe UI", 13, QFont.Weight.Bold), (380, 50))
        self.register_btn.clicked.connect(self.register_user)
        layout.addWidget(self.register_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)
        
        login_container = QHBoxLayout()
        login_text = LabelFactory.create_subtitle("Already have an account?", QFont("Segoe UI", 11))
        self.login_link = ButtonFactory.create_secondary_button("Login", QFont("Segoe UI", 11, QFont.Weight.DemiBold), (None, 30))
        self.login_link.clicked.connect(self.go_to_login)
        
        login_container.addStretch()
        login_container.addWidget(login_text)
        login_container.addSpacing(5)
        login_container.addWidget(self.login_link)
        login_container.addStretch()
        layout.addLayout(login_container)

        layout.addSpacing(10)
        self.feedback_label = LabelFactory.create_feedback(QFont("Segoe UI", 11))
        layout.addWidget(self.feedback_label)

        self.username_input.returnPressed.connect(self.register_user)
        self.password_input.returnPressed.connect(self.register_user)
        self.confirm_password_input.returnPressed.connect(self.register_user)

    def paintEvent(self, event):
        PaintHelper.paint_blue_gradient(self, event)
        super().paintEvent(event)
    
    def go_to_login(self):
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.feedback_label.clear()
        self.stacked_widget.setCurrentIndex(1)

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        for value, field_name in [(username, "Username"), (password, "Password"), (confirm_password, "Confirm Password")]:
            valid, msg = ValidationHelper.validate_not_empty(value, field_name)
            if not valid:
                self.feedback_label.setStyleSheet("color: #EF5350;")
                self.feedback_label.setText("Please fill in all fields.")
                return
        
        for value, field_name in [(username, "Username"), (password, "Password")]:
            valid, msg = ValidationHelper.validate_no_spaces(value, field_name)
            if not valid:
                self.feedback_label.setStyleSheet("color: #EF5350;")
                self.feedback_label.setText(msg)
                return
        
        if password != confirm_password:
            self.feedback_label.setStyleSheet("color: #EF5350;")
            self.feedback_label.setText("Passwords do not match.")
            return
        
        success, msg = self.user_manager.register_user(username, password)
        color = "#66BB6A" if success else "#EF5350"
        self.feedback_label.setStyleSheet(f"color: {color};")
        self.feedback_label.setText(msg)
        
        if success:
            self.username_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()
            QTimer.singleShot(1500, lambda: self.stacked_widget.setCurrentIndex(1))
