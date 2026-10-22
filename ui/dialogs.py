# ui/dialogs.py
"""Dialog windows"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .constants import PRIMARY_COLOR, ACCENT_COLOR, BG_GRADIENT_TOP, BG_GRADIENT_BOTTOM


class AboutDialog(QDialog):
    """About Us dialog with team info, GUI description, and parameter explanations"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Traquarium")
        self.setFixedSize(650, 550)
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {BG_GRADIENT_TOP}, stop:1 {BG_GRADIENT_BOTTOM});
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Title
        title = QLabel("🐠 About Traquarium")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(title)

        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #CAE9FF;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #5FA8D3;
                border-radius: 6px;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(12)

        # About the GUI
        about_gui = QLabel()
        about_gui.setWordWrap(True)
        about_gui.setFont(QFont("Segoe UI", 10))
        about_gui.setStyleSheet("color: #FFFFFF; padding: 10px; background-color: rgba(27, 73, 101, 0.7); border: 2px solid #5FA8D3; border-radius: 8px;")
        about_gui.setText("""
<b style='font-size: 14pt; color: #5FA8D3;'>📊 About Traquarium</b><br><br>

<b style='color: #CAE9FF;'>What is Traquarium?</b><br>
Traquarium is a desktop application designed to help aquarium owners monitor and track 
water quality parameters. The program allows users to record pH levels, temperature, 
and ammonia concentrations over time, providing visual analysis and automated warnings 
when parameters fall outside safe ranges.<br><br>

<b style='color: #CAE9FF;'>How to Use the Program:</b><br><br>

<b>1. Home Dashboard</b><br>
• Displays overview of your latest water readings<br>
• Shows circular stat cards for pH, temperature, and ammonia<br>
• Includes a bar graph visualization of your most recent test<br>
• Quick access to add new readings<br><br>

<b>2. Input Page</b><br>
• Enter a profile name for your aquarium (e.g., "Main Tank", "Betta Tank")<br>
• Input three water parameters: pH (0-14), Temperature (0-40°C), Ammonia (0-10 ppm)<br>
• Built-in parameter guide on the right side explains ideal ranges<br>
• Strict validation prevents invalid values from being saved<br>
• Press Enter or click "Save Reading" to store your data<br><br>

<b>3. History Page</b><br>
• View all saved readings in a searchable table<br>
• Search by profile name to filter specific aquariums<br>
• Click any row to see detailed warnings and suggestions<br>
• Edit mode allows you to correct past readings<br>
• Delete unwanted entries<br>
• Color-coded warnings: Green (safe), Yellow (caution), Red (danger)<br><br>

<b>4. Graph Page</b><br>
• Select a profile from History page first<br>
• Visualize all readings for that profile as bar graphs<br>
• Blue bars = pH levels<br>
• Orange bars = Temperature<br>
• Red bars = Ammonia levels<br>
• Info box shows latest reading details<br>
• Perfect for spotting trends and tracking improvements<br><br>

<b style='color: #CAE9FF;'>Key Features:</b><br>
• Multi-user support - Each user has separate data storage<br>
• Automatic warnings - Get alerts when parameters are unsafe<br>
• Data persistence - All readings saved locally in JSON format<br>
• Keyboard shortcuts - Quick navigation (Ctrl+H, Ctrl+1/2/3, F11)<br>
• Offline operation - No internet connection required
        """)
        content_layout.addWidget(about_gui)

        # Parameter Explanations
        params = QLabel()
        params.setWordWrap(True)
        params.setFont(QFont("Segoe UI", 10))
        params.setStyleSheet("color: #FFFFFF; padding: 10px; background-color: rgba(27, 73, 101, 0.7); border: 2px solid #5FA8D3; border-radius: 8px;")
        params.setText("""
<b style='font-size: 14pt; color: #5FA8D3;'>🧪 Water Parameter Guide</b><br><br>

<b style='color: #CAE9FF;'>pH Level (6.5 - 8.0)</b><br>
Measures water acidity/alkalinity. Most freshwater fish thrive in pH 6.5-7.5. 
Marine aquariums typically need 8.0-8.4.<br>
• <b>Too Low:</b> Add pH buffer or reduce CO₂<br>
• <b>Too High:</b> Perform partial water change<br><br>

<b style='color: #CAE9FF;'>Temperature (20-28°C / 68-82°F)</b><br>
Critical for fish metabolism and immune function. Different species need different ranges.
Tropical fish: 24-28°C, Coldwater fish: 18-22°C.<br>
• <b>Too Low:</b> Increase heater temperature<br>
• <b>Too High:</b> Improve ventilation or add cooling<br><br>

<b style='color: #CAE9FF;'>Ammonia (0-0.5 ppm)</b><br>
Highly toxic to fish even in small amounts. Should ideally be 0 ppm in established tanks.
Comes from fish waste, uneaten food, and decaying matter.<br>
• <b>>0.5 ppm:</b> URGENT - Immediate water change required<br>
• <b>0.2-0.5 ppm:</b> Check filter, reduce feeding<br>
        """)
        content_layout.addWidget(params)

        # Team Information
        team = QLabel()
        team.setWordWrap(True)
        team.setFont(QFont("Segoe UI", 10))
        team.setStyleSheet("color: #FFFFFF; padding: 10px; background-color: rgba(27, 73, 101, 0.7); border: 2px solid #5FA8D3; border-radius: 8px;")
        team.setText("""
<b style='font-size: 14pt; color: #5FA8D3;'>💻 Technical Information</b><br><br>

<b style='color: #CAE9FF;'>Technology Stack</b><br>
• <b>Python 3.x</b> - Core programming language for application logic<br>
• <b>PyQt6</b> - Cross-platform GUI framework for desktop applications<br>
• <b>PyQtGraph</b> - Scientific graphics and data visualization library<br>
• <b>JSON</b> - Lightweight data-interchange format for persistent storage<br>
• <b>NumPy</b> - Numerical computing library for data processing<br><br>

<b style='color: #CAE9FF;'>Data Storage</b><br>
• All user data is stored locally on your computer<br>
• Each user has a separate folder in the "users" directory<br>
• Readings are saved in JSON format for easy portability<br>
• No internet connection required - fully offline application<br>
• Your data remains private and secure on your device<br><br>

<b style='color: #CAE9FF;'>System Requirements</b><br>
• Python 3.8 or higher<br>
• Windows, macOS, or Linux operating system<br>
• Minimum 100MB free disk space<br>
• Screen resolution: 1050x750 or higher recommended<br><br>

<b style='color: #CAE9FF;'>Development Team</b><br>
Developed by the Traquarium Team:<br>
• <b>Arindaeng, Paul Daniel</b> - Assistant Programmer<br>
• <b>Dela Cruz, Gabriel</b> - Designer<br>
• <b>Eslabon, John Donald</b> - Lead Programmer<br>
• <b>Garcia, Rain</b> - Co-Lead Programmer<br><br>

<b style='color: #CAE9FF;'>Project Purpose</b><br>
This application was developed to address the practical challenge of tracking 
aquarium water quality over time. Traditional manual record-keeping is prone 
to errors and lacks analytical capabilities. Traquarium provides an automated, 
user-friendly solution with data visualization and intelligent warning systems.<br><br>

<i style='color: #A8DADC;'>Traquarium v1.0.0 | © 2025 Traquarium Team</i>
        """)
        content_layout.addWidget(team)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #5FA8D3;
                color: #FFFFFF;
                padding: 10px 30px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A90BA;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
