# pages/history_page.py
"""History page — displays all readings with NH3/toxicity columns,
   edit/delete backed by SQLite via ReadingManager."""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QAbstractItemView, QMessageBox, QStyledItemDelegate, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QDoubleValidator
from ui.base_page import AquaPage
from ui.components import ButtonFactory, InputFieldFactory, StrictDoubleValidator
from ui.styles import TABLE_STYLE, TABLE_NO_SELECTION_STYLE, DROPDOWN_FRAME_STYLE
from ui.helpers import DataHelper, WarningHelper, DialogHelper
from ammonia_engine import AmmoniaEngine, PH_MIN, PH_MAX, TEMP_MIN, TEMP_MAX, TAN_MIN, TAN_MAX


# ---------------------------------------------------------------------------
# Numeric delegate
# ---------------------------------------------------------------------------

class NumericDelegate(QStyledItemDelegate):
    """Restrict in-cell editing to valid numeric ranges."""

    _RANGES = {
        2: (TAN_MIN,  TAN_MAX,  "TAN"),
        3: (PH_MIN,   PH_MAX,   "pH"),
        4: (TEMP_MIN, TEMP_MAX, "Temperature"),
    }

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        col = index.column()
        if col in self._RANGES:
            lo, hi, _ = self._RANGES[col]
            v = StrictDoubleValidator(lo, hi, 4, editor)
            v.setNotation(QDoubleValidator.Notation.StandardNotation)
            editor.setValidator(v)
        editor.textChanged.connect(lambda t: self._highlight(editor, col))
        return editor

    def _highlight(self, editor, col):
        text = editor.text()
        ok = True
        if text and col in self._RANGES:
            try:
                val = float(text)
                lo, hi, _ = self._RANGES[col]
                ok = lo <= val <= hi
            except ValueError:
                ok = False
        color = "#2B3E50" if ok else "#EF5350"
        editor.setStyleSheet(f"background:{color}; color:white;")

    def setModelData(self, editor, model, index):
        text = editor.text()
        col  = index.column()
        if not text:
            QMessageBox.warning(editor, "Invalid", "Value cannot be empty.")
            return
        if col in self._RANGES:
            try:
                val = float(text)
                lo, hi, name = self._RANGES[col]
                if not (lo <= val <= hi):
                    QMessageBox.warning(
                        editor, "Out of range",
                        f"{name} must be between {lo} and {hi}."
                    )
                    return
            except ValueError:
                QMessageBox.warning(editor, "Invalid", "Enter a valid number.")
                return
        super().setModelData(editor, model, index)


# ---------------------------------------------------------------------------
# History page
# ---------------------------------------------------------------------------

# Column indices
COL_TS   = 0
COL_NAME = 1
COL_TAN  = 2
COL_PH   = 3
COL_TEMP = 4
COL_NH3  = 5
COL_TOX  = 6

HEADERS = ["Timestamp", "Tank Name", "TAN (mg/L)", "pH",
           "Temp (°C)", "NH₃ (mg/L)", "Toxicity"]

# Toxicity row colours (background)
TOX_COLORS = {
    "Safe":          QColor("#1B5E20"),
    "Caution":       QColor("#4E3A00"),
    "Critical Toxic":QColor("#5C0A0A"),
}


class HistoryPage(AquaPage):
    def __init__(self, stacked_widget, manager):
        super().__init__("History", stacked_widget)
        self.stacked_widget = stacked_widget
        self.manager        = manager
        self.selected_name  = None
        self.is_editing     = False
        self.edited_row     = -1

        # ----------------------------------------------------------------
        # Top bar
        # ----------------------------------------------------------------
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.search_input = InputFieldFactory.create_search_input(
            "Search by tank name…", QFont("Segoe UI", 11))
        self.search_input.setFixedWidth(260)
        self.search_input.textChanged.connect(self.live_search)

        search_btn  = ButtonFactory.create_nav_button("Search",  QFont("Segoe UI", 10, QFont.Weight.Bold))
        search_btn.setFixedWidth(90);  search_btn.clicked.connect(self.live_search)

        self.edit_button = ButtonFactory.create_edit_button("Edit", QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.edit_button.setFixedWidth(80); self.edit_button.clicked.connect(self.toggle_edit_mode)

        self.save_button = ButtonFactory.create_success_button("Save", QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.save_button.setFixedWidth(80); self.save_button.clicked.connect(self.save_edited_row)
        self.save_button.setVisible(False)

        delete_btn  = ButtonFactory.create_danger_button("Delete",  QFont("Segoe UI", 10, QFont.Weight.Bold))
        delete_btn.setFixedWidth(80);  delete_btn.clicked.connect(self.delete_selected)

        refresh_btn = ButtonFactory.create_success_button("Refresh", QFont("Segoe UI", 10, QFont.Weight.Bold))
        refresh_btn.setFixedWidth(105); refresh_btn.clicked.connect(self.refresh_table)

        for w in (self.search_input, search_btn, self.edit_button,
                  self.save_button, delete_btn, refresh_btn):
            top_layout.addWidget(w)

        # ----------------------------------------------------------------
        # Main table (7 columns)
        # ----------------------------------------------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellClicked.connect(self.on_table_cell_clicked)
        self.table.verticalHeader().sectionClicked.connect(self.on_row_header_clicked)
        self.table.verticalHeader().setDefaultSectionSize(35)
        self.table.horizontalHeader().setMinimumHeight(40)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setStyleSheet(TABLE_STYLE)

        # Numeric delegates on editable columns
        delegate = NumericDelegate()
        for col in (COL_TAN, COL_PH, COL_TEMP):
            self.table.setItemDelegateForColumn(col, delegate)

        # ----------------------------------------------------------------
        # Dropdown — detail panel
        # ----------------------------------------------------------------
        self.dropdown_button = QPushButton("Show Details ▼")
        self.dropdown_button.setCheckable(True)
        self.dropdown_button.clicked.connect(self.toggle_dropdown)
        self.dropdown_button.setStyleSheet("""
            QPushButton {
                background-color: #CAE9FF; color: #1B4965;
                padding: 6px; border-radius: 4px;
                font-size: 11px; font-weight: bold;
            }
            QPushButton:checked { background-color: #A8D5F2; }
        """)

        self.dropdown_frame = QFrame()
        self.dropdown_frame.setVisible(False)
        self.dropdown_frame.setStyleSheet(DROPDOWN_FRAME_STYLE)
        dropdown_layout = QHBoxLayout(self.dropdown_frame)
        dropdown_layout.setSpacing(8)

        # Dosing instructions table
        self.dosing_table = QTableWidget()
        self.dosing_table.setColumnCount(1)
        self.dosing_table.setHorizontalHeaderLabels(["Dosing / Maintenance Instructions"])
        self.dosing_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.dosing_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.dosing_table.setWordWrap(True)
        self.dosing_table.setAlternatingRowColors(True)
        self.dosing_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.dosing_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.dosing_table.setFont(QFont("Segoe UI", 10))
        self.dosing_table.verticalHeader().setDefaultSectionSize(36)
        self.dosing_table.horizontalHeader().setMinimumHeight(35)
        self.dosing_table.setStyleSheet(TABLE_NO_SELECTION_STYLE)

        # Warning table
        self.warning_table = QTableWidget()
        self.warning_table.setColumnCount(2)
        self.warning_table.setHorizontalHeaderLabels(["Warning", "Suggestion"])
        self.warning_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.warning_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.warning_table.setWordWrap(True)
        self.warning_table.setAlternatingRowColors(True)
        self.warning_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.warning_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.warning_table.setFont(QFont("Segoe UI", 10))
        self.warning_table.verticalHeader().setDefaultSectionSize(40)
        self.warning_table.horizontalHeader().setMinimumHeight(35)
        self.warning_table.setStyleSheet(TABLE_NO_SELECTION_STYLE)

        dropdown_layout.addWidget(self.dosing_table,  1)
        dropdown_layout.addWidget(self.warning_table, 1)

        # ----------------------------------------------------------------
        # Layout assembly
        # ----------------------------------------------------------------
        self.content_layout.addLayout(top_layout)
        self.content_layout.addWidget(self.table, stretch=1)
        self.content_layout.addWidget(self.dropdown_button)
        self.content_layout.addWidget(self.dropdown_frame)

        self.update_table(self.manager.get_all())

    # ----------------------------------------------------------------
    # Table population
    # ----------------------------------------------------------------

    def _g(self, reading, *keys):
        """Get a field from a reading dict by trying multiple keys."""
        return DataHelper.get_field(reading, keys[0], list(keys))

    def _tox_color(self, toxicity: str) -> QColor:
        return TOX_COLORS.get(toxicity, QColor(0, 0, 0, 0))

    def update_table(self, readings):
        self.table.setRowCount(len(readings))
        for row, r in enumerate(readings):
            ts       = self._g(r, "timestamp")
            name     = self._g(r, "name", "tank_name")
            tan      = self._g(r, "tan")
            ph       = self._g(r, "pH", "ph")
            temp     = self._g(r, "temperature")
            nh3      = self._g(r, "nh3")
            toxicity = self._g(r, "toxicity")

            bg = self._tox_color(str(toxicity))

            vals = [
                str(ts),
                str(name),
                DataHelper.format_float(tan,  4),
                DataHelper.format_float(ph,   2),
                DataHelper.format_float(temp, 1),
                DataHelper.format_float(nh3,  6),
                str(toxicity),
            ]
            for col, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(bg)
                self.table.setItem(row, col, item)

    # ----------------------------------------------------------------
    # Selection / dropdown
    # ----------------------------------------------------------------

    def on_table_cell_clicked(self, row, column):
        item = self.table.item(row, COL_NAME)
        if not item:
            return
        self.selected_name = item.text().strip()
        self.table.selectRow(row)
        if self.dropdown_frame.isVisible():
            self.update_dropdown_tables(row)
        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "graph_page"):
            parent.graph_page.update_graph(
                self.manager.get_all(), selected_name=self.selected_name)

    def on_row_header_clicked(self, idx):
        self.table.selectRow(idx)
        self.on_table_cell_clicked(idx, 0)

    def toggle_dropdown(self):
        visible = not self.dropdown_frame.isVisible()
        self.dropdown_frame.setVisible(visible)
        self.dropdown_button.setText(
            "Hide Details ▲" if visible else "Show Details ▼")
        if visible:
            row = self.table.currentRow()
            self.update_dropdown_tables(row)

    def update_dropdown_tables(self, row: int):
        # Dosing instructions from the selected row
        if row < 0 or not self.selected_name:
            self.dosing_table.setRowCount(0)
            self.warning_table.setRowCount(0)
            return

        all_readings = self.manager.get_all()
        matches = [r for r in all_readings
                   if str(self._g(r, "name", "tank_name")).lower()
                   == self.selected_name.lower()]
        if not matches:
            self.dosing_table.setRowCount(0)
            return

        latest = matches[-1]
        tan  = float(self._g(latest, "tan")  or 0)
        ph   = float(self._g(latest, "pH", "ph") or 0)
        temp = float(self._g(latest, "temperature") or 0)
        nh3  = float(self._g(latest, "nh3")  or 0)
        tox  = str(self._g(latest, "toxicity"))

        # Re-generate instructions from AmmoniaEngine
        try:
            instructions = AmmoniaEngine.generate_dosing_instructions(
                nh3, tox, tan, ph, temp)
        except Exception:
            instructions = ["Could not generate instructions."]

        self.dosing_table.setRowCount(len(instructions))
        for i, line in enumerate(instructions):
            item = QTableWidgetItem(line)
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.dosing_table.setItem(i, 0, item)
        self.dosing_table.resizeRowsToContents()

        # Warnings based on NH3 / pH / temp
        warnings = WarningHelper.generate_warnings(ph, temp, nh3)
        self.warning_table.setRowCount(len(warnings))
        for i, (warn, suggest, color, bg) in enumerate(warnings):
            for col, text in enumerate((warn, suggest)):
                it = QTableWidgetItem(text)
                it.setForeground(color)
                it.setBackground(bg)
                it.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.warning_table.setItem(i, col, it)

    # ----------------------------------------------------------------
    # Search / refresh
    # ----------------------------------------------------------------

    def live_search(self):
        q = self.search_input.text().strip().lower()
        all_r = self.manager.get_all()
        if not q:
            self.update_table(all_r)
            return
        filtered = [r for r in all_r
                    if str(self._g(r, "name", "tank_name")).lower().startswith(q)]
        self.update_table(filtered)

    def refresh_table(self):
        if self.is_editing:
            self.cancel_edit_mode()
        self.search_input.clear()
        self.selected_name = None
        self.dropdown_frame.setVisible(False)
        self.dropdown_button.setChecked(False)
        self.manager.load_readings()
        self.update_table(self.manager.get_all())
        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "graph_page"):
            parent.graph_page.update_graph([], selected_name=None)

    # ----------------------------------------------------------------
    # Edit mode
    # ----------------------------------------------------------------

    def toggle_edit_mode(self):
        if self.is_editing:
            self.cancel_edit_mode()
        else:
            self.start_edit_mode()

    def start_edit_mode(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "No selection", "Select a row to edit.")
            return
        self.is_editing = True
        self.edited_row = row
        self.edit_button.setText("❌ Cancel")
        from ui.styles import DANGER_BUTTON_STYLE
        self.edit_button.setStyleSheet(DANGER_BUTTON_STYLE)
        self.save_button.setVisible(True)
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked |
            QTableWidget.EditTrigger.SelectedClicked)
        for col in range(len(HEADERS)):
            item = self.table.item(row, col)
            if item:
                # Allow editing only TAN, pH, Temp, Name (not TS, NH3, Toxicity)
                if col in (COL_NAME, COL_TAN, COL_PH, COL_TEMP):
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setBackground(QColor("#4A5F7F"))
        QMessageBox.information(
            self, "Edit Mode",
            "Double-click Tank Name, TAN, pH, or Temperature to edit.\n"
            "NH₃ and Toxicity are recalculated automatically on Save.")

    def cancel_edit_mode(self):
        if self.edited_row >= 0:
            for col in range(len(HEADERS)):
                item = self.table.item(self.edited_row, col)
                if item:
                    item.setBackground(QColor(0, 0, 0, 0))
        self.is_editing  = False
        self.edited_row  = -1
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.edit_button.setText("Edit")
        from ui.styles import EDIT_BUTTON_STYLE
        self.edit_button.setStyleSheet(EDIT_BUTTON_STYLE)
        self.save_button.setVisible(False)
        self.update_table(self.manager.get_all())

    def save_edited_row(self):
        if not self.is_editing or self.edited_row < 0:
            return
        row = self.edited_row
        try:
            name = self.table.item(row, COL_NAME).text().strip()
            tan  = float(self.table.item(row, COL_TAN).text())
            ph   = float(self.table.item(row, COL_PH).text())
            temp = float(self.table.item(row, COL_TEMP).text())
        except (AttributeError, ValueError):
            QMessageBox.warning(self, "Invalid", "Check your values and try again.")
            return

        if not name:
            QMessageBox.warning(self, "Invalid", "Tank name cannot be empty."); return
        if not (TAN_MIN <= tan <= TAN_MAX):
            QMessageBox.warning(self, "Out of range", f"TAN must be {TAN_MIN}–{TAN_MAX}."); return
        if not (PH_MIN <= ph <= PH_MAX):
            QMessageBox.warning(self, "Out of range", f"pH must be {PH_MIN}–{PH_MAX}."); return
        if not (TEMP_MIN <= temp <= TEMP_MAX):
            QMessageBox.warning(self, "Out of range", f"Temperature must be {TEMP_MIN}–{TEMP_MAX}."); return

        try:
            result = AmmoniaEngine.calculate(tan, ph, temp)
        except ValueError as e:
            QMessageBox.critical(self, "Calculation error", str(e)); return

        # Get the reading ID from hidden data (stored in column 0 item's data role)
        id_item = self.table.item(row, COL_TS)
        reading_id = id_item.data(Qt.ItemDataRole.UserRole) if id_item else None

        if reading_id is None:
            # Fall back: match by timestamp
            ts = self.table.item(row, COL_TS).text()
            all_r = self.manager.get_all()
            match = next((r for r in all_r if r.get("timestamp") == ts), None)
            reading_id = match.get("id") if match else None

        if reading_id is None:
            QMessageBox.critical(self, "Error", "Cannot identify reading to update."); return

        self.manager.update_reading(
            reading_id, name, tan, ph, temp,
            round(result.nh3, 6), result.toxicity)

        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "home_page"):
            parent.home_page.update_latest(self.manager.get_all())
        if hasattr(parent, "graph_page"):
            parent.graph_page.update_graph(self.manager.get_all())

        QMessageBox.information(self, "Saved", "Reading updated and NH₃ recalculated.")
        self.cancel_edit_mode()

    # ----------------------------------------------------------------
    # Delete
    # ----------------------------------------------------------------

    def delete_selected(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "No selection", "Select a row to delete."); return

        confirm = QMessageBox.question(
            self, "Delete",
            "Delete this reading from the database?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm != QMessageBox.StandardButton.Yes:
            return

        id_item    = self.table.item(row, COL_TS)
        reading_id = id_item.data(Qt.ItemDataRole.UserRole) if id_item else None

        if reading_id is None:
            ts    = self.table.item(row, COL_TS).text()
            all_r = self.manager.get_all()
            match = next((r for r in all_r if r.get("timestamp") == ts), None)
            reading_id = match.get("id") if match else None

        if reading_id is None:
            QMessageBox.critical(self, "Error", "Cannot identify reading to delete."); return

        self.manager.delete_reading(reading_id)
        self.update_table(self.manager.get_all())

        parent = self.parentWidget().parentWidget()
        if hasattr(parent, "home_page"):
            parent.home_page.update_latest(self.manager.get_all())
        if hasattr(parent, "graph_page"):
            parent.graph_page.update_graph(self.manager.get_all())

        QMessageBox.information(self, "Deleted", "Reading deleted.")

    # Expose reading IDs in the table so edit/delete can find them
    def update_table(self, readings):
        self.table.setRowCount(len(readings))
        for row, r in enumerate(readings):
            ts       = self._g(r, "timestamp")
            name     = self._g(r, "name", "tank_name")
            tan      = self._g(r, "tan")
            ph       = self._g(r, "pH", "ph")
            temp     = self._g(r, "temperature")
            nh3      = self._g(r, "nh3")
            toxicity = self._g(r, "toxicity")
            rid      = r.get("id")

            bg = self._tox_color(str(toxicity))

            vals = [
                str(ts),
                str(name),
                DataHelper.format_float(tan,  4),
                DataHelper.format_float(ph,   2),
                DataHelper.format_float(temp, 1),
                DataHelper.format_float(nh3,  6),
                str(toxicity),
            ]
            for col, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(bg)
                # Store DB id in column 0 for edit/delete lookup
                if col == COL_TS:
                    item.setData(Qt.ItemDataRole.UserRole, rid)
                self.table.setItem(row, col, item)
