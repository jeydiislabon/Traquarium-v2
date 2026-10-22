# pages/input_page.py
"""Input page for adding new water readings"""

from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame, QScrollArea, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from ui.base_page import AquaPage
from ui.constants import MAIN_FONT
from ui.components import ButtonFactory, InputFieldFactory, ValidatorFactory, FrameFactory
from ui.styles import INPUT_FIELD_SMALL_STYLE, SCROLLBAR_STYLE
from ui.helpers import ValidationHelper
from data_model import WaterReading


class InputPage(AquaPage):
    def __init__(self, stacked_widget, history_page, graph_page, manager):
        super().__init__("Input Parameters", stacked_widget)
        self.history_page = history_page
        self.graph_page = graph_page
        self.manager = manager

        # Add spacing at top to push inputs down
        self.content_layout.addSpacing(10)
        
        # Create horizontal layout for inputs and guide
        main_horizontal = QHBoxLayout()
        main_horizontal.setSpacing(20)
        main_horizontal.setContentsMargins(20, 0, 20, 0)
        
        # Left side - Input fields
        input_wrapper = FrameFactory.create_card_frame((400, 500), 500)
        input_container = QVBoxLayout(input_wrapper)
        input_container.setContentsMargins(30, 40, 30, 40)
        input_container.setAlignment(Qt.AlignmentFlag.AlignTop)
        input_container.setSpacing(18)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter profile name")
        
        self.ph_input = InputFieldFactory.create_validated_input("Enter pH level (0-14)", 0.0, 14.0)
        self.temp_input = InputFieldFactory.create_validated_input("Enter temperature 0-40°C", 0.0, 40.0)
        self.ammonia_input = InputFieldFactory.create_validated_input("Enter ammonia 0-10 ppm", 0.0, 10.0)

        for field in (self.name_input, self.ph_input, self.temp_input, self.ammonia_input):
            field.setFont(MAIN_FONT)
            field.setMinimumSize(320, 48)
            field.setMaximumSize(440, 48)
            field.setStyleSheet(INPUT_FIELD_SMALL_STYLE)
            field.returnPressed.connect(self.save_reading)
            input_container.addWidget(field, alignment=Qt.AlignmentFlag.AlignCenter)

        self.save_button = ButtonFactory.create_success_button("Save Reading", MAIN_FONT)
        self.save_button.clicked.connect(self.save_reading)
        input_container.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.feedback = QLabel("")
        self.feedback.setFont(MAIN_FONT)
        self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback.setStyleSheet("color: #06B6D4; font-weight: 500;")
        input_container.addWidget(self.feedback)
        
        # Right side - Water Parameter Guide with scroll
        guide_container = FrameFactory.create_card_frame((400, 500), 500)
        
        guide_main_layout = QVBoxLayout(guide_container)
        guide_main_layout.setContentsMargins(15, 15, 15, 15)
        guide_main_layout.setSpacing(10)
        
        # Guide title (fixed at top)
        guide_title = QLabel("Water Parameter Guide")
        guide_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        guide_title.setStyleSheet("color: #FFFFFF; padding: 5px; background: transparent;")
        guide_main_layout.addWidget(guide_title)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(SCROLLBAR_STYLE)
        
        # Content widget inside scroll area
        scroll_content = QFrame()
        scroll_content.setStyleSheet("background: transparent; border: none;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)
        
        # Profile Name Section
        profile_section = FrameFactory.create_guide_section(
            "Profile Name",
            "Give your aquarium a unique name to identify it. This helps you track multiple tanks separately. Examples: 'Main Tank', 'Betta Tank', 'Community Tank', 'Reef Tank'.",
            "• Must contain letters (not just numbers)\n• Each profile name must be unique\n• Choose descriptive names for easy identification"
        )
        scroll_layout.addWidget(profile_section)
        
        # pH Section
        ph_section = FrameFactory.create_guide_section(
            "pH Level (6.5 - 8.0)",
            "Measures water acidity/alkalinity. Most freshwater fish thrive in pH 6.5-7.5. Marine aquariums typically need 8.0-8.4.",
            "• Too Low: Add pH buffer or reduce CO₂\n• Too High: Perform partial water change"
        )
        scroll_layout.addWidget(ph_section)
        
        # Temperature Section
        temp_section = FrameFactory.create_guide_section(
            "Temperature (20-28°C / 68-82°F)",
            "Critical for fish metabolism and immune function. Different species need different ranges. Tropical fish: 24-28°C, Coldwater fish: 18-22°C.",
            "• Too Low: Increase heater temperature\n• Too High: Improve ventilation or add cooling"
        )
        scroll_layout.addWidget(temp_section)
        
        # Ammonia Section
        ammonia_section = FrameFactory.create_guide_section(
            "Ammonia (0-0.5 ppm)",
            "Highly toxic to fish even in small amounts. Should ideally be 0 ppm in established tanks. Comes from fish waste, uneaten food, and decaying matter.",
            "• >0.5 ppm: URGENT - Immediate water change required\n• 0.2-0.5 ppm: Check filter, reduce feeding"
        )
        scroll_layout.addWidget(ammonia_section)
        
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        guide_main_layout.addWidget(scroll_area)
        
        # Add both sides to horizontal layout
        main_horizontal.addWidget(input_wrapper)
        main_horizontal.addWidget(guide_container)
        
        self.content_layout.addLayout(main_horizontal)
        
        # Add stretch to push navigation buttons to bottom
        self.content_layout.addStretch()

    def save_reading(self):
        name = self.name_input.text().strip()
        
        # Validate name
        valid, msg = ValidationHelper.validate_not_empty(name, "Profile name")
        if not valid:
            self.feedback.setText(msg)
            self.feedback.setStyleSheet("color: #EF5350; font-weight: 500;")
            return
        valid, msg = ValidationHelper.validate_not_numeric_only(name, "Profile name")
        if not valid:
            self.feedback.setText(msg)
            self.feedback.setStyleSheet("color: #EF5350; font-weight: 500;")
            return
        
        # Check for duplicate profile name
        existing_readings = self.manager.get_all()
        existing_names = [r["name"].lower() for r in existing_readings]
        if name.lower() in existing_names:
            self.feedback.setText("Profile name already exists. Please use a different name.")
            self.feedback.setStyleSheet("color: #EF5350; font-weight: 500;")
            return

        # Check which fields are missing
        missing_fields = []
        if not self.ph_input.text().strip():
            missing_fields.append("pH")
        if not self.temp_input.text().strip():
            missing_fields.append("Temperature")
        if not self.ammonia_input.text().strip():
            missing_fields.append("Ammonia")
        
        if missing_fields:
            if len(missing_fields) == 3:
                self.feedback.setText("Please input values for pH, Temperature, and Ammonia.")
            elif len(missing_fields) == 2:
                self.feedback.setText(f"Please input values for {missing_fields[0]} and {missing_fields[1]}.")
            else:
                self.feedback.setText(f"Please input value for {missing_fields[0]}.")
            self.feedback.setStyleSheet("color: #EF5350; font-weight: 500;")
            return
        
        try:
            ph = float(self.ph_input.text())
            temp = float(self.temp_input.text())
            ammonia = float(self.ammonia_input.text())
        except ValueError:
            self.feedback.setText("Please enter valid numeric values.")
            self.feedback.setStyleSheet("color: #EF5350; font-weight: 500;")
            return
        
        # Validate water parameters
        valid, msg = ValidationHelper.validate_water_params(ph, temp, ammonia)
        if not valid:
            self.feedback.setText(msg.split('\n')[0])  # Show first error
            self.feedback.setStyleSheet("color: #EF5350; font-weight: 500;")
            return

        reading = WaterReading(name, ph, temp, ammonia)
        self.manager.add_reading(reading)

        self.manager.load_readings()
        readings = self.manager.get_all()

        # Update linked pages
        self.history_page.update_table(readings)
        self.graph_page.update_graph(readings, selected_name=name)

        # Update Home Dashboard
        if hasattr(self.parentWidget().parentWidget(), "home_page"):
            self.parentWidget().parentWidget().home_page.update_latest(readings)

        # Clear inputs
        self.name_input.clear()
        self.ph_input.clear()
        self.temp_input.clear()
        self.ammonia_input.clear()
        self.feedback.setText("Reading saved successfully!")
        self.feedback.setStyleSheet("color: #66BB6A; font-weight: 500;")
        QTimer.singleShot(2000, lambda: self.feedback.clear())
