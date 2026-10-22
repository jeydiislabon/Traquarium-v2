# pages/home_page.py
"""Dashboard / Home page -- clean redesign with SENSE-style sidebar."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout, QScrollArea,
)
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QFont, QPainter, QLinearGradient, QColor, QPainterPath
from datetime import datetime
import pyqtgraph as pg
import numpy as np


class HomePage(QWidget):
    def __init__(self, stacked_widget, manager, username):
        super().__init__()
        self.username       = username
        self.manager        = manager
        self.stacked_widget = stacked_widget
        self.readings       = []

        # ----------------------------------------------------------------
        # Root layout: sidebar | content
        # ----------------------------------------------------------------
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---- Sidebar ---------------------------------------------------
        self.sidebar = self._build_sidebar()
        root.addWidget(self.sidebar)

        # ---- Content ---------------------------------------------------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent; border: none;")

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_lay = QVBoxLayout(content_widget)
        content_lay.setContentsMargins(36, 32, 36, 32)
        content_lay.setSpacing(24)

        # Header
        self.title_lbl = QLabel(f"Welcome back, {self.username}!")
        self.title_lbl.setFont(QFont("Segoe UI", 26, QFont.Weight.Light))
        self.title_lbl.setStyleSheet("color: #E8E8E8;")

        self.sub_lbl = QLabel("No readings yet. Add your first reading to get started.")
        self.sub_lbl.setFont(QFont("Segoe UI", 12))
        self.sub_lbl.setStyleSheet("color: #9CA3AF;")

        content_lay.addWidget(self.title_lbl)
        content_lay.addWidget(self.sub_lbl)

        # Summary strip
        summary = QFrame()
        summary.setFixedHeight(72)
        summary.setStyleSheet("""
            QFrame {
                background: rgba(43, 62, 80, 0.5);
                border-radius: 12px;
                border: 1.5px solid #4A5F7F;
            }
        """)
        sum_lay = QHBoxLayout(summary)
        sum_lay.setContentsMargins(24, 0, 24, 0)
        sum_lay.setSpacing(32)

        self.lbl_total    = self._summary_item("0", "Total Readings")
        self.lbl_profiles = self._summary_item("0", "Profiles Tracked")
        self.lbl_updated  = self._summary_item("Never", "Last Updated")

        for w in (self.lbl_total, self._vsep(), self.lbl_profiles,
                  self._vsep(), self.lbl_updated):
            sum_lay.addWidget(w)
        sum_lay.addStretch()
        content_lay.addWidget(summary)

        # Graph card
        graph_card = QFrame()
        graph_card.setMinimumHeight(260)
        graph_card.setStyleSheet("""
            QFrame {
                background: rgba(43, 62, 80, 0.55);
                border-radius: 16px;
                border: 1.5px solid #4A5F7F;
            }
        """)
        g_lay = QVBoxLayout(graph_card)
        g_lay.setContentsMargins(18, 14, 18, 14)
        g_lay.setSpacing(6)

        g_title = QLabel("Latest Water Parameters")
        g_title.setFont(QFont("Segoe UI", 11))
        g_title.setStyleSheet("color: #9CA3AF;")
        g_lay.addWidget(g_title)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground((43, 62, 80, 80))
        self.plot_widget.setLabel("left", "Value", color="#9CA3AF", **{"font-size": "9pt"})
        self.plot_widget.showGrid(x=False, y=True, alpha=0.2)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.getAxis("bottom").setTicks(
            [[(0, "TAN"), (1, "pH"), (2, "Temp"), (3, "NH3")]])
        self.plot_widget.getAxis("bottom").setStyle(tickTextOffset=8)
        self.plot_widget.getAxis("bottom").setPen(color=(184, 184, 184))
        self.plot_widget.getAxis("left").setPen(color=(184, 184, 184))
        g_lay.addWidget(self.plot_widget)
        content_lay.addWidget(graph_card)

        # Stat cards row
        cards_lay = QGridLayout()
        cards_lay.setSpacing(20)

        self.ph_card      = self._stat_card("--", "pH Level",     "No data", "#7E87E1")
        self.temp_card    = self._stat_card("--", "Temperature",  "No data", "#EF5350")
        self.nh3_card     = self._stat_card("--", "NH3 (mg/L)",   "No data", "#26C6DA")
        self.toxicity_card = self._stat_card("--", "Toxicity",    "No data", "#F59E0B")

        cards_lay.addWidget(self.ph_card,       0, 0)
        cards_lay.addWidget(self.temp_card,     0, 1)
        cards_lay.addWidget(self.nh3_card,      0, 2)
        cards_lay.addWidget(self.toxicity_card, 0, 3)
        content_lay.addLayout(cards_lay)

        content_lay.addStretch()

        scroll_area.setWidget(content_widget)
        root.addWidget(scroll_area, stretch=1)

        self.update_latest(self.manager.get_all())

    # ----------------------------------------------------------------
    # Sidebar
    # ----------------------------------------------------------------

    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1A2530, stop:1 #131C23);
                border: none;
                border-right: 1px solid rgba(255,255,255,0.06);
            }
        """)
        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(0, 24, 0, 24)
        lay.setSpacing(0)

        # Logo row
        logo_row = QHBoxLayout()
        logo_row.setContentsMargins(20, 0, 20, 0)
        logo_box = QLabel("T")
        logo_box.setFixedSize(36, 36)
        logo_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_box.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        logo_box.setStyleSheet("""
            background: #1B6CA8; color: white;
            border-radius: 8px;
        """)
        brand = QLabel("Traquarium")
        brand.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        brand.setStyleSheet("color: white;")
        logo_row.addWidget(logo_box)
        logo_row.addSpacing(10)
        logo_row.addWidget(brand)
        logo_row.addStretch()
        lay.addLayout(logo_row)

        lay.addSpacing(24)

        # User row
        user_row = QHBoxLayout()
        user_row.setContentsMargins(20, 8, 20, 8)
        avatar = QLabel(self.username[0].upper() if self.username else "U")
        avatar.setFixedSize(34, 34)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        avatar.setStyleSheet("""
            background: #293438; color: white;
            border-radius: 17px;
            border: 1.5px solid rgba(255,255,255,0.2);
        """)
        uname = QLabel(self.username)
        uname.setFont(QFont("Segoe UI", 11))
        uname.setStyleSheet("color: #E8E8E8;")
        dot = QLabel("online")
        dot.setFont(QFont("Segoe UI", 8))
        dot.setStyleSheet("color: #10B981;")

        uv = QVBoxLayout()
        uv.setSpacing(1)
        uv.addWidget(uname)
        uv.addWidget(dot)

        user_row.addWidget(avatar)
        user_row.addSpacing(8)
        user_row.addLayout(uv)
        user_row.addStretch()
        lay.addLayout(user_row)

        lay.addSpacing(16)

        # Section label
        sec = QLabel("NAVIGATION")
        sec.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        sec.setStyleSheet("color: #4A5F7F; letter-spacing: 2px; padding-left: 20px;")
        lay.addWidget(sec)
        lay.addSpacing(6)

        for label, idx in [("Overview", 3), ("Input", 4), ("History", 5), ("Graph", 6)]:
            btn = self._nav_btn(label, idx)
            lay.addWidget(btn)

        lay.addSpacing(20)

        # Input shortcut button
        self.add_btn = QPushButton("+ Add New Reading")
        self.add_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.add_btn.setFixedHeight(40)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background: #1B6CA8; color: white;
                border: none; border-radius: 8px;
                margin: 0 16px; text-align: left; padding-left: 14px;
            }
            QPushButton:hover { background: #1A5F96; }
        """)
        self.add_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        lay.addWidget(self.add_btn)

        lay.addStretch()

        # Bottom: tagline
        tag = QLabel("Your tank data,\nyour decisions.")
        tag.setFont(QFont("Segoe UI", 9))
        tag.setStyleSheet("color: #4A5F7F; padding-left: 20px; padding-bottom: 8px;")
        lay.addWidget(tag)

        # Logout
        logout = QPushButton("Logout")
        logout.setFont(QFont("Segoe UI", 10))
        logout.setFixedHeight(38)
        logout.setStyleSheet("""
            QPushButton {
                background: transparent; color: #EF5350;
                border: none; border-top: 1px solid rgba(255,255,255,0.07);
                text-align: left; padding-left: 20px;
            }
            QPushButton:hover { background: rgba(239,83,80,0.1); color: #FF6B6B; }
        """)
        logout.clicked.connect(self.logout)
        logout.setCursor(Qt.CursorShape.PointingHandCursor)
        lay.addWidget(logout)

        return sidebar

    def _nav_btn(self, label, page_idx):
        btn = QPushButton(label)
        btn.setFont(QFont("Segoe UI", 11))
        btn.setFixedHeight(38)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #9CA3AF;
                border: none; text-align: left;
                padding-left: 20px; border-radius: 0;
            }
            QPushButton:hover { background: rgba(255,255,255,0.05); color: white; }
        """)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(page_idx))
        return btn

    # ----------------------------------------------------------------
    # Summary helpers
    # ----------------------------------------------------------------

    @staticmethod
    def _summary_item(value, label):
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)
        val = QLabel(value)
        val.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        val.setStyleSheet("color: white;")
        val.setObjectName("val")
        lbl = QLabel(label)
        lbl.setFont(QFont("Segoe UI", 9))
        lbl.setStyleSheet("color: #9CA3AF;")
        lay.addWidget(val)
        lay.addWidget(lbl)
        return w

    @staticmethod
    def _vsep():
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedWidth(1)
        sep.setStyleSheet("background: rgba(255,255,255,0.12); border: none;")
        return sep

    # ----------------------------------------------------------------
    # Stat card
    # ----------------------------------------------------------------

    def _stat_card(self, value, label, detail, color):
        card = QFrame()
        card.setMinimumHeight(130)
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(43, 62, 80, 0.55);
                border-radius: 14px;
                border: 1.5px solid #4A5F7F;
            }}
        """)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(6)

        lbl = QLabel(label)
        lbl.setFont(QFont("Segoe UI", 10))
        lbl.setStyleSheet("color: #9CA3AF; background: transparent;")
        lay.addWidget(lbl)

        val = QLabel(value)
        val.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        val.setStyleSheet(f"color: {color}; background: transparent;")
        val.setObjectName("value")
        lay.addWidget(val)

        det = QLabel(detail)
        det.setFont(QFont("Segoe UI", 9))
        det.setStyleSheet("color: #6B7280; background: transparent;")
        det.setObjectName("detail")
        lay.addWidget(det)

        return card

    # ----------------------------------------------------------------
    # Update
    # ----------------------------------------------------------------

    def update_latest(self, readings):
        self.readings = readings

        if not readings:
            self.plot_widget.clear()
            self.lbl_total.findChild(QLabel,    "val").setText("0")
            self.lbl_profiles.findChild(QLabel, "val").setText("0")
            self.lbl_updated.findChild(QLabel,  "val").setText("Never")
            self.sub_lbl.setText("No readings yet. Add your first reading to get started.")
            self.add_btn.setText("+ Add New Reading")
            for card, val in [
                (self.ph_card, "--"), (self.temp_card, "--"),
                (self.nh3_card, "--"), (self.toxicity_card, "--"),
            ]:
                card.findChild(QLabel, "value").setText(val)
                card.findChild(QLabel, "detail").setText("No data")
            return

        total    = len(readings)
        profiles = len(set(r.get("name", r.get("tank_name", "")) for r in readings))
        latest   = readings[-1]

        self.lbl_total.findChild(QLabel,    "val").setText(str(total))
        self.lbl_profiles.findChild(QLabel, "val").setText(str(profiles))

        try:
            ts = latest.get("timestamp", "")
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
            self.lbl_updated.findChild(QLabel, "val").setText(
                dt.strftime("%b %d, %I:%M %p"))
        except Exception:
            self.lbl_updated.findChild(QLabel, "val").setText("--")

        self.sub_lbl.setText(
            f"Monitoring {profiles} aquarium{'s' if profiles != 1 else ''}")
        self.add_btn.setText("Go to Input ->")

        # Bar graph
        tan  = float(latest.get("tan",  0))
        ph   = float(latest.get("pH",   latest.get("ph",  0)))
        temp = float(latest.get("temperature", 0))
        nh3  = float(latest.get("nh3",  0))

        self.plot_widget.clear()
        for i, (height, color) in enumerate([
            (tan,  (56,  189, 248)),
            (ph,   (126, 135, 225)),
            (temp, (239, 83,  80)),
            (nh3,  (239, 68,  68)),
        ]):
            self.plot_widget.addItem(
                pg.BarGraphItem(x=[i], height=[height], width=0.6, brush=color))

        # Stat cards
        tox = str(latest.get("toxicity", "--"))
        tox_colors = {
            "Safe":           "#10B981",
            "Caution":        "#F59E0B",
            "Critical Toxic": "#EF4444",
        }
        tc = tox_colors.get(tox, "#E8E8E8")

        self.ph_card.findChild(QLabel, "value").setText(f"{ph:.2f}")
        self.ph_card.findChild(QLabel, "detail").setText("Latest reading")

        self.temp_card.findChild(QLabel, "value").setText(f"{temp:.1f}")
        self.temp_card.findChild(QLabel, "detail").setText("degrees C")

        self.nh3_card.findChild(QLabel, "value").setText(f"{nh3:.4f}")
        self.nh3_card.findChild(QLabel, "detail").setText("mg/L")

        self.toxicity_card.findChild(QLabel, "value").setStyleSheet(
            f"color: {tc}; background: transparent; font-size: 14px; font-weight: bold;")
        self.toxicity_card.findChild(QLabel, "value").setText(tox)
        self.toxicity_card.findChild(QLabel, "detail").setText("Current level")

    def update_stats(self, *args):
        pass  # folded into update_latest

    def logout(self):
        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "current_user"):
            parent.current_user = None
            parent.manager      = None
        self.stacked_widget.setCurrentIndex(1)

    def show_about(self):
        from ui.dialogs import AboutDialog
        AboutDialog(self).exec()

    def create_nav_button(self, *a):
        pass  # legacy stub

    def create_stat_card(self, *a):
        pass  # legacy stub

    def paintEvent(self, event):
        from ui.helpers import PaintHelper
        PaintHelper.paint_blue_gradient(self, event)
        super().paintEvent(event)
