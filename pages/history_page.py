# pages/history_page.py
"""History page with table view and warnings"""

import json
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, 
                              QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
                              QAbstractItemView, QMessageBox, QStyledItemDelegate, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QDoubleValidator
from ui.base_page import AquaPage
from ui.components import ButtonFactory, InputFieldFactory, StrictDoubleValidator
from ui.styles import TABLE_STYLE, TABLE_ALTERNATE_STYLE, TABLE_NO_SELECTION_STYLE, DROPDOWN_FRAME_STYLE
from ui.helpers import DataHelper, WarningHelper, DialogHelper


class NumericDelegate(QStyledItemDelegate):
    """Custom delegate to allow only numeric input in table cells with range validation"""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        column = index.column()
        
        # Set strict validator based on column
        if column == 2:  # pH column (0-14)
            validator = StrictDoubleValidator(0.0, 14.0, 2, editor)
        elif column == 3:  # Temperature column (0-40°C)
            validator = StrictDoubleValidator(0.0, 40.0, 2, editor)
        elif column == 4:  # Ammonia column (0-10 ppm)
            validator = StrictDoubleValidator(0.0, 10.0, 2, editor)
        else:
            validator = StrictDoubleValidator(0.0, 999.99, 2, editor)
        
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        editor.setValidator(validator)
        
        # Connect textChanged to validate in real-time
        editor.textChanged.connect(lambda text: self.validate_input(editor, column))
        
        return editor
    
    def validate_input(self, editor, column):
        """Real-time validation as user types"""
        if editor is None:
            return
        text = editor.text()
        if not text:
            return
        
        try:
            value = float(text)
            
            # Check ranges and show visual feedback
            valid = True
            if column == 2 and (value < 0 or value > 14):
                valid = False
            elif column == 3 and (value < 0 or value > 40):
                valid = False
            elif column == 4 and (value < 0 or value > 10):
                valid = False
            
            # Visual feedback
            if valid:
                editor.setStyleSheet("background-color: #2B3E50; color: white;")
            else:
                editor.setStyleSheet("background-color: #EF5350; color: white;")
        except ValueError:
            editor.setStyleSheet("background-color: #EF5350; color: white;")
    
    def setModelData(self, editor, model, index):
        """Validate data before setting it in the model"""
        if editor is None:
            return
        text = editor.text()
        column = index.column()
        
        if not text:
            QMessageBox.warning(editor, "Invalid Input", "Value cannot be empty!")
            return
        
        try:
            value = float(text)
            
            # Validate ranges
            if column == 2:  # pH
                if value < 0 or value > 14:
                    QMessageBox.warning(editor, "Invalid Range", "pH must be between 0 and 14!")
                    return
            elif column == 3:  # Temperature
                if value < 0 or value > 40:
                    QMessageBox.warning(editor, "Invalid Range", "Temperature must be between 0°C and 40°C!")
                    return
            elif column == 4:  # Ammonia
                if value < 0 or value > 10:
                    QMessageBox.warning(editor, "Invalid Range", "Ammonia must be between 0 and 10 ppm!")
                    return
            
            # If validation passes, set the data
            super().setModelData(editor, model, index)
        except ValueError:
            QMessageBox.warning(editor, "Invalid Input", "Please enter a valid number!")
            return


class HistoryPage(AquaPage):
    def __init__(self, stacked_widget, manager):
        super().__init__("History", stacked_widget)
        self.stacked_widget = stacked_widget
        self.manager = manager
        self.selected_name = None
        self.is_editing = False
        self.edited_row = -1
        
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.search_input = InputFieldFactory.create_search_input("Search by profile name...", QFont("Segoe UI", 11))
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.live_search)

        search_button = ButtonFactory.create_nav_button("Search", QFont("Segoe UI", 10, QFont.Weight.Bold))
        search_button.setFixedWidth(90)
        search_button.clicked.connect(self.live_search)
        
        self.edit_button = ButtonFactory.create_edit_button("Edit", QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.edit_button.setFixedWidth(80)
        self.edit_button.clicked.connect(self.toggle_edit_mode)
        
        delete_button = ButtonFactory.create_danger_button("Delete", QFont("Segoe UI", 10, QFont.Weight.Bold))
        delete_button.setFixedWidth(80)
        delete_button.clicked.connect(self.delete_button)

        refresh_button = ButtonFactory.create_success_button("Refresh", QFont("Segoe UI", 10, QFont.Weight.Bold))
        refresh_button.setFixedWidth(105)
        refresh_button.clicked.connect(self.refresh_table)

        # Save button (initially hidden)
        self.save_button = ButtonFactory.create_success_button("Save", QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.save_button.setFixedWidth(80)
        self.save_button.clicked.connect(self.save_edited_row)
        self.save_button.setVisible(False)
        
        top_layout.addWidget(self.search_input)
        top_layout.addWidget(search_button)
        top_layout.addWidget(self.edit_button)
        top_layout.addWidget(self.save_button)
        top_layout.addWidget(delete_button)
        top_layout.addWidget(refresh_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Name", "pH", "Temperature (°C)", "Ammonia (ppm)"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellClicked.connect(self.on_table_cell_clicked)
        self.table.verticalHeader().sectionClicked.connect(self.on_row_header_clicked)
        
        # Set minimum row height to prevent header cutoff
        self.table.verticalHeader().setDefaultSectionSize(35)
        self.table.horizontalHeader().setMinimumHeight(40)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set numeric delegate for pH, Temperature, and Ammonia columns
        self.numeric_delegate = NumericDelegate()
        self.table.setItemDelegateForColumn(2, self.numeric_delegate)  # pH
        self.table.setItemDelegateForColumn(3, self.numeric_delegate)  # Temperature
        self.table.setItemDelegateForColumn(4, self.numeric_delegate)  # Ammonia

        self.table.setStyleSheet(TABLE_STYLE)

        self.dropdown_button = QPushButton("Show Saved Readings ▼")
        self.dropdown_button.setCheckable(True)
        self.dropdown_button.clicked.connect(self.toggle_dropdown)
        self.dropdown_button.setStyleSheet("""
            QPushButton {
                background-color: #CAE9FF;
                color: #1B4965;
                padding: 6px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:checked { background-color: #A8D5F2; }
        """)

        self.dropdown_frame = QFrame()
        self.dropdown_frame.setVisible(False)
        self.dropdown_frame.setStyleSheet(DROPDOWN_FRAME_STYLE)
        self.dropdown_layout = QHBoxLayout(self.dropdown_frame)
        self.dropdown_layout.setSpacing(8)

        self.saved_table = QTableWidget()
        self.saved_table.setColumnCount(5)
        self.saved_table.setHorizontalHeaderLabels(["Timestamp", "Name", "pH", "Temp(°C)", "Ammonia"])
        self.saved_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.saved_table.setColumnWidth(0, 130)
        self.saved_table.setColumnWidth(1, 90)
        self.saved_table.setColumnWidth(2, 60)
        self.saved_table.setColumnWidth(3, 85)
        self.saved_table.setColumnWidth(4, 90)
        self.saved_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.saved_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.saved_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.saved_table.setAlternatingRowColors(True)
        self.saved_table.setMinimumWidth(480)
        self.saved_table.setFont(QFont("Segoe UI", 9))
        
        # Make table non-selectable (display only)
        self.saved_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.saved_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.saved_table.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        
        # Fix header height
        self.saved_table.verticalHeader().setDefaultSectionSize(30)
        self.saved_table.horizontalHeader().setMinimumHeight(35)

        self.warning_table = QTableWidget()
        self.warning_table.setColumnCount(2)
        self.warning_table.setHorizontalHeaderLabels(["Warning", "Suggestion"])
        self.warning_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.warning_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.warning_table.setWordWrap(True)
        self.warning_table.setAlternatingRowColors(True)
        self.warning_table.setFont(QFont("Segoe UI", 10))
        
        # Make table non-selectable (display only)
        self.warning_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.warning_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.warning_table.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        
        # Fix header height
        self.warning_table.verticalHeader().setDefaultSectionSize(40)
        self.warning_table.horizontalHeader().setMinimumHeight(35)

        # Apply no-selection style to dropdown tables
        self.saved_table.setStyleSheet(TABLE_NO_SELECTION_STYLE)
        self.warning_table.setStyleSheet(TABLE_NO_SELECTION_STYLE)

        self.dropdown_layout.addWidget(self.saved_table, 1)
        self.dropdown_layout.addWidget(self.warning_table, 2)

        # Add to content_layout (from base class) to keep nav buttons at bottom
        self.content_layout.addLayout(top_layout)
        self.content_layout.addWidget(self.table, stretch=1)
        self.content_layout.addWidget(self.dropdown_button)
        self.content_layout.addWidget(self.dropdown_frame)

        self.update_table(self.manager.get_all())

    def _field(self, reading, attr, alt_keys):
        return DataHelper.get_field(reading, attr, alt_keys)

    def update_table(self, readings):
        self.table.setRowCount(len(readings))

        for row, reading in enumerate(readings):
            ts = self._field(reading, "timestamp", ["timestamp"])
            name = self._field(reading, "name", ["name"])
            ph = self._field(reading, "pH", ["pH"])
            temp = self._field(reading, "temperature", ["temperature"])
            ammonia = self._field(reading, "ammonia", ["ammonia"])

            ph_text = DataHelper.format_float(ph, 2)
            temp_text = DataHelper.format_float(temp, 1)
            ammonia_text = DataHelper.format_float(ammonia, 2)

            items = [
                QTableWidgetItem(str(ts)),
                QTableWidgetItem(str(name)),
                QTableWidgetItem(ph_text),
                QTableWidgetItem(temp_text),
                QTableWidgetItem(ammonia_text)
            ]
            for col, it in enumerate(items):
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, it)

    def on_table_cell_clicked(self, row, column):
        """When a row is clicked, select it and update graph instantly."""
        item = self.table.item(row, 1)
        if not item:
            return

        self.selected_name = item.text().strip()
        self.table.selectRow(row)

        if self.dropdown_frame.isVisible():
            self.update_dropdown_tables()

        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "graph_page"):
            readings = self.manager.get_all()
            parent.graph_page.update_graph(readings, selected_name=self.selected_name)

    def on_row_header_clicked(self, logicalIndex):
        self.table.selectRow(logicalIndex)
        self.on_table_cell_clicked(logicalIndex, 0)

    def toggle_dropdown(self):
        visible = not self.dropdown_frame.isVisible()
        self.dropdown_frame.setVisible(visible)
        self.dropdown_button.setText("Hide Saved Readings ▲" if visible else "Show Saved Readings ▼")
        if visible:
            self.update_dropdown_tables()

    def update_dropdown_tables(self):
        if not self.selected_name:
            self.saved_table.setRowCount(0)
            self.warning_table.setRowCount(0)
            return

        all_readings = self.manager.get_all()
        matches = [r for r in all_readings
                   if str(self._field(r, "name", ["name"])).strip().lower() == self.selected_name.lower()]
        matches = matches[-2:]

        if not matches:
            self.saved_table.setRowCount(1)
            self.saved_table.setItem(0, 0, QTableWidgetItem("No saved readings"))
            self.warning_table.setRowCount(0)
            return

        self.saved_table.setRowCount(len(matches))
        all_warnings = []

        for row, r in enumerate(matches):
            ts = self._field(r, "timestamp", ["timestamp"])
            name = self._field(r, "name", ["name"])
            ph = float(self._field(r, "pH", ["pH"]) or 0)
            temp = float(self._field(r, "temperature", ["temperature"]) or 0)
            ammonia = float(self._field(r, "ammonia", ["ammonia"]) or 0)

            items = [
                QTableWidgetItem(str(ts)),
                QTableWidgetItem(str(name)),
                QTableWidgetItem(f"{ph:.2f}"),
                QTableWidgetItem(f"{temp:.1f}"),
                QTableWidgetItem(f"{ammonia:.2f}")
            ]
            for col, it in enumerate(items):
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.saved_table.setItem(row, col, it)

            all_warnings.extend(self._generate_warnings(ph, temp, ammonia))

        self.warning_table.setRowCount(len(all_warnings))
        for i, (warn, suggest, color, bg) in enumerate(all_warnings):
            w_item = QTableWidgetItem(warn)
            s_item = QTableWidgetItem(suggest)
            for col, item in enumerate((w_item, s_item)):
                item.setForeground(color)
                item.setBackground(bg)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.warning_table.setItem(i, col, item)

    def _generate_warnings(self, ph, temp, ammonia):
        return WarningHelper.generate_warnings(ph, temp, ammonia)

    def live_search(self):
        search_name = self.search_input.text().strip().lower()
        all_readings = self.manager.get_all()
        if not search_name:
            self.update_table(all_readings)
            return
        filtered = [r for r in all_readings if str(self._field(r, "name", ["name"])).strip().lower().startswith(search_name)]
        self.update_table(filtered)

    def refresh_table(self):
        # Cancel edit mode if active
        if self.is_editing:
            self.cancel_edit_mode()
        
        self.search_input.clear()
        self.selected_name = None
        self.dropdown_frame.setVisible(False)
        self.dropdown_button.setChecked(False)
        self.manager.load_readings()  # Reload from file
        self.update_table(self.manager.get_all())
        
        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "graph_page"):
            parent.graph_page.update_graph([], selected_name=None)
        
    def toggle_edit_mode(self):
        """Toggle edit mode for the selected row"""
        if self.is_editing:
            self.cancel_edit_mode()
        else:
            self.start_edit_mode()
    
    def start_edit_mode(self):
        """Enable editing for selected row"""
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a row to edit.")
            return
        
        self.is_editing = True
        self.edited_row = row
        
        # Change button appearance
        self.edit_button.setText("❌ Cancel")
        from ui.styles import DANGER_BUTTON_STYLE
        self.edit_button.setStyleSheet(DANGER_BUTTON_STYLE)
        
        # Show save button
        self.save_button.setVisible(True)
        
        # Enable editing on the table
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.SelectedClicked)
        
        # Make timestamp column non-editable, others editable
        for col in range(5):
            item = self.table.item(row, col)
            if item:
                if col == 0:  # Timestamp - not editable
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                else:  # Name, pH, Temperature, Ammonia - editable
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        
        # Highlight the row
        for col in range(5):
            item = self.table.item(row, col)
            if item:
                item.setBackground(QColor("#4A5F7F"))
        
        QMessageBox.information(self, "Edit Mode", 
            "Edit mode enabled!\n\n"
            "• Double-click on Name, pH, Temperature, or Ammonia to edit\n"
            "• Only numbers allowed for pH, Temperature, Ammonia\n"
            "• Click 'Save' when done or 'Cancel' to discard changes")
    
    def cancel_edit_mode(self):
        """Cancel edit mode and reload original data"""
        if self.edited_row >= 0:
            # Remove highlight
            for col in range(5):
                item = self.table.item(self.edited_row, col)
                if item:
                    item.setBackground(QColor(0, 0, 0, 0))  # Transparent
        
        self.is_editing = False
        self.edited_row = -1
        
        # Disable editing on the table
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Reset button
        self.edit_button.setText("Edit")
        from ui.styles import EDIT_BUTTON_STYLE
        self.edit_button.setStyleSheet(EDIT_BUTTON_STYLE)
        
        # Hide save button
        self.save_button.setVisible(False)
        
        # Reload original data
        self.update_table(self.manager.get_all())
    
    def save_edited_row(self):
        """Validate and save the edited row"""
        if not self.is_editing or self.edited_row < 0:
            return
        
        row = self.edited_row
        
        try:
            # Get values
            name = self.table.item(row, 1).text().strip()
            ph_text = self.table.item(row, 2).text().strip()
            temp_text = self.table.item(row, 3).text().strip()
            ammonia_text = self.table.item(row, 4).text().strip()
            
            # Validate name
            if not name:
                QMessageBox.warning(self, "Invalid Input", "Name cannot be empty!")
                return
            
            # Validate and convert numbers
            try:
                ph = float(ph_text)
                temp = float(temp_text)
                ammonia = float(ammonia_text)
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", 
                    "pH, Temperature, and Ammonia must be valid numbers!")
                return
            
            # Validate ranges (same as input page and water parameter guide)
            if ph < 0 or ph > 14:
                QMessageBox.warning(self, "Invalid Range", 
                    "pH must be between 0 and 14!\n\nRefer to Water Parameter Guide:\npH Level (6.5 - 8.0) is ideal for most aquariums.")
                return
            
            if temp < 0 or temp > 40:
                QMessageBox.warning(self, "Invalid Range", 
                    "Temperature must be between 0°C and 40°C!\n\nRefer to Water Parameter Guide:\nTemperature (20-28°C / 68-82°F) is ideal for most fish.")
                return
            
            if ammonia < 0 or ammonia > 10:
                QMessageBox.warning(self, "Invalid Range", 
                    "Ammonia must be between 0 and 10 ppm!\n\nRefer to Water Parameter Guide:\nAmmonia (0-0.5 ppm) is the safe range.")
                return
            
            # Save to file
            data = []
            for r in range(self.table.rowCount()):
                data.append({
                    "timestamp": self.table.item(r, 0).text(),
                    "name": self.table.item(r, 1).text(),
                    "pH": float(self.table.item(r, 2).text()),
                    "temperature": float(self.table.item(r, 3).text()),
                    "ammonia": float(self.table.item(r, 4).text())
                })
            
            with open(self.manager.file_path, "w") as f:
                json.dump(data, f, indent=4)
            
            self.manager.load_readings()
            
            # Update all pages
            parent = self.parentWidget().parentWidget()
            if hasattr(parent, "home_page"):
                parent.home_page.update_latest(self.manager.get_all())
            if hasattr(parent, "graph_page"):
                parent.graph_page.update_graph(self.manager.get_all())
            
            QMessageBox.information(self, "Success", "Changes saved successfully!")
            
            # Exit edit mode
            self.cancel_edit_mode()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")

    def delete_button(self):
        """Delete the selected row and update JSON."""
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return

        confirm = QMessageBox.question(
            self, "Delete Confirmation",
            "Are you sure you want to delete this reading?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        timestamp_to_delete = self.table.item(row, 0).text()

        readings = self.manager.get_all()
        updated = [r for r in readings if r["timestamp"] != timestamp_to_delete]

        with open(self.manager.file_path, "w") as f:
            json.dump(updated, f, indent=4)

        self.manager.load_readings()
        self.update_table(self.manager.get_all())

        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "home_page"):
            parent.home_page.update_latest(self.manager.get_all())
        if hasattr(parent, "graph_page"):
            parent.graph_page.update_graph(self.manager.get_all())

        QMessageBox.information(self, "Deleted", "Reading deleted successfully!")
