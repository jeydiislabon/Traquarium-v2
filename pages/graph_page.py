# pages/graph_page.py
"""Graph page -- bar chart of TAN, NH3, pH, and Temperature per tank."""

import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.base_page import AquaPage


class GraphPage(AquaPage):
    def __init__(self, stacked_widget):
        super().__init__("Water Parameter Graph", stacked_widget)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("#0D1545")
        self.plot_widget.setLabel("left",   "Value",         color="#FFFFFF")
        self.plot_widget.setLabel("bottom", "Reading Index", color="#FFFFFF")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.addLegend(offset=(10, 10))
        self.content_layout.addWidget(self.plot_widget, stretch=1)

        self.info_box = QLabel("")
        self.info_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_box.setFont(QFont("Segoe UI", 11))
        from ui.styles import INFO_BOX_STYLE
        self.info_box.setStyleSheet(INFO_BOX_STYLE)
        self.content_layout.addWidget(self.info_box,
                                      alignment=Qt.AlignmentFlag.AlignCenter)

    def update_graph(self, readings, selected_name=None):
        self.plot_widget.clear()

        if not selected_name:
            self.info_box.setText("Select a tank from the History page.")
            return
        if not readings:
            self.info_box.setText("No readings to display.")
            return

        filtered = [r for r in readings
                    if str(r.get("name", r.get("tank_name", ""))).lower()
                    == selected_name.lower()]
        if not filtered:
            self.info_box.setText(f"No data for '{selected_name}'.")
            return

        x    = np.arange(len(filtered))
        tan  = np.array([float(r.get("tan",  0)) for r in filtered])
        ph   = np.array([float(r.get("pH",   r.get("ph", 0))) for r in filtered])
        temp = np.array([float(r.get("temperature", 0)) for r in filtered])
        nh3  = np.array([float(r.get("nh3",  0)) for r in filtered])

        bw = 0.2

        self.plot_widget.addItem(
            pg.BarGraphItem(x=x - 1.5*bw, height=tan,  width=bw,
                            brush="#38BDF8", name="TAN (mg/L)"))
        self.plot_widget.addItem(
            pg.BarGraphItem(x=x - 0.5*bw, height=ph,   width=bw,
                            brush="#06B6D4", name="pH"))
        self.plot_widget.addItem(
            pg.BarGraphItem(x=x + 0.5*bw, height=temp, width=bw,
                            brush="#F59E0B", name="Temp (deg C)"))
        self.plot_widget.addItem(
            pg.BarGraphItem(x=x + 1.5*bw, height=nh3,  width=bw,
                            brush="#EF4444", name="NH3 (mg/L)"))

        latest = filtered[-1]
        tox    = latest.get("toxicity", "--")
        tox_color = {
            "Safe":           "#66BB6A",
            "Caution":        "#FFA726",
            "Critical Toxic": "#EF5350",
        }.get(tox, "#FFFFFF")

        tank_name = latest.get("name", latest.get("tank_name", "--"))
        tan_val   = float(latest.get("tan", 0))
        nh3_val   = float(latest.get("nh3", 0))
        ph_val    = float(latest.get("pH",  latest.get("ph", 0)))
        temp_val  = float(latest.get("temperature", 0))
        ts        = latest.get("timestamp", "--")

        self.info_box.setText(
            f"<div style='color:#FFFFFF;'>"
            f"<b>Tank:</b> {tank_name}<br>"
            f"<b>TAN:</b> <span style='color:#38BDF8;'>{tan_val:.4f} mg/L</span><br>"
            f"<b>NH3:</b> <span style='color:#EF4444;'>{nh3_val:.6f} mg/L</span><br>"
            f"<b>pH:</b> <span style='color:#06B6D4;'>{ph_val:.2f}</span>"
            f"&nbsp;&nbsp;"
            f"<b>Temp:</b> <span style='color:#F59E0B;'>{temp_val:.1f} deg C</span><br>"
            f"<b>Toxicity:</b> <span style='color:{tox_color};'>{tox}</span><br>"
            f"<small style='color:#A8DADC;'>Last update: {ts}</small>"
            f"</div>"
        )

        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setBackground("#0D1545")
        self.plot_widget.setMouseEnabled(x=False, y=False)
