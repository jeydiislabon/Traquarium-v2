# pages/graph_page.py
"""Graph visualization page"""

import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.base_page import AquaPage


class GraphPage(AquaPage):
    def __init__(self, stacked_widget):
        super().__init__("Water Parameter Graph", stacked_widget)

        # Graph area
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("#1D2429")
        self.plot_widget.setLabel("left", "Value", color="#FFFFFF")
        self.plot_widget.setLabel("bottom", "Reading Index", color="#FFFFFF")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.addLegend(offset=(10, 10))
        self.content_layout.addWidget(self.plot_widget, stretch=1)

        # Info box (centered below graph)
        self.info_box = QLabel("")
        self.info_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_box.setFont(QFont("Segoe UI", 11))
        from ui.styles import INFO_BOX_STYLE
        self.info_box.setStyleSheet(INFO_BOX_STYLE)
        self.content_layout.addWidget(self.info_box, alignment=Qt.AlignmentFlag.AlignCenter)

    def update_graph(self, readings, selected_name=None):
        """Draws a smooth line graph for one or all readings."""
        self.plot_widget.clear()
        
        if not selected_name:
            self.info_box.setText("No profile selected.")
            return

        if not readings:
            self.info_box.setText("No readings to display.")
            return

        # Filter by selected name
        if selected_name:
            readings = [r for r in readings if r["name"].lower() == selected_name.lower()]
            if not readings:
                self.info_box.setText(f"No data found for '{selected_name}'.")
                return

        # Plot data as bar graphs
        x = np.arange(len(readings))
        ph = np.array([float(r["pH"]) for r in readings])
        temp = np.array([float(r["temperature"]) for r in readings])
        ammonia = np.array([float(r["ammonia"]) for r in readings])
        
        # Bar width
        bar_width = 0.25
        
        # Create bar graphs with offset positions
        bg1 = pg.BarGraphItem(x=x - bar_width, height=ph, width=bar_width, brush="#06B6D4", name="pH Level")
        bg2 = pg.BarGraphItem(x=x, height=temp, width=bar_width, brush="#F59E0B", name="Temperature (°C)")
        bg3 = pg.BarGraphItem(x=x + bar_width, height=ammonia, width=bar_width, brush="#EF4444", name="Ammonia (ppm)")
        
        self.plot_widget.addItem(bg1)
        self.plot_widget.addItem(bg2)
        self.plot_widget.addItem(bg3)

        # Display info box for last reading
        latest = readings[-1]
        self.info_box.setText(f"""
        <div style='color:#FFFFFF;'>
        <b>Profile:</b> {latest['name']}<br>
        <b>pH:</b> <span style='color:#06B6D4;'>{latest['pH']}</span><br>
        <b>Temperature:</b> <span style='color:#F59E0B;'>{latest['temperature']} °C</span><br>
        <b>Ammonia:</b> <span style='color:#EF4444;'>{latest['ammonia']} ppm</span><br>
        <small style='color:#A8DADC;'>Timestamp: {latest['timestamp']}</small>
        </div>
        """)

        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setBackground("#1D2429")
        self.plot_widget.setMouseEnabled(x=False, y=False)
