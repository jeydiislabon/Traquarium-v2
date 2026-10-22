# ui/dialogs.py
"""Dialog windows"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .constants import PRIMARY_COLOR, ACCENT_COLOR, BG_GRADIENT_TOP, BG_GRADIENT_BOTTOM


class AboutDialog(QDialog):
    """About Traquarium dialog -- v2 with updated content."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Traquarium")
        self.setFixedSize(660, 560)
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {BG_GRADIENT_TOP}, stop:1 {BG_GRADIENT_BOTTOM});
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("About Traquarium")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                background: #CAE9FF; width: 12px; border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #5FA8D3; border-radius: 6px;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(12)

        _BOX = ("color: #FFFFFF; padding: 10px; "
                "background-color: rgba(27, 73, 101, 0.7); "
                "border: 2px solid #5FA8D3; border-radius: 8px;")

        # --- About section ---
        about_lbl = QLabel()
        about_lbl.setWordWrap(True)
        about_lbl.setFont(QFont("Segoe UI", 10))
        about_lbl.setStyleSheet(_BOX)
        about_lbl.setText("""
<b style='font-size: 14pt; color: #5FA8D3;'>About Traquarium v2</b><br><br>

<b style='color: #CAE9FF;'>What is Traquarium?</b><br>
Traquarium is an offline desktop decision support system for small-scale freshwater
aquatic retail facilities. It accepts manual water parameter measurements
(TAN, pH, Temperature) from standard liquid or colorimetric test kits, computes
the toxic un-ionized ammonia (NH3) concentration using the Emerson et al. (1975)
thermodynamic equilibrium model, classifies the toxicity level, and generates
step-by-step chemical dosing instructions.<br><br>

<b style='color: #CAE9FF;'>How to Use the Program:</b><br><br>

<b>1. Home Dashboard</b><br>
Displays an overview of your latest readings, stat cards for pH, Temperature,
and NH3, a bar chart of the most recent entry, and a toxicity indicator.<br><br>

<b>2. Input Page</b><br>
Enter a tank name, TAN (mg/L), pH (6.0-9.0), and Temperature (15-35 deg C).
The system computes pKa, NH3 fraction, NH3 concentration in mg/L, and
toxicity classification on each save. Results are shown immediately on the
right-side computation panel.<br><br>

<b>3. History Page</b><br>
View all readings with colour-coded toxicity rows (green/amber/red).
Click a row then open Details to see dosing instructions and parameter warnings.
Edit (recalculates NH3 automatically) or delete individual readings.<br><br>

<b>4. Graph Page</b><br>
Select a tank from History to visualise TAN, pH, Temperature, and NH3 as a
grouped bar chart across all readings for that tank.<br><br>

<b style='color: #CAE9FF;'>Key Features:</b><br>
- Multi-user support - each user has a separate SQLite database<br>
- Emerson (1975) NH3 equilibrium engine with sub-millisecond inference<br>
- PSO multi-tank water change optimization engine<br>
- Offline only - no internet or subscription required
""")
        content_layout.addWidget(about_lbl)

        # --- Science section ---
        science_lbl = QLabel()
        science_lbl.setWordWrap(True)
        science_lbl.setFont(QFont("Segoe UI", 10))
        science_lbl.setStyleSheet(_BOX)
        science_lbl.setText("""
<b style='font-size: 14pt; color: #5FA8D3;'>Water Parameter Guide</b><br><br>

<b style='color: #CAE9FF;'>TAN - Total Ammonia Nitrogen (0-10 mg/L)</b><br>
The total ammonia measured from your test kit. Includes both ionised NH4+ and
un-ionised NH3. The engine converts this to toxic NH3 using pH and temperature.<br>
Safe cycled tank: TAN near 0 mg/L.<br><br>

<b style='color: #CAE9FF;'>pH (6.0 - 9.0)</b><br>
Governs what fraction of TAN becomes toxic NH3. Higher pH = more toxic NH3.
Most freshwater fish: pH 6.5-7.5.<br>
- Too low: add pH buffer or reduce CO2<br>
- Too high: perform partial water change<br><br>

<b style='color: #CAE9FF;'>Temperature (15 - 35 deg C)</b><br>
Higher temperature increases NH3 toxicity at the same TAN and pH.
Tropical fish: 24-28 deg C. Coldwater fish: 18-22 deg C.<br>
- Too low: raise heater temperature<br>
- Too high: improve ventilation or add chiller<br><br>

<b style='color: #CAE9FF;'>NH3 Toxicity Thresholds (Emerson et al., 1975)</b><br>
- Safe:           NH3 below 0.02 mg/L<br>
- Caution:        0.02 to 0.05 mg/L<br>
- Critical Toxic: 0.05 mg/L and above
""")
        content_layout.addWidget(science_lbl)

        # --- Technical section ---
        tech_lbl = QLabel()
        tech_lbl.setWordWrap(True)
        tech_lbl.setFont(QFont("Segoe UI", 10))
        tech_lbl.setStyleSheet(_BOX)
        tech_lbl.setText("""
<b style='font-size: 14pt; color: #5FA8D3;'>Technical Information</b><br><br>

<b style='color: #CAE9FF;'>Technology Stack</b><br>
- Python 3.8+ - Core language<br>
- PyQt6 - Cross-platform GUI framework<br>
- PyQtGraph - Scientific bar chart rendering<br>
- SQLite (stdlib sqlite3) - ACID-compliant local database<br>
- NumPy - Array operations for PSO and graphing<br><br>

<b style='color: #CAE9FF;'>Data Storage</b><br>
- Per-user SQLite database at users/username/readings.db<br>
- Schema: id, timestamp, tank_name, tan, ph, temperature, nh3, toxicity, kh, gh<br>
- No internet connection required - fully offline<br><br>

<b style='color: #CAE9FF;'>System Requirements</b><br>
- Python 3.8 or higher<br>
- Windows, macOS, or Linux<br>
- Minimum 100 MB free disk space<br>
- Screen resolution: 1050x750 or higher<br><br>

<b style='color: #CAE9FF;'>Developer</b><br>
Eslabon, John Donald S.<br>
Technological Institute of the Philippines - Quezon City<br>
CPE025A | CPE31S1A - Major (Capstone) Design Experience<br>
1st Semester, SY 2026-2027<br><br>

<b style='color: #CAE9FF;'>References</b><br>
Emerson et al. (1975). Aqueous ammonia equilibrium calculations.
Journal of the Fisheries Research Board of Canada, 32(12), 2379-2383.<br>
Kennedy and Eberhart (1995). Particle swarm optimization. ICNN'95.<br><br>

<i style='color: #A8DADC;'>Traquarium v2.0.0 | 2026 | Eslabon, John Donald S.</i>
""")
        content_layout.addWidget(tech_lbl)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #5FA8D3; color: #FFFFFF;
                padding: 10px 30px; border-radius: 8px; font-weight: bold;
            }
            QPushButton:hover { background-color: #4A90BA; }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
