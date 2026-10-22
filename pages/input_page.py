# pages/input_page.py
"""Input page — accepts TAN, pH, Temperature (+ optional kH, gH) and
   computes NH3 via AmmoniaEngine before saving to SQLite."""

from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame, QScrollArea, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from ui.base_page import AquaPage
from ui.constants import MAIN_FONT
from ui.components import ButtonFactory, InputFieldFactory, ValidatorFactory, FrameFactory
from ui.styles import INPUT_FIELD_SMALL_STYLE, SCROLLBAR_STYLE
from ui.helpers import ValidationHelper
from data_model import WaterReading
from ammonia_engine import AmmoniaEngine, PH_MIN, PH_MAX, TEMP_MIN, TEMP_MAX, TAN_MIN, TAN_MAX


class InputPage(AquaPage):
    def __init__(self, stacked_widget, history_page, graph_page, manager):
        super().__init__("Input Parameters", stacked_widget)
        self.history_page = history_page
        self.graph_page   = graph_page
        self.manager      = manager

        self.content_layout.addSpacing(10)

        main_horizontal = QHBoxLayout()
        main_horizontal.setSpacing(20)
        main_horizontal.setContentsMargins(20, 0, 20, 0)

        # ----------------------------------------------------------------
        # Left card — input fields
        # ----------------------------------------------------------------
        input_wrapper    = FrameFactory.create_card_frame((420, 520), 520)
        input_container  = QVBoxLayout(input_wrapper)
        input_container.setContentsMargins(30, 35, 30, 35)
        input_container.setAlignment(Qt.AlignmentFlag.AlignTop)
        input_container.setSpacing(15)

        # Tank / profile name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Tank / Profile name (e.g. Main Tank)")

        # Required parameters
        self.tan_input  = InputFieldFactory.create_validated_input(
            f"TAN — Total Ammonia Nitrogen (0–{TAN_MAX} mg/L)",
            TAN_MIN, TAN_MAX)
        self.ph_input   = InputFieldFactory.create_validated_input(
            f"pH ({PH_MIN}–{PH_MAX})",
            PH_MIN, PH_MAX)
        self.temp_input = InputFieldFactory.create_validated_input(
            f"Temperature ({TEMP_MIN}–{TEMP_MAX} °C)",
            TEMP_MIN, TEMP_MAX)

        # Optional parameters (kH / gH)
        optional_label = QLabel("Optional  —  for logging only")
        optional_label.setFont(QFont("Segoe UI", 9))
        optional_label.setStyleSheet("color: #9CA3AF;")

        self.kh_input = QLineEdit()
        self.kh_input.setPlaceholderText("Carbonate Hardness — kH (°dKH, optional)")
        self.gh_input = QLineEdit()
        self.gh_input.setPlaceholderText("General Hardness — gH (°dGH, optional)")

        for field in (self.name_input, self.tan_input, self.ph_input,
                      self.temp_input, self.kh_input, self.gh_input):
            field.setFont(MAIN_FONT)
            field.setMinimumSize(340, 46)
            field.setMaximumSize(460, 46)
            field.setStyleSheet(INPUT_FIELD_SMALL_STYLE)
            field.returnPressed.connect(self.save_reading)
            input_container.addWidget(field, alignment=Qt.AlignmentFlag.AlignCenter)

        input_container.insertWidget(4, optional_label,
                                     alignment=Qt.AlignmentFlag.AlignCenter)

        self.save_button = ButtonFactory.create_success_button("Save Reading", MAIN_FONT)
        self.save_button.clicked.connect(self.save_reading)
        input_container.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.feedback = QLabel("")
        self.feedback.setFont(MAIN_FONT)
        self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback.setWordWrap(True)
        self.feedback.setStyleSheet("color: #06B6D4; font-weight: 500;")
        input_container.addWidget(self.feedback)

        # ----------------------------------------------------------------
        # Right card — parameter guide (scrollable)
        # ----------------------------------------------------------------
        guide_container  = FrameFactory.create_card_frame((420, 520), 520)
        guide_main_layout = QVBoxLayout(guide_container)
        guide_main_layout.setContentsMargins(15, 15, 15, 15)
        guide_main_layout.setSpacing(10)

        guide_title = QLabel("Water Parameter Guide")
        guide_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        guide_title.setStyleSheet("color: #FFFFFF; padding: 5px; background: transparent;")
        guide_main_layout.addWidget(guide_title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(SCROLLBAR_STYLE)

        scroll_content = QFrame()
        scroll_content.setStyleSheet("background: transparent; border: none;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)

        scroll_layout.addWidget(FrameFactory.create_guide_section(
            "Tank / Profile Name",
            "A unique label for each display tank (e.g. 'Main Tank', 'Betta Tank'). "
            "Each name must be unique per user.",
            "• Must contain letters (not only digits)\n"
            "• Used to track readings per tank separately"
        ))
        scroll_layout.addWidget(FrameFactory.create_guide_section(
            f"TAN — Total Ammonia Nitrogen  (0–{TAN_MAX} mg/L)",
            "The total ammonia measured by your liquid or colorimetric test kit. "
            "Includes both ionised NH₄⁺ and un-ionised NH₃. "
            "The system converts this to toxic NH₃ using the Emerson (1975) formula.",
            "• Safe TAN: < 0.5 mg/L in a healthy cycled tank\n"
            "• Always test alongside pH and Temperature"
        ))
        scroll_layout.addWidget(FrameFactory.create_guide_section(
            f"pH  ({PH_MIN}–{PH_MAX})",
            "Governs what fraction of TAN is in the toxic NH₃ form. "
            "Higher pH = more toxic NH₃ at the same TAN level. "
            "Most freshwater fish: pH 6.5–7.5.",
            "• Too low? Add pH buffer or reduce CO₂\n"
            "• Too high? Perform partial water change"
        ))
        scroll_layout.addWidget(FrameFactory.create_guide_section(
            f"Temperature  ({TEMP_MIN}–{TEMP_MAX} °C)",
            "Higher temperature increases NH₃ toxicity at the same TAN and pH. "
            "Tropical fish: 24–28 °C. Coldwater fish: 18–22 °C.",
            "• Too low? Increase heater temperature\n"
            "• Too high? Improve ventilation or add chiller"
        ))
        scroll_layout.addWidget(FrameFactory.create_guide_section(
            "kH / gH  (optional, logged only)",
            "Carbonate Hardness (kH) and General Hardness (gH) are recorded "
            "for historical reference. They do not affect the NH₃ calculation.",
            "• kH: buffering capacity, ideally 4–8 °dKH\n"
            "• gH: total dissolved minerals, ideally 4–12 °dGH"
        ))

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        guide_main_layout.addWidget(scroll_area)

        main_horizontal.addWidget(input_wrapper)
        main_horizontal.addWidget(guide_container)
        self.content_layout.addLayout(main_horizontal)
        self.content_layout.addStretch()

    # ----------------------------------------------------------------
    # Save logic
    # ----------------------------------------------------------------

    def save_reading(self):
        name = self.name_input.text().strip()

        # --- Validate name ------------------------------------------
        valid, msg = ValidationHelper.validate_not_empty(name, "Tank name")
        if not valid:
            self._show_error(msg); return

        valid, msg = ValidationHelper.validate_not_numeric_only(name, "Tank name")
        if not valid:
            self._show_error(msg); return

        # --- Required numeric fields --------------------------------
        missing = []
        if not self.tan_input.text().strip():  missing.append("TAN")
        if not self.ph_input.text().strip():   missing.append("pH")
        if not self.temp_input.text().strip(): missing.append("Temperature")

        if missing:
            self._show_error(f"Please enter: {', '.join(missing)}.")
            return

        try:
            tan  = float(self.tan_input.text())
            ph   = float(self.ph_input.text())
            temp = float(self.temp_input.text())
        except ValueError:
            self._show_error("TAN, pH and Temperature must be valid numbers.")
            return

        # --- Optional kH / gH ---------------------------------------
        kh = gh = None
        try:
            kh_text = self.kh_input.text().strip()
            gh_text = self.gh_input.text().strip()
            if kh_text: kh = float(kh_text)
            if gh_text: gh = float(gh_text)
        except ValueError:
            self._show_error("kH and gH must be valid numbers if provided.")
            return

        # --- AmmoniaEngine calculation --------------------------------
        try:
            result = AmmoniaEngine.calculate(tan, ph, temp)
        except ValueError as e:
            self._show_error(str(e))
            return

        # --- Persist to SQLite ----------------------------------------
        reading = WaterReading(
            tank_name   = name,
            tan         = tan,
            ph          = ph,
            temperature = temp,
            nh3         = round(result.nh3, 6),
            toxicity    = result.toxicity,
            kh          = kh,
            gh          = gh,
        )
        self.manager.add_reading(reading)

        readings = self.manager.get_all()

        # --- Update linked pages -------------------------------------
        self.history_page.update_table(readings)
        self.graph_page.update_graph(readings, selected_name=name)

        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "home_page"):
            parent.home_page.update_latest(readings)

        # --- Clear form -----------------------------------------------
        for field in (self.name_input, self.tan_input, self.ph_input,
                      self.temp_input, self.kh_input, self.gh_input):
            field.clear()

        # Show result inline
        tox_color = {"Safe": "#66BB6A", "Caution": "#FFA726",
                     "Critical Toxic": "#EF5350"}.get(result.toxicity, "#06B6D4")
        self.feedback.setStyleSheet(f"color: {tox_color}; font-weight: 600;")
        self.feedback.setText(
            f"Saved ✔  |  NH₃: {result.nh3:.4f} mg/L  |  {result.toxicity}  "
            f"| {result.inference_ms:.2f} ms"
        )
        QTimer.singleShot(4000, lambda: self.feedback.clear())

    def _show_error(self, msg: str):
        self.feedback.setText(msg)
        self.feedback.setStyleSheet("color: #EF5350; font-weight: 500;")
