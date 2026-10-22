# pages/input_page.py
"""Input page -- TAN, pH, Temperature -> AmmoniaEngine -> computation result panel."""

from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QHBoxLayout, QVBoxLayout,
    QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from ui.base_page import AquaPage
from ui.constants import MAIN_FONT
from ui.components import ButtonFactory, InputFieldFactory, FrameFactory
from ui.styles import INPUT_FIELD_SMALL_STYLE, SCROLLBAR_STYLE
from ui.helpers import ValidationHelper
from data_model import WaterReading
from ammonia_engine import AmmoniaEngine, PH_MIN, PH_MAX, TEMP_MIN, TEMP_MAX, TAN_MIN, TAN_MAX


# Toxicity display config
_TOX_CFG = {
    "Safe":           {"color": "#10B981", "bg": "#064E3B", "label": "SAFE"},
    "Caution":        {"color": "#F59E0B", "bg": "#451A03", "label": "CAUTION"},
    "Critical Toxic": {"color": "#EF4444", "bg": "#450A0A", "label": "CRITICAL TOXIC"},
}


class InputPage(AquaPage):
    def __init__(self, stacked_widget, history_page, graph_page, manager):
        super().__init__("Input Parameters", stacked_widget)
        self.history_page = history_page
        self.graph_page   = graph_page
        self.manager      = manager

        self.content_layout.addSpacing(8)

        # ----------------------------------------------------------------
        # Main horizontal split: left = form, right = result + guide
        # ----------------------------------------------------------------
        main_h = QHBoxLayout()
        main_h.setSpacing(16)
        main_h.setContentsMargins(20, 0, 20, 0)

        # ---- LEFT: input form ------------------------------------------
        form_card = FrameFactory.create_card_frame((380, 440), 460)
        form_lay  = QVBoxLayout(form_card)
        form_lay.setContentsMargins(28, 30, 28, 30)
        form_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_lay.setSpacing(14)

        form_title = QLabel("Enter Water Parameters")
        form_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        form_title.setStyleSheet("color: #E8E8E8;")
        form_lay.addWidget(form_title)

        # Tank name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Tank / Profile name  (e.g. Main Tank)")

        # Required parameters - validator uses Intermediate for partial input
        self.tan_input  = InputFieldFactory.create_validated_input(
            f"TAN -- Total Ammonia Nitrogen  (0 - {TAN_MAX} mg/L)",
            TAN_MIN, TAN_MAX, 4)
        self.ph_input   = InputFieldFactory.create_validated_input(
            f"pH  ({PH_MIN} - {PH_MAX})",
            PH_MIN, PH_MAX, 2)
        self.temp_input = InputFieldFactory.create_validated_input(
            f"Temperature  ({TEMP_MIN} - {TEMP_MAX} degrees C)",
            TEMP_MIN, TEMP_MAX, 2)

        for field in (self.name_input, self.tan_input, self.ph_input, self.temp_input):
            field.setFont(MAIN_FONT)
            field.setMinimumSize(300, 46)
            field.setMaximumSize(420, 46)
            field.setStyleSheet(INPUT_FIELD_SMALL_STYLE)
            field.returnPressed.connect(self.save_reading)
            form_lay.addWidget(field, alignment=Qt.AlignmentFlag.AlignCenter)

        self.save_btn = ButtonFactory.create_success_button("Save Reading", MAIN_FONT)
        self.save_btn.setMinimumHeight(46)
        self.save_btn.clicked.connect(self.save_reading)
        form_lay.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.form_feedback = QLabel("")
        self.form_feedback.setFont(QFont("Segoe UI", 10))
        self.form_feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.form_feedback.setWordWrap(True)
        self.form_feedback.setStyleSheet("color: #EF5350;")
        form_lay.addWidget(self.form_feedback)

        # ---- RIGHT: result panel + guide (stacked vertically) ----------
        right_v = QVBoxLayout()
        right_v.setSpacing(12)

        # Computation result card
        self.result_card = FrameFactory.create_card_frame((380, 200), 520)
        result_lay = QVBoxLayout(self.result_card)
        result_lay.setContentsMargins(24, 20, 24, 20)
        result_lay.setSpacing(10)

        res_header = QLabel("NH3 Computation Result")
        res_header.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        res_header.setStyleSheet("color: #E8E8E8;")
        result_lay.addWidget(res_header)

        # Grid: label | value
        grid = QGridLayout()
        grid.setSpacing(8)
        grid.setColumnStretch(1, 1)

        self._lbl_pka   = self._make_val_label("--")
        self._lbl_frac  = self._make_val_label("--")
        self._lbl_nh3   = self._make_val_label("--", big=True)
        self._lbl_tox   = self._make_val_label("--", big=True)
        self._lbl_infer = self._make_val_label("--")
        self._lbl_inst  = QLabel("--")
        self._lbl_inst.setFont(QFont("Segoe UI", 9))
        self._lbl_inst.setStyleSheet("color: #9CA3AF;")
        self._lbl_inst.setWordWrap(True)

        rows = [
            ("pKa",              self._lbl_pka),
            ("NH3 Fraction",     self._lbl_frac),
            ("NH3 (mg/L)",       self._lbl_nh3),
            ("Toxicity Level",   self._lbl_tox),
            ("Inference Time",   self._lbl_infer),
            ("Next Action",      self._lbl_inst),
        ]
        for i, (name, widget) in enumerate(rows):
            key_lbl = QLabel(name)
            key_lbl.setFont(QFont("Segoe UI", 10))
            key_lbl.setStyleSheet("color: #9CA3AF;")
            grid.addWidget(key_lbl, i, 0)
            grid.addWidget(widget,  i, 1)

        result_lay.addLayout(grid)
        right_v.addWidget(self.result_card)

        # Guide card (scrollable)
        guide_card   = FrameFactory.create_card_frame((380, 180), 520)
        guide_outer  = QVBoxLayout(guide_card)
        guide_outer.setContentsMargins(14, 14, 14, 14)
        guide_outer.setSpacing(8)

        guide_title = QLabel("Water Parameter Guide")
        guide_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        guide_title.setStyleSheet("color: #E8E8E8; background: transparent;")
        guide_outer.addWidget(guide_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(SCROLLBAR_STYLE)

        scroll_inner = QFrame()
        scroll_inner.setStyleSheet("background: transparent; border: none;")
        scroll_lay = QVBoxLayout(scroll_inner)
        scroll_lay.setSpacing(8)

        scroll_lay.addWidget(FrameFactory.create_guide_section(
            f"TAN  (0 - {TAN_MAX} mg/L)",
            "Total Ammonia Nitrogen from your liquid or strip test kit. "
            "The engine converts this to toxic NH3 using pH and temperature.",
            "Safe cycled tank: TAN near 0 mg/L. Always test all three together."
        ))
        scroll_lay.addWidget(FrameFactory.create_guide_section(
            f"pH  ({PH_MIN} - {PH_MAX})",
            "Higher pH = more of TAN converts to toxic NH3. "
            "Most freshwater fish: pH 6.5 - 7.5.",
            "Too low: add pH buffer.  Too high: partial water change."
        ))
        scroll_lay.addWidget(FrameFactory.create_guide_section(
            f"Temperature  ({TEMP_MIN} - {TEMP_MAX} degrees C)",
            "Higher temperature increases NH3 toxicity. "
            "Tropical fish: 24 - 28 deg C. Coldwater: 18 - 22 deg C.",
            "Too low: raise heater.  Too high: add chiller or ventilation."
        ))
        scroll_lay.addStretch()

        scroll.setWidget(scroll_inner)
        guide_outer.addWidget(scroll)
        right_v.addWidget(guide_card, stretch=1)

        main_h.addWidget(form_card,  stretch=42)
        main_h.addLayout(right_v,    stretch=58)

        self.content_layout.addLayout(main_h)
        self.content_layout.addStretch()

    # ----------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------

    @staticmethod
    def _make_val_label(text, big=False):
        lbl = QLabel(text)
        size = 13 if big else 11
        weight = QFont.Weight.Bold if big else QFont.Weight.Normal
        lbl.setFont(QFont("Segoe UI", size, weight))
        lbl.setStyleSheet("color: #E8E8E8;")
        lbl.setWordWrap(True)
        return lbl

    def _show_form_error(self, msg):
        self.form_feedback.setStyleSheet("color: #EF5350;")
        self.form_feedback.setText(msg)

    def _clear_result(self):
        for lbl in (self._lbl_pka, self._lbl_frac, self._lbl_nh3,
                    self._lbl_tox, self._lbl_infer, self._lbl_inst):
            lbl.setText("--")
            lbl.setStyleSheet("color: #E8E8E8;")

    # ----------------------------------------------------------------
    # Save / compute
    # ----------------------------------------------------------------

    def save_reading(self):
        self.form_feedback.clear()
        name = self.name_input.text().strip()

        ok, msg = ValidationHelper.validate_not_empty(name, "Tank name")
        if not ok: self._show_form_error(msg); return
        ok, msg = ValidationHelper.validate_not_numeric_only(name, "Tank name")
        if not ok: self._show_form_error(msg); return

        missing = []
        if not self.tan_input.text().strip():  missing.append("TAN")
        if not self.ph_input.text().strip():   missing.append("pH")
        if not self.temp_input.text().strip(): missing.append("Temperature")
        if missing:
            self._show_form_error(f"Please enter: {', '.join(missing)}.")
            return

        try:
            tan  = float(self.tan_input.text())
            ph   = float(self.ph_input.text())
            temp = float(self.temp_input.text())
        except ValueError:
            self._show_form_error("TAN, pH, and Temperature must be valid numbers.")
            return

        # Run AmmoniaEngine
        try:
            result = AmmoniaEngine.calculate(tan, ph, temp)
        except ValueError as e:
            self._show_form_error(str(e))
            return

        # Show computation result
        cfg = _TOX_CFG.get(result.toxicity, {"color": "#E8E8E8", "bg": "#2B3E50", "label": result.toxicity})
        self._lbl_pka.setText(f"{result.pka:.6f}")
        self._lbl_frac.setText(f"{result.fraction:.6f}  ({result.fraction * 100:.4f}%)")
        self._lbl_nh3.setStyleSheet(f"color: {cfg['color']}; font-weight: bold;")
        self._lbl_nh3.setText(f"{result.nh3:.6f} mg/L")
        self._lbl_tox.setStyleSheet(
            f"color: {cfg['color']}; font-weight: bold; "
            f"background: {cfg['bg']}; border-radius: 4px; padding: 2px 6px;")
        self._lbl_tox.setText(cfg["label"])
        self._lbl_infer.setText(f"{result.inference_ms:.3f} ms")
        # First dosing instruction (short)
        first = result.dosing_instructions[0] if result.dosing_instructions else "--"
        self._lbl_inst.setText(first)

        # Persist to SQLite
        reading = WaterReading(
            tank_name   = name,
            tan         = tan,
            ph          = ph,
            temperature = temp,
            nh3         = round(result.nh3, 6),
            toxicity    = result.toxicity,
        )
        self.manager.add_reading(reading)
        readings = self.manager.get_all()

        self.history_page.update_table(readings)
        self.graph_page.update_graph(readings, selected_name=name)

        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "home_page"):
            parent.home_page.update_latest(readings)

        # Clear form inputs
        for field in (self.name_input, self.tan_input, self.ph_input, self.temp_input):
            field.clear()

        self.form_feedback.setStyleSheet("color: #10B981; font-weight: 600;")
        self.form_feedback.setText("Reading saved.")
        QTimer.singleShot(3000, self.form_feedback.clear)
