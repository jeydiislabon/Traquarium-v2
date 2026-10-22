# pages/home_page.py
"""Dashboard/Home page with modern sidebar layout"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QColor, QPainterPath
from datetime import datetime
import pyqtgraph as pg
import numpy as np


class HomePage(QWidget):
    def __init__(self, stacked_widget, manager, username):
        super().__init__()
        self.username = username
        self.manager = manager
        self.stacked_widget = stacked_widget
        self.readings = []

        # Main horizontal layout (sidebar + content)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Center Content Area
        content_area = QWidget()
        content_area.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Header with welcome message
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        self.title_label = QLabel(f"Welcome back, {self.username}!")
        self.title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Light))
        self.title_label.setStyleSheet("color: #E8E8E8;")
        header_layout.addWidget(self.title_label)
        
        # Subtitle with quick info
        self.subtitle_label = QLabel("Here's your aquarium overview")
        self.subtitle_label.setFont(QFont("Segoe UI", 12))
        self.subtitle_label.setStyleSheet("color: #B8B8B8;")
        header_layout.addWidget(self.subtitle_label)
        
        content_layout.addLayout(header_layout)
        
        # Quick stats summary
        self.summary_card = QFrame()
        self.summary_card.setFixedHeight(80)
        self.summary_card.setStyleSheet("""
            QFrame {
                background: rgba(43, 62, 80, 0.4);
                border-radius: 12px;
                border: 2px solid #4A5F7F;
            }
        """)
        summary_layout = QHBoxLayout(self.summary_card)
        summary_layout.setContentsMargins(20, 15, 20, 15)
        summary_layout.setSpacing(40)
        
        # Total readings
        self.total_readings_label = QLabel("0\nTotal Readings")
        self.total_readings_label.setFont(QFont("Segoe UI", 12))
        self.total_readings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_readings_label.setStyleSheet("color: #FFFFFF; line-height: 1.5;")
        summary_layout.addWidget(self.total_readings_label)
        
        # Separator
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.VLine)
        sep1.setStyleSheet("background: rgba(255, 255, 255, 0.2);")
        sep1.setFixedWidth(2)
        summary_layout.addWidget(sep1)
        
        # Profiles tracked
        self.profiles_label = QLabel("0\nProfiles Tracked")
        self.profiles_label.setFont(QFont("Segoe UI", 12))
        self.profiles_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profiles_label.setStyleSheet("color: #FFFFFF;")
        summary_layout.addWidget(self.profiles_label)
        
        # Separator
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.VLine)
        sep2.setStyleSheet("background: rgba(255, 255, 255, 0.2);")
        sep2.setFixedWidth(2)
        summary_layout.addWidget(sep2)
        
        # Last updated
        self.last_updated_label = QLabel("Never\nLast Updated")
        self.last_updated_label.setFont(QFont("Segoe UI", 12))
        self.last_updated_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.last_updated_label.setStyleSheet("color: #FFFFFF;")
        summary_layout.addWidget(self.last_updated_label)
        
        content_layout.addWidget(self.summary_card)

        # Graph visualization area
        self.graph_card = QFrame()
        self.graph_card.setFixedHeight(280)
        self.graph_card.setStyleSheet("""
            QFrame {
                background: rgba(43, 62, 80, 0.6);
                border-radius: 16px;
                border: 2px solid #4A5F7F;
            }
        """)
        
        graph_layout = QVBoxLayout(self.graph_card)
        graph_layout.setContentsMargins(15, 15, 15, 15)
        
        # Title for graph
        graph_title = QLabel("Latest Water Parameters")
        graph_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Normal))
        graph_title.setStyleSheet("color: #B8B8B8;")
        graph_layout.addWidget(graph_title)
        
        # Bar graph widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground((62, 78, 94, 100))
        self.plot_widget.setLabel("left", "Value", color="#B8B8B8", **{"font-size": "10pt"})
        self.plot_widget.showGrid(x=False, y=True, alpha=0.2)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.getAxis('bottom').setTicks([[(0, 'pH'), (1, 'Temp'), (2, 'Ammonia')]])
        self.plot_widget.getAxis('bottom').setStyle(tickTextOffset=10)
        self.plot_widget.getAxis('bottom').setPen(color=(184, 184, 184))
        self.plot_widget.getAxis('left').setPen(color=(184, 184, 184))
        graph_layout.addWidget(self.plot_widget)
        
        content_layout.addWidget(self.graph_card)
        
        # Add spacing between graph and stats cards
        content_layout.addSpacing(60)

        # Stats cards in a row
        stats_layout = QGridLayout()
        stats_layout.setSpacing(30)
        stats_layout.setContentsMargins(0, 20, 0, 0)

        self.ph_card = self.create_stat_card("--", "pH Level", "No data", "#7E87E1")
        self.temp_card = self.create_stat_card("--", "Temperature", "No data", "#EF5350")
        self.ammonia_card = self.create_stat_card("--", "Ammonia", "No data", "#26C6DA")

        stats_layout.addWidget(self.ph_card, 0, 0)
        stats_layout.addWidget(self.temp_card, 0, 1)
        stats_layout.addWidget(self.ammonia_card, 0, 2)

        content_layout.addLayout(stats_layout)
        content_layout.addStretch()

        main_layout.addWidget(content_area, 1)

        self.update_latest(self.manager.get_all())

    def create_sidebar(self):
        """Create the left sidebar with user info and navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #293438,
                    stop:1 #1D2429);
                border: none;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 30, 0, 30)
        layout.setSpacing(0)

        # User profile section
        user_container = QWidget()
        user_container.setStyleSheet("background: transparent;")
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(20, 10, 20, 10)
        
        # Profile picture with default user icon
        profile_pic = QLabel("👤")
        profile_pic.setFixedSize(40, 40)
        profile_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_pic.setFont(QFont("Segoe UI", 18))
        profile_pic.setStyleSheet("""
            QLabel {
                background: #242C30;
                border-radius: 20px;
                border: 2px solid rgba(255, 255, 255, 0.2);
                color: #FFFFFF;
            }
        """)
        user_layout.addWidget(profile_pic)
        
        # Username
        username_label = QLabel(self.username)
        username_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        username_label.setStyleSheet("color: #FFFFFF;")
        user_layout.addWidget(username_label)
        
        # Online indicator
        online_dot = QLabel("●")
        online_dot.setFont(QFont("Segoe UI", 10))
        online_dot.setStyleSheet("color: #66BB6A;")
        user_layout.addWidget(online_dot)
        
        layout.addWidget(user_container)
        layout.addSpacing(20)

        # Navigation buttons
        nav_buttons = [
            ("", "Overview", 3),
        ]

        for icon, text, page_idx in nav_buttons:
            btn = self.create_nav_button(icon, text, page_idx)
            layout.addWidget(btn)

        layout.addSpacing(30)

        # Add New Reading / Go to Input button (changes based on data)
        self.add_btn = QPushButton("+ Add New Reading")
        self.add_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.add_btn.setFixedHeight(45)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #242C30,
                    stop:1 #1D2429);
                color: #FFFFFF;
                border-radius: 10px;
                border: none;
                margin: 0 15px;
                text-align: left;
                padding-left: 15px;
                outline: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #293438,
                    stop:1 #242C30);
            }
            QPushButton:pressed {
                background: #0F1314;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.add_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.add_btn)

        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("← Logout")
        logout_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Normal))
        logout_btn.setFixedHeight(40)
        logout_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #EF5350;
                border: none;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                text-align: left;
                padding-left: 24px;
            }
            QPushButton:hover {
                background: rgba(239, 83, 80, 0.1);
                color: #FF6B6B;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(logout_btn)
        
        # About Us button at the bottom
        about_btn = QPushButton("? About Us")
        about_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Normal))
        about_btn.setFixedHeight(40)
        about_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #9CA3AF;
                border: none;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                text-align: left;
                padding-left: 24px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.05);
                color: #FFFFFF;
            }
        """)
        about_btn.clicked.connect(self.show_about)
        about_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(about_btn)
        
        return sidebar
    
    def show_about(self):
        """Show About dialog"""
        from ui.dialogs import AboutDialog
        dialog = AboutDialog(self)
        dialog.exec()
    
    def logout(self):
        """Logout and return to login page"""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            'Logout',
            'Are you sure you want to logout?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear login page fields
            login_page = self.stacked_widget.widget(1)
            if login_page:
                login_page.username_input.clear()
                login_page.password_input.clear()
                login_page.feedback_label.clear()
            
            # Go back to login page
            self.stacked_widget.setCurrentIndex(1)

    def create_nav_button(self, icon, text, page_idx):
        """Create a navigation button for the sidebar"""
        btn = QPushButton(f"{icon}  {text}")
        btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Normal))
        btn.setFixedHeight(50)
        
        is_active = (text == "Overview")
        
        if is_active:
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(36, 44, 48, 0.5);
                    color: #FFFFFF;
                    border: none;
                    border-left: 4px solid #242C30;
                    text-align: left;
                    padding-left: 20px;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #B8B8B8;
                    border: none;
                    text-align: left;
                    padding-left: 24px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.05);
                    color: #FFFFFF;
                }
            """)
        
        btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(page_idx))
        
        # Only show pointer cursor if not the active page
        if not is_active:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        return btn

    def create_stat_card(self, value, label, detail, color):
        """Create a clean circular statistics card widget with hover animation"""
        card = QFrame()
        card.setFixedSize(180, 200)
        card.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        
        # Store original position for animation
        card.original_y = 0
        card.is_hovered = False
        
        # Enable mouse tracking for hover effects
        card.setMouseTracking(True)
        
        # Override enter/leave events for floating animation
        def enterEvent(event):
            card.is_hovered = True
            # Move up by 10 pixels for floating effect
            current_pos = card.pos()
            card.move(current_pos.x(), current_pos.y() - 10)
            card.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 15px;
                }
            """)
        
        def leaveEvent(event):
            card.is_hovered = False
            # Move back to original position
            current_pos = card.pos()
            card.move(current_pos.x(), current_pos.y() + 10)
            card.setStyleSheet("""
                QFrame {
                    background: transparent;
                    border: none;
                }
            """)
        
        card.enterEvent = enterEvent
        card.leaveEvent = leaveEvent

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        # Circular progress container
        circle_container = QFrame()
        circle_container.setFixedSize(120, 120)
        circle_container.setStyleSheet(f"""
            QFrame {{
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                    fx:0.5, fy:0.5,
                    stop:0 {color},
                    stop:0.65 {color},
                    stop:0.66 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.03));
                border-radius: 60px;
            }}
        """)
        
        circle_layout = QVBoxLayout(circle_container)
        circle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #FFFFFF;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setObjectName("value")
        circle_layout.addWidget(value_label)
        
        layout.addWidget(circle_container, 0, Qt.AlignmentFlag.AlignCenter)

        text_label = QLabel(label)
        text_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        text_label.setStyleSheet("color: #E8E8E8;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label)
        
        detail_label = QLabel(detail)
        detail_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Normal))
        detail_label.setStyleSheet("color: #808080;")
        detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detail_label.setObjectName("detail")
        layout.addWidget(detail_label)

        return card

    def update_latest(self, readings):
        """Update display with the latest saved reading and stats."""
        self.readings = readings
        
        if not readings:
            self.plot_widget.clear()
            # Update summary with no data
            self.total_readings_label.setText("0\nTotal Readings")
            self.profiles_label.setText("0\nProfiles Tracked")
            self.last_updated_label.setText("Never\nLast Updated")
            self.subtitle_label.setText("No readings yet. Add your first reading to get started!")
            # Change button to "Add New Reading" when no data
            self.add_btn.setText("+ Add New Reading")
            return

        # Update summary stats
        total = len(readings)
        unique_profiles = len(set(r["name"] for r in readings))
        
        self.total_readings_label.setText(f"{total}\nTotal Readings")
        self.profiles_label.setText(f"{unique_profiles}\nProfiles Tracked")
        
        # Format last updated time
        latest = readings[-1]
        try:
            last_time = datetime.strptime(latest["timestamp"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            last_time = datetime.strptime(latest["timestamp"], "%Y-%m-%d %H:%M")
        
        time_str = last_time.strftime("%b %d, %I:%M %p")
        self.last_updated_label.setText(f"{time_str}\nLast Updated")
        self.subtitle_label.setText(f"Monitoring {unique_profiles} aquarium{'s' if unique_profiles != 1 else ''}")
        
        # Change button to "Go to Input" when there is data
        self.add_btn.setText("→ Go to Input")

        # Update graph with latest reading only
        ph = float(latest["pH"])
        temp = float(latest["temperature"])
        ammonia = float(latest["ammonia"])
        
        # Clear and create bar graph
        self.plot_widget.clear()
        
        x = np.array([0, 1, 2])
        heights = np.array([ph, temp, ammonia])
        colors = [(126, 135, 225), (239, 83, 80), (38, 198, 218)]
        
        # Create bars
        for i in range(3):
            bar = pg.BarGraphItem(x=[x[i]], height=[heights[i]], width=0.6, brush=colors[i])
            self.plot_widget.addItem(bar)

        # Update stats cards
        if total > 1:
            try:
                first_date = datetime.strptime(readings[0]["timestamp"], "%Y-%m-%d %H:%M:%S")
                last_date = datetime.strptime(readings[-1]["timestamp"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                first_date = datetime.strptime(readings[0]["timestamp"], "%Y-%m-%d %H:%M")
                last_date = datetime.strptime(readings[-1]["timestamp"], "%Y-%m-%d %H:%M")
            days = (last_date - first_date).days + 1
        else:
            days = 1

        avg_ph = sum(float(r["pH"]) for r in readings) / total
        avg_temp = sum(float(r["temperature"]) for r in readings) / total

        self.update_stats(total, days, avg_ph, avg_temp)

    def update_stats(self, total, days, avg_ph, avg_temp):
        """Update statistics cards with latest reading data"""
        if not self.readings:
            return
            
        latest = self.readings[-1]
        
        # Update pH card
        ph_val = latest["pH"]
        self.ph_card.findChild(QLabel, "value").setText(str(ph_val))
        self.ph_card.findChild(QLabel, "detail").setText("Latest reading")
        
        # Update Temperature card
        temp_val = latest["temperature"]
        self.temp_card.findChild(QLabel, "value").setText(str(temp_val))
        self.temp_card.findChild(QLabel, "detail").setText("°C")
        
        # Update Ammonia card
        ammonia_val = latest["ammonia"]
        self.ammonia_card.findChild(QLabel, "value").setText(str(ammonia_val))
        self.ammonia_card.findChild(QLabel, "detail").setText("ppm")

    def paintEvent(self, event):
        from ui.helpers import PaintHelper
        PaintHelper.paint_blue_gradient(self, event)
        super().paintEvent(event)
