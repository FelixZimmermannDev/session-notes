from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent, QCursor, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from backend.coding_session import SessionStatus
from backend.session_tracker import SessionTracker
from frontend.styles import DARK_STYLE, LIGHT_STYLE


class CodingSessionWidget(QWidget):
    def __init__(self, tracker, open_settings=None):
        super().__init__()
        self.tracker = tracker
        self.open_settings = open_settings
        self.today = date.today().isoformat()
        self.position = "top-right"
        self.always_on_top = True
        self.compact_mode = False

        self.setObjectName("sessionCard")
        self.setWindowTitle("Coding Session Tracker")

        self.title_label = QLabel("Coding Session")
        self.title_label.setObjectName("titleLabel")
        self.settings_button = QPushButton("⚙")
        self.settings_button.setObjectName("settingsButton")
        self.settings_button.setFixedWidth(30)
        self.hide_button = QPushButton("-")
        self.hide_button.setObjectName("windowControlButton")
        self.hide_button.setFixedWidth(30)
        self.close_button = QPushButton("×")
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedWidth(30)
        self.date_label = QLabel(f"Today: {self.today}")
        self.date_label.setObjectName("dateLabel")
        self.status_label = QLabel()
        self.status_label.setObjectName("statusLabel")

        self.coded_button = QPushButton("Coded")
        self.coded_button.setObjectName("codedButton")
        self.unset_button = QPushButton("Unset")
        self.unset_button.setObjectName("unsetButton")
        self.not_coded_button = QPushButton("Not coded")
        self.not_coded_button.setObjectName("notCodedButton")
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Note for today")
        self.save_note_button = QPushButton("Save note")
        self.save_note_button.setObjectName("saveNoteButton")

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_button)
        header_layout.addWidget(self.hide_button)
        header_layout.addWidget(self.close_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.coded_button)
        button_layout.addWidget(self.unset_button)
        button_layout.addWidget(self.not_coded_button)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(14, 14, 14, 14)
        self.layout.setSpacing(10)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.status_label)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.note_input)
        self.layout.addWidget(self.save_note_button)
        self.setLayout(self.layout)

        self.coded_button.clicked.connect(self.mark_coded)
        self.unset_button.clicked.connect(self.mark_unset)
        self.not_coded_button.clicked.connect(self.mark_not_coded)
        self.save_note_button.clicked.connect(self.save_note)
        self.hide_button.clicked.connect(self.hide)
        self.close_button.clicked.connect(QApplication.quit)
        if self.open_settings is not None:
            self.settings_button.clicked.connect(self.open_settings)

        self.resize(320, 190)
        self.show_as_floating()
        self.update_status_label()

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()

    def show_as_window(self):
        self.hide()
        self.setWindowFlags(Qt.Window)
        self.setWindowOpacity(1.0)
        self.resize(360, 220)
        self.show()
        self.update_status_label()

    def show_as_floating(self):
        self.hide()
        flags = Qt.Tool | Qt.FramelessWindowHint
        if self.always_on_top:
            flags = flags | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.resize(320, 190)
        self.move_to_position()
        self.show()
        self.update_status_label()

    def set_always_on_top(self, enabled):
        self.always_on_top = enabled
        if self.isVisible():
            self.show_as_floating()

    def set_position(self, position):
        self.position = position
        self.move_to_position()

    def set_compact_mode(self, enabled):
        self.compact_mode = enabled
        if enabled:
            self.date_label.hide()
            self.resize(280, 155)
            self.layout.setSpacing(7)
        else:
            self.date_label.show()
            self.resize(320, 190)
            self.layout.setSpacing(10)
        self.move_to_position()

    def move_to_position(self):
        screen = QApplication.primaryScreen()
        if screen is None:
            return

        margin = 20
        screen_area = screen.availableGeometry()

        if "right" in self.position:
            x = screen_area.right() - self.width() - margin
        else:
            x = screen_area.left() + margin

        if "bottom" in self.position:
            y = screen_area.bottom() - self.height() - margin
        else:
            y = screen_area.top() + margin

        self.move(x, y)

    def mark_coded(self):
        self.tracker.mark_day_coded(self.today)
        self.update_status_label()

    def mark_not_coded(self):
        self.tracker.mark_day_not_coded(self.today)
        self.update_status_label()

    def mark_unset(self):
        session = self.tracker.get_or_create_session(self.today)
        session.status = SessionStatus.UNSET
        self.update_status_label()

    def save_note(self):
        self.tracker.update_note_for_date(self.today, self.note_input.text())
        self.note_input.clear()
        self.update_status_label()

    def update_status_label(self):
        session = self.tracker.get_or_create_session(self.today)
        status = session.get_status().value
        self.status_label.setText(f"Status: {status}")

        if status == "coded":
            color = "#2ecc71"
        elif status == "uncoded":
            color = "#e74c3c"
        else:
            color = "#6b7280"

        self.status_label.setStyleSheet(f"background-color: {color}; color: white;")


class SettingsDialog(QDialog):
    def __init__(self, desktop_ui):
        super().__init__(desktop_ui.widget)
        self.desktop_ui = desktop_ui
        self.setWindowTitle("Settings")

        self.mode_input = QComboBox()
        self.mode_input.addItems(["Hidden", "Window", "Floating"])
        self.mode_input.setCurrentText(desktop_ui.mode)

        self.always_on_top_input = QCheckBox()
        self.always_on_top_input.setChecked(desktop_ui.widget.always_on_top)

        self.position_input = QComboBox()
        self.position_input.addItems(["top-right", "top-left", "bottom-right", "bottom-left"])
        self.position_input.setCurrentText(desktop_ui.widget.position)

        self.opacity_input = QComboBox()
        self.opacity_input.addItems(["100%", "90%", "80%"])
        self.opacity_input.setCurrentText(desktop_ui.opacity_label)

        self.theme_input = QComboBox()
        self.theme_input.addItems(["Dark", "Light"])
        self.theme_input.setCurrentText(desktop_ui.theme)

        self.compact_mode_input = QCheckBox()
        self.compact_mode_input.setChecked(desktop_ui.widget.compact_mode)

        save_button = QPushButton("Apply")
        save_button.clicked.connect(self.apply_settings)

        layout = QFormLayout()
        layout.addRow("Mode", self.mode_input)
        layout.addRow("Always on top", self.always_on_top_input)
        layout.addRow("Position", self.position_input)
        layout.addRow("Opacity", self.opacity_input)
        layout.addRow("Theme", self.theme_input)
        layout.addRow("Compact mode", self.compact_mode_input)
        layout.addRow(save_button)
        self.setLayout(layout)

    def apply_settings(self):
        self.desktop_ui.set_always_on_top(self.always_on_top_input.isChecked())
        self.desktop_ui.set_position(self.position_input.currentText())
        self.desktop_ui.set_opacity(self.opacity_input.currentText())
        self.desktop_ui.set_compact_mode(self.compact_mode_input.isChecked())
        self.desktop_ui.set_theme(self.theme_input.currentText())
        self.desktop_ui.set_mode(self.mode_input.currentText())

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.accept()
        else:
            super().keyPressEvent(event)


class DesktopUI:
    def __init__(self):
        QApplication.instance().setStyleSheet(DARK_STYLE)
        self.tracker = SessionTracker()
        self.settings_dialog = None
        self.widget = CodingSessionWidget(self.tracker, self.show_settings)
        self.mode = "Floating"
        self.opacity_label = "100%"
        self.theme = "Dark"
        self.tray_icon = self.create_tray_icon()

    def create_tray_icon(self):
        icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        tray_icon = QSystemTrayIcon(icon, QApplication.instance())
        tray_icon.setToolTip("Coding Session Tracker")

        menu = QMenu()

        show_action = QAction("Show", menu)
        settings_action = QAction("Settings", menu)
        hide_action = QAction("Hide", menu)
        quit_action = QAction("Quit", menu)

        show_action.triggered.connect(lambda: self.set_mode("Floating"))
        settings_action.triggered.connect(self.show_settings)
        hide_action.triggered.connect(lambda: self.set_mode("Hidden"))
        quit_action.triggered.connect(QApplication.quit)

        menu.addAction(settings_action)
        menu.addAction(show_action)
        menu.addAction(hide_action)
        menu.addAction(quit_action)

        tray_icon.setContextMenu(menu)
        tray_icon.activated.connect(self.handle_tray_click)
        return tray_icon

    def handle_tray_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.set_mode("Floating")
            self.tray_icon.contextMenu().popup(QCursor.pos())

    def set_mode(self, mode):
        self.mode = mode
        if mode == "Hidden":
            self.widget.hide()
        elif mode == "Window":
            self.widget.show_as_window()
        else:
            self.widget.show_as_floating()

    def set_always_on_top(self, enabled):
        self.widget.set_always_on_top(enabled)

    def set_position(self, position):
        self.widget.set_position(position)

    def set_opacity(self, opacity_label):
        self.opacity_label = opacity_label
        opacity_map = {
            "100%": 1.0,
            "90%": 0.9,
            "80%": 0.8,
        }
        self.widget.setWindowOpacity(opacity_map[opacity_label])

    def set_compact_mode(self, enabled):
        self.widget.set_compact_mode(enabled)

    def set_theme(self, theme):
        self.theme = theme
        if theme == "Light":
            QApplication.instance().setStyleSheet(LIGHT_STYLE)
        else:
            QApplication.instance().setStyleSheet(DARK_STYLE)
        self.widget.update_status_label()

    def show_settings(self):
        if self.settings_dialog is None or not self.settings_dialog.isVisible():
            self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.show()
        self.settings_dialog.raise_()
        self.settings_dialog.activateWindow()

    def run(self):
        self.set_mode("Floating")
        self.tray_icon.show()
