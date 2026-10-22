"""Main application window"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMenuBar, QMessageBox, QApplication
from PyQt6.QtGui import QIcon, QKeySequence, QAction
from data_model import ReadingManager
from ui.utils import find_logo_path
from pages import LoadingPage, LoginPage, WelcomePage, HomePage, InputPage, HistoryPage, GraphPage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Traquarium")
        
        icon_path = find_logo_path()
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        
        self.setMinimumSize(1050, 750)
        self.resize(1050, 750)
        self.center_on_screen()

        self.current_user = None
        self.manager = None
        self.is_closing = False

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.create_menu_bar()
        main_layout.addWidget(self.menu_bar)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.loading_page = LoadingPage(self.stacked_widget)
        self.login_page = LoginPage(self.stacked_widget, main_window=self)
        self.welcome_page = WelcomePage(self.stacked_widget)

        self.stacked_widget.addWidget(self.loading_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.setCurrentIndex(0)

        self.setup_shortcuts()
    
    def center_on_screen(self):
        from ui.helpers import WindowHelper
        WindowHelper.center_window(self)

    def create_menu_bar(self):
        from ui.styles import MENU_BAR_STYLE
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setStyleSheet(MENU_BAR_STYLE)

        file_menu = self.menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.quit_app)
        file_menu.addAction(exit_action)

        help_menu = self.menu_bar.addMenu("Help")
        shortcuts_action = QAction("Keyboard Shortcuts", self)
        shortcuts_action.setShortcut(QKeySequence("F1"))
        shortcuts_action.triggered.connect(self.show_shortcuts_guide)
        help_menu.addAction(shortcuts_action)

        about_action = QAction("About Traquarium", self)
        about_action.setShortcut(QKeySequence("Ctrl+I"))
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_shortcuts(self):
        from PyQt6.QtGui import QShortcut, QKeySequence
        from PyQt6.QtCore import Qt
        
        fullscreen_shortcut = QShortcut(QKeySequence(Qt.Key.Key_F11), self)
        fullscreen_shortcut.activated.connect(self.toggle_fullscreen)
    
    def toggle_fullscreen(self):
        from ui.helpers import WindowHelper
        WindowHelper.toggle_fullscreen(self)

    def show_shortcuts_guide(self):
        from ui.styles import MESSAGE_BOX_STYLE
        msg = QMessageBox(self)
        msg.setWindowTitle("Keyboard Shortcuts")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(
            "<b style='font-size: 14pt;'>Keyboard Shortcuts</b><br><br>"
            "<b>Navigation:</b><br>"
            "<table cellpadding='5'>"
            "<tr><td><b>Ctrl + H</b></td><td>→</td><td>Go to Home Page</td></tr>"
            "<tr><td><b>Ctrl + 1</b></td><td>→</td><td>Go to Input Page</td></tr>"
            "<tr><td><b>Ctrl + 2</b></td><td>→</td><td>Go to History Page</td></tr>"
            "<tr><td><b>Ctrl + 3</b></td><td>→</td><td>Go to Graph Page</td></tr>"
            "</table><br>"
            "<b>Application:</b><br>"
            "<table cellpadding='5'>"
            "<tr><td><b>F11</b></td><td>→</td><td>Toggle Fullscreen</td></tr>"
            "<tr><td><b>Ctrl + Q</b></td><td>→</td><td>Exit Application</td></tr>"
            "<tr><td><b>F1</b></td><td>→</td><td>Show This Help</td></tr>"
            "<tr><td><b>Ctrl + I</b></td><td>→</td><td>About Traquarium</td></tr>"
            "</table><br>"
            "<i>Tip: Use the menu bar at the top for additional options!</i>"
        )
        msg.setStyleSheet(MESSAGE_BOX_STYLE)
        msg.exec()

    def show_about(self):
        from ui.dialogs import AboutDialog
        dialog = AboutDialog(self)
        dialog.exec()

    def quit_app(self):
        if not self.is_closing:
            self.is_closing = True
            reply = QMessageBox.question(
                self,
                'Exit Traquarium',
                'Close Traquarium and save all data?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                QApplication.instance().quit()
            else:
                self.is_closing = False
    
    def closeEvent(self, event):
        if self.is_closing:
            event.accept()
            return
            
        reply = QMessageBox.question(
            self,
            'Exit Traquarium',
            'Close Traquarium and save all data?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def set_current_user(self, username):
        self.current_user = username
        self.manager = ReadingManager(username)

        self.home_page = HomePage(self.stacked_widget, self.manager, username)
        self.history_page = HistoryPage(self.stacked_widget, self.manager)
        self.graph_page = GraphPage(self.stacked_widget)
        self.input_page = InputPage(self.stacked_widget, self.history_page, self.graph_page, self.manager)

        while self.stacked_widget.count() > 3:
            widget = self.stacked_widget.widget(3)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.history_page)
        self.stacked_widget.addWidget(self.graph_page)

        readings = self.manager.get_all()
        self.home_page.update_latest(readings)
        self.history_page.update_table(readings)
        self.graph_page.update_graph(readings)
