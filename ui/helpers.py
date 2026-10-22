"""Helper functions"""

from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QPainter, QLinearGradient, QColor
from PyQt6.QtCore import QPointF
from .styles import MESSAGE_BOX_STYLE


class PaintHelper:
    @staticmethod
    def paint_blue_gradient(widget, event):
        painter = QPainter(widget)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, widget.height()))
        gradient.setColorAt(0, QColor("#1e3c72"))
        gradient.setColorAt(0.5, QColor("#2a5298"))
        gradient.setColorAt(1, QColor("#1e3c72"))
        painter.fillRect(widget.rect(), gradient)


class ValidationHelper:
    @staticmethod
    def validate_not_empty(value, field_name):
        if not value:
            return False, f"{field_name} cannot be empty."
        return True, ""
    
    @staticmethod
    def validate_no_spaces(value, field_name):
        if " " in value:
            return False, f"{field_name} cannot contain spaces."
        return True, ""
    
    @staticmethod
    def validate_not_numeric_only(value, field_name):
        if value.isnumeric():
            return False, f"{field_name} must contain letters."
        return True, ""
    
    @staticmethod
    def validate_range(value, min_val, max_val, field_name):
        try:
            num = float(value)
            if num < min_val or num > max_val:
                return False, f"{field_name} must be between {min_val} and {max_val}."
            return True, ""
        except ValueError:
            return False, f"{field_name} must be a valid number."
    
    @staticmethod
    def validate_water_params(ph, temp, ammonia):
        errors = []
        
        valid, msg = ValidationHelper.validate_range(ph, 0, 14, "pH")
        if not valid:
            errors.append(msg)
        
        valid, msg = ValidationHelper.validate_range(temp, 0, 40, "Temperature")
        if not valid:
            errors.append(msg)
        
        valid, msg = ValidationHelper.validate_range(ammonia, 0, 10, "Ammonia")
        if not valid:
            errors.append(msg)
        
        if errors:
            return False, "\n".join(errors)
        return True, ""


class DialogHelper:
    @staticmethod
    def show_error(parent, title, message):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet(MESSAGE_BOX_STYLE)
        msg.exec()
    
    @staticmethod
    def show_success(parent, title, message):
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet(MESSAGE_BOX_STYLE)
        msg.exec()
    
    @staticmethod
    def show_confirmation(parent, title, message):
        reply = QMessageBox.question(
            parent,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class WindowHelper:
    @staticmethod
    def center_window(window):
        screen = QApplication.primaryScreen().availableGeometry()
        window_size = window.size()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        window.move(x, y)
    
    @staticmethod
    def toggle_fullscreen(window):
        if window.isFullScreen():
            window.showNormal()
        else:
            window.showFullScreen()


class DataHelper:
    @staticmethod
    def get_field(reading, attr, alt_keys):
        if hasattr(reading, attr):
            val = getattr(reading, attr)
            return "" if val is None else val
        if isinstance(reading, dict):
            for k in alt_keys:
                if k in reading:
                    val = reading[k]
                    return "" if val is None else val
        return ""
    
    @staticmethod
    def format_float(value, decimals=2):
        try:
            return f"{float(value):.{decimals}f}" if value not in ("", None) else ""
        except:
            return ""
    
    @staticmethod
    def filter_readings_by_name(readings, name):
        if not name:
            return readings
        return [r for r in readings if DataHelper.get_field(r, "name", ["name"]).lower() == name.lower()]


class WarningHelper:
    @staticmethod
    def generate_warnings(ph, temp, ammonia):
        from PyQt6.QtGui import QColor
        
        warnings = []
        
        if ph < 6.5:
            warnings.append(("⚠ pH too low", "Add pH buffer or check CO₂", 
                           QColor("#E65100"), QColor("#FFF3E0")))
        elif ph > 8.0:
            warnings.append(("⚠ pH too high", "Perform partial water change", 
                           QColor("#E65100"), QColor("#FFF3E0")))
        else:
            warnings.append(("✔ pH OK", "No immediate action", 
                           QColor("#2E7D32"), QColor("#E8F5E9")))
        
        if temp < 20:
            warnings.append(("❄ Temperature too low", "Increase heater temperature", 
                           QColor("#0277BD"), QColor("#E3F2FD")))
        elif temp > 28:
            warnings.append(("🔥 Temperature too high", "Cool the tank or improve ventilation", 
                           QColor("#C62828"), QColor("#FFEBEE")))
        else:
            warnings.append(("✔ Temperature OK", "No immediate action", 
                           QColor("#2E7D32"), QColor("#E8F5E9")))
        
        if ammonia > 0.5:
            warnings.append(("☠ High Ammonia Level", "Perform partial water change immediately", 
                           QColor("#B71C1C"), QColor("#FFEBEE")))
        elif ammonia > 0.2:
            warnings.append(("⚠ Moderate Ammonia", "Check filter and feed less", 
                           QColor("#E65100"), QColor("#FFF3E0")))
        else:
            warnings.append(("✔ Ammonia OK", "No immediate action", 
                           QColor("#2E7D32"), QColor("#E8F5E9")))
        
        return warnings
