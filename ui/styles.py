"""UI styles"""

INPUT_FIELD_STYLE = """
    QLineEdit {
        border: none;
        border-radius: 15px;
        padding: 15px 20px;
        background: #242C30;
        color: #E8E8E8;
        font-size: 14px;
        line-height: 1.5;
    }
    QLineEdit:focus {
        background: #1D2429;
        border: 2px solid #293438;
        padding: 13px 18px;
    }
    QLineEdit::placeholder {
        color: #6B7280;
    }
"""

INPUT_FIELD_SMALL_STYLE = """
    QLineEdit {
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid #293438;
        border-radius: 8px;
        padding: 10px;
        color: #FFFFFF;
        font-size: 13px;
        outline: none;
    }
    QLineEdit:focus {
        border: 2px solid #4A5F7F;
        background: rgba(255, 255, 255, 0.12);
        outline: none;
    }
"""

SEARCH_INPUT_STYLE = """
    QLineEdit {
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid #293438;
        padding: 8px;
        border-radius: 6px;
        color: #FFFFFF;
        font-size: 12px;
    }
    QLineEdit:focus {
        border: 3px solid #293438;
        background: rgba(255, 255, 255, 0.12);
    }
"""

PRIMARY_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #293438,
            stop:0.5 #1D2429,
            stop:1 #0F1314);
        color: #FFFFFF;
        border-radius: 15px;
        border: 1px solid #242C30;
        letter-spacing: 2px;
        outline: none;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #242C30,
            stop:1 #1D2429);
        border: 1px solid #293438;
    }
    QPushButton:pressed {
        background: #0F1314;
    }
    QPushButton:focus {
        outline: none;
    }
"""

SECONDARY_BUTTON_STYLE = """
    QPushButton {
        background: rgba(255, 255, 255, 0.15);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 6px;
        padding: 5px 15px;
        text-align: center;
        outline: none;
    }
    QPushButton:hover {
        color: #FFFFFF;
        background: rgba(255, 255, 255, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    QPushButton:focus {
        outline: none;
    }
"""

SUCCESS_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #10B981,
            stop:1 #059669);
        color: #FFFFFF;
        padding: 12px 30px;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        border-bottom: 3px solid rgba(0, 0, 0, 0.2);
        outline: none;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #059669,
            stop:1 #047857);
        border-bottom: 5px solid rgba(0, 0, 0, 0.3);
        margin-top: -2px;
        padding-bottom: 14px;
    }
    QPushButton:pressed {
        margin-top: 2px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
    QPushButton:focus {
        outline: none;
    }
"""

DANGER_BUTTON_STYLE = """
    QPushButton { 
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #EF4444, stop:1 #DC2626);
        color: white; 
        padding: 8px 14px; 
        border-radius: 6px; 
        font-weight: bold;
        border: none;
        border-bottom: 3px solid rgba(0, 0, 0, 0.2);
    }
    QPushButton:hover { 
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #DC2626, stop:1 #B91C1C);
        border-bottom: 5px solid rgba(0, 0, 0, 0.3);
        margin-top: -2px;
        padding-bottom: 10px;
    }
    QPushButton:pressed {
        margin-top: 2px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
"""

NAV_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #293438,
            stop:1 #1D2429);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 500;
        border-bottom: 3px solid rgba(0, 0, 0, 0.2);
        outline: none;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #242C30,
            stop:1 #0F1314);
        border-bottom: 5px solid rgba(0, 0, 0, 0.3);
        margin-top: -2px;
        padding-bottom: 12px;
    }
    QPushButton:pressed {
        margin-top: 2px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
    QPushButton:focus {
        outline: none;
    }
"""

ICON_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #293438,
            stop:1 #1D2429);
        color: white;
        border-radius: 20px;
        border: none;
        outline: none;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #242C30,
            stop:1 #0F1314);
    }
    QPushButton:focus {
        outline: none;
    }
"""

ICON_BUTTON_SECONDARY_STYLE = """
    QPushButton {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 20px;
        border: 2px solid rgba(41, 52, 56, 0.5);
        outline: none;
    }
    QPushButton:hover {
        background: rgba(255, 255, 255, 0.15);
        border: 2px solid #293438;
    }
    QPushButton:focus {
        outline: none;
    }
"""

EDIT_BUTTON_STYLE = """
    QPushButton { 
        background: rgba(255, 255, 255, 0.1); 
        color: #FFFFFF; 
        padding: 8px 14px; 
        border-radius: 6px; 
        font-weight: bold;
        border: 2px solid rgba(41, 52, 56, 0.5);
        border-bottom: 3px solid rgba(0, 0, 0, 0.2);
    }
    QPushButton:hover { 
        background: rgba(255, 255, 255, 0.15);
        border: 2px solid #293438;
        border-bottom: 5px solid rgba(41, 52, 56, 0.3);
        margin-top: -2px;
        padding-bottom: 10px;
    }
    QPushButton:pressed {
        margin-top: 2px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
"""

CARD_FRAME_STYLE = """
    QFrame {
        background: #2B3E50;
        border: 2px solid #4A5F7F;
        border-radius: 15px;
        outline: none;
    }
"""

GRAPH_CARD_STYLE = """
    QFrame {
        background: rgba(43, 62, 80, 0.6);
        border-radius: 16px;
        border: 2px solid #4A5F7F;
    }
"""

SIDEBAR_STYLE = """
    QFrame {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #293438,
            stop:1 #1D2429);
        border: none;
    }
"""

GUIDE_SECTION_STYLE = """
    QFrame {
        background: #34495E;
        border: 2px solid #4A5F7F;
        border-radius: 10px;
        padding: 12px;
        outline: none;
    }
"""

DROPDOWN_FRAME_STYLE = """
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid #293438;
    border-radius: 6px;
    padding:6px;
"""

TABLE_STYLE = """
    QTableWidget {
        background: rgba(255, 255, 255, 0.05);
        color: #FFFFFF;
        border: 2px solid #293438;
        border-radius: 8px;
        gridline-color: #293438;
        selection-background-color: rgba(41, 52, 56, 0.3);
    }
    QHeaderView::section {
        background-color: #293438;
        color: #FFFFFF;
        padding: 8px;
        font-weight: bold;
        border: none;
    }
"""

TABLE_ALTERNATE_STYLE = """
    QTableWidget {
        background: rgba(255, 255, 255, 0.05);
        alternate-background-color: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        gridline-color: #1E90FF;
        selection-background-color: rgba(30, 144, 255, 0.3);
        font-size: 10pt;
    }
    QHeaderView::section {
        background-color: #CAE9FF;
        color: #1B4965;
        font-weight: bold;
        font-size: 10pt;
        padding: 4px;
        border: none;
    }
    QTableWidget::item {
        padding: 3px;
    }
"""

TABLE_NO_SELECTION_STYLE = """
    QTableWidget {
        background: rgba(255, 255, 255, 0.05);
        alternate-background-color: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        gridline-color: #1E90FF;
        selection-background-color: transparent;
        selection-color: #FFFFFF;
        font-size: 10pt;
    }
    QHeaderView::section {
        background-color: #CAE9FF;
        color: #1B4965;
        font-weight: bold;
        font-size: 10pt;
        padding: 4px;
        border: none;
    }
    QTableWidget::item {
        padding: 3px;
    }
    QTableWidget::item:selected {
        background: transparent;
        color: #FFFFFF;
    }
    QTableWidget::item:focus {
        background: transparent;
        outline: none;
    }
    QTableWidget::item:hover {
        background: transparent;
    }
"""

SCROLLBAR_STYLE = """
    QScrollArea {
        background: transparent;
        border: none;
    }
    QScrollBar:vertical {
        background: rgba(255, 255, 255, 0.1);
        width: 10px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: rgba(255, 255, 255, 0.5);
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""

PROGRESS_BAR_STYLE = """
    QProgressBar {
        background-color: rgba(62, 78, 94, 0.5);
        border-radius: 4px;
        border: none;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #EF5350,
            stop:1 #E53935);
        border-radius: 4px;
    }
"""

MENU_BAR_STYLE = """
    QMenuBar {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #293438,
            stop:0.25 #242C30,
            stop:0.5 #1D2429,
            stop:0.75 #0F1314,
            stop:1 #010100);
        color: white;
        padding: 2px;
    }
    QMenuBar::item {
        background-color: transparent;
        color: white;
        padding: 4px 12px;
    }
    QMenuBar::item:selected {
        background-color: rgba(255, 255, 255, 0.1);
    }
    QMenu {
        background-color: #1D2429;
        color: white;
        border: 1px solid #293438;
    }
    QMenu::item {
        padding: 6px 30px 6px 20px;
    }
    QMenu::item:selected {
        background-color: #242C30;
    }
"""

MESSAGE_BOX_STYLE = """
    QMessageBox {
        background-color: #2B3E50;
    }
    QLabel {
        color: #FFFFFF;
        font-size: 11pt;
    }
    QPushButton {
        background-color: #2a5298;
        color: white;
        padding: 8px 20px;
        border-radius: 6px;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: #1e3c72;
    }
"""

INFO_BOX_STYLE = """
    QLabel {
        background: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        border-radius: 10px;
        border: 2px solid rgba(41, 52, 56, 0.3);
        padding: 12px;
        margin: 8px;
    }
"""
