"""
ui/styles.py
------------
All Qt stylesheets for Traquarium v2.
Color palette (aquarium-inspired):
  Navy Blue      #1A2472   deep background
  Royal Blue     #2255A4   panels / cards
  Lavender       #673888   accent / borders
  Plum           #C06090   hover / secondary
  Cranberry      #B01040   primary CTA / danger
  Dusty Rose     #8B1A3A   pressed / deep accent
"""

# ---------------------------------------------------------------------------
# Input fields
# ---------------------------------------------------------------------------
INPUT_FIELD_STYLE = """
    QLineEdit {
        background: #0D1545;
        border: 2px solid #3A4A9A;
        border-radius: 10px;
        padding: 13px 18px;
        color: #FFFFFF;
        font-size: 14px;
        selection-background-color: #673888;
    }
    QLineEdit:focus {
        border: 2px solid #673888;
        background: #1A2472;
    }
    QLineEdit::placeholder { color: #6B7BB0; }
"""

INPUT_FIELD_SMALL_STYLE = """
    QLineEdit {
        background: #0D1545;
        border: 1.5px solid #3A4A9A;
        border-radius: 8px;
        padding: 9px 12px;
        color: #FFFFFF;
        font-size: 13px;
        selection-background-color: #673888;
    }
    QLineEdit:focus {
        border: 2px solid #673888;
        background: #1A2472;
    }
    QLineEdit::placeholder { color: #6B7BB0; }
"""

SEARCH_INPUT_STYLE = """
    QLineEdit {
        background: #0D1545;
        border: 1.5px solid #3A4A9A;
        border-radius: 8px;
        padding: 7px 12px;
        color: #FFFFFF;
        font-size: 12px;
    }
    QLineEdit:focus {
        border: 2px solid #673888;
    }
    QLineEdit::placeholder { color: #6B7BB0; }
"""

# ---------------------------------------------------------------------------
# Buttons
# ---------------------------------------------------------------------------
PRIMARY_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #B01040, stop:1 #8B1A3A);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #C01550, stop:1 #9B2040);
    }
    QPushButton:pressed { background: #6B0020; }
    QPushButton:focus   { outline: none; }
"""

SECONDARY_BUTTON_STYLE = """
    QPushButton {
        background: rgba(103, 56, 136, 0.25);
        color: #FFFFFF;
        border: 1.5px solid #673888;
        border-radius: 8px;
        padding: 6px 16px;
    }
    QPushButton:hover {
        background: rgba(192, 96, 144, 0.3);
        border-color: #C06090;
    }
    QPushButton:focus { outline: none; }
"""

SUCCESS_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #673888, stop:1 #8B1A3A);
        color: #FFFFFF;
        padding: 11px 28px;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        border-bottom: 3px solid rgba(0,0,0,0.25);
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #7A44A0, stop:1 #9B2040);
        border-bottom: 4px solid rgba(0,0,0,0.3);
    }
    QPushButton:pressed {
        background: #4A1A60;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    QPushButton:focus { outline: none; }
"""

DANGER_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #B01040, stop:1 #8B1A3A);
        color: #FFFFFF;
        padding: 8px 14px;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        border-bottom: 3px solid rgba(0,0,0,0.25);
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #C01550, stop:1 #9B2040);
        border-bottom: 4px solid rgba(0,0,0,0.3);
    }
    QPushButton:pressed { background: #6B0020; }
"""

NAV_BUTTON_STYLE = """
    QPushButton {
        background: rgba(34, 85, 164, 0.45);
        color: #B8C4E8;
        border: 1px solid #3A4A9A;
        padding: 9px 20px;
        border-radius: 8px;
        font-weight: 500;
    }
    QPushButton:hover {
        background: rgba(103, 56, 136, 0.5);
        color: #FFFFFF;
        border-color: #673888;
    }
    QPushButton:pressed { background: rgba(139, 26, 58, 0.5); }
    QPushButton:focus   { outline: none; }
"""

ICON_BUTTON_STYLE = """
    QPushButton {
        background: rgba(34, 85, 164, 0.4);
        color: #B8C4E8;
        border-radius: 8px;
        border: 1px solid #3A4A9A;
        padding: 4px 10px;
        font-size: 11px;
    }
    QPushButton:hover {
        background: rgba(103, 56, 136, 0.5);
        color: #FFFFFF;
        border-color: #673888;
    }
    QPushButton:focus { outline: none; }
"""

ICON_BUTTON_SECONDARY_STYLE = """
    QPushButton {
        background: rgba(192, 96, 144, 0.15);
        color: #B8C4E8;
        border-radius: 8px;
        border: 1px solid #673888;
        padding: 4px 10px;
        font-size: 11px;
    }
    QPushButton:hover {
        background: rgba(192, 96, 144, 0.3);
        color: #FFFFFF;
        border-color: #C06090;
    }
    QPushButton:focus { outline: none; }
"""

EDIT_BUTTON_STYLE = """
    QPushButton {
        background: rgba(103, 56, 136, 0.2);
        color: #B8C4E8;
        padding: 8px 14px;
        border-radius: 8px;
        font-weight: bold;
        border: 1.5px solid #673888;
    }
    QPushButton:hover {
        background: rgba(103, 56, 136, 0.4);
        color: #FFFFFF;
        border-color: #C06090;
    }
    QPushButton:pressed { background: rgba(139, 26, 58, 0.4); }
"""

# ---------------------------------------------------------------------------
# Cards / Frames
# ---------------------------------------------------------------------------
CARD_FRAME_STYLE = """
    QFrame {
        background: rgba(26, 36, 114, 0.6);
        border: 1.5px solid #3A4A9A;
        border-radius: 14px;
    }
    QFrame:focus { outline: none; }
"""

GRAPH_CARD_STYLE = """
    QFrame {
        background: rgba(26, 36, 114, 0.5);
        border-radius: 16px;
        border: 1.5px solid #3A4A9A;
    }
"""

SIDEBAR_STYLE = """
    QFrame {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #1A2472, stop:1 #0D1545);
        border: none;
        border-right: 1px solid #3A4A9A;
    }
"""

GUIDE_SECTION_STYLE = """
    QFrame {
        background: rgba(34, 85, 164, 0.3);
        border: 1.5px solid #3A4A9A;
        border-radius: 10px;
        padding: 10px;
    }
    QFrame:focus { outline: none; }
"""

DROPDOWN_FRAME_STYLE = """
    background: rgba(13, 21, 69, 0.8);
    border: 1.5px solid #3A4A9A;
    border-radius: 8px;
    padding: 6px;
"""

# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------
TABLE_STYLE = """
    QTableWidget {
        background: rgba(13, 21, 69, 0.6);
        color: #FFFFFF;
        border: 1.5px solid #3A4A9A;
        border-radius: 10px;
        gridline-color: #2A3A7A;
        selection-background-color: rgba(103, 56, 136, 0.4);
        alternate-background-color: rgba(34, 85, 164, 0.15);
    }
    QHeaderView::section {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2255A4, stop:1 #1A2472);
        color: #FFFFFF;
        padding: 8px;
        font-weight: bold;
        border: none;
        border-right: 1px solid #3A4A9A;
    }
    QTableWidget::item { padding: 4px; }
    QTableWidget::item:selected {
        background: rgba(103, 56, 136, 0.45);
        color: #FFFFFF;
    }
"""

TABLE_ALTERNATE_STYLE = TABLE_STYLE

TABLE_NO_SELECTION_STYLE = """
    QTableWidget {
        background: rgba(13, 21, 69, 0.6);
        alternate-background-color: rgba(34, 85, 164, 0.12);
        color: #FFFFFF;
        gridline-color: #2A3A7A;
        selection-background-color: transparent;
        selection-color: #FFFFFF;
        border: 1.5px solid #3A4A9A;
        border-radius: 8px;
    }
    QHeaderView::section {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2255A4, stop:1 #1A2472);
        color: #FFFFFF;
        font-weight: bold;
        padding: 6px;
        border: none;
    }
    QTableWidget::item { padding: 3px; }
    QTableWidget::item:selected { background: transparent; color: #FFFFFF; }
    QTableWidget::item:focus    { background: transparent; outline: none; }
    QTableWidget::item:hover    { background: transparent; }
"""

# ---------------------------------------------------------------------------
# Scrollbar
# ---------------------------------------------------------------------------
SCROLLBAR_STYLE = """
    QScrollArea { background: transparent; border: none; }
    QScrollBar:vertical {
        background: rgba(26, 36, 114, 0.4);
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #673888;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover { background: #C06090; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
"""

# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
PROGRESS_BAR_STYLE = """
    QProgressBar {
        background: rgba(26, 36, 114, 0.5);
        border-radius: 4px;
        border: none;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #B01040, stop:1 #673888);
        border-radius: 4px;
    }
"""

MENU_BAR_STYLE = """
    QMenuBar {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #1A2472, stop:0.5 #2255A4, stop:1 #1A2472);
        color: #FFFFFF;
        padding: 2px;
        border-bottom: 1px solid #3A4A9A;
    }
    QMenuBar::item { background: transparent; color: #B8C4E8; padding: 4px 14px; }
    QMenuBar::item:selected { background: rgba(103,56,136,0.4); color: #FFFFFF; }
    QMenu {
        background: #1A2472;
        color: #FFFFFF;
        border: 1px solid #3A4A9A;
    }
    QMenu::item { padding: 6px 30px 6px 20px; }
    QMenu::item:selected { background: #673888; }
"""

MESSAGE_BOX_STYLE = """
    QMessageBox { background: #1A2472; }
    QLabel { color: #FFFFFF; font-size: 11pt; }
    QPushButton {
        background: #673888;
        color: white;
        padding: 8px 20px;
        border-radius: 8px;
        min-width: 80px;
        border: none;
    }
    QPushButton:hover { background: #7A44A0; }
"""

INFO_BOX_STYLE = """
    QLabel {
        background: rgba(13, 21, 69, 0.7);
        color: #FFFFFF;
        border-radius: 10px;
        border: 1.5px solid #3A4A9A;
        padding: 12px;
        margin: 8px;
    }
"""
