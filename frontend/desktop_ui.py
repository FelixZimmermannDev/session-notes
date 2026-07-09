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

from backend.session_tracker import SessionTracker
from frontend.styles import DARK_STYLE, LIGHT_STYLE


class CodingSessionWidget(QWidget):
    def __init__(self, tracker, open_settings=None, save_sessions=None):
        super().__init__()
        self.tracker = tracker
        self.open_settings = open_settings
        self.save_sessions = save_sessions
        self.open_find = None
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
        self.summary_label = QLabel("Session: 1")
        self.summary_label.setObjectName("statusLabel")
        self.last_saved_label = QLabel("Last saved: none")
        self.last_saved_label.setObjectName("dateLabel")

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Write a session note")
        self.save_note_button = QPushButton("Save note")
        self.save_note_button.setObjectName("saveNoteButton")
        self.find_button = QPushButton("Find")
        self.find_button.setObjectName("findButton")

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_button)
        header_layout.addWidget(self.hide_button)
        header_layout.addWidget(self.close_button)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.save_note_button)
        action_layout.addWidget(self.find_button)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(14, 14, 14, 14)
        self.layout.setSpacing(10)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.summary_label)
        self.layout.addWidget(self.last_saved_label)
        self.layout.addWidget(self.note_input)
        self.layout.addLayout(action_layout)
        self.setLayout(self.layout)

        self.note_input.returnPressed.connect(self.save_note)
        self.save_note_button.clicked.connect(self.save_note)
        self.find_button.clicked.connect(self.show_find_dialog)
        self.hide_button.clicked.connect(self.hide)
        self.close_button.clicked.connect(QApplication.quit)
        if self.open_settings is not None:
            self.settings_button.clicked.connect(self.open_settings)

        self.resize(340, 210)
        self.show_as_floating()
        self.update_summary()

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()

    def show_as_window(self):
        self.hide()
        self.setWindowFlags(Qt.Window)
        self.setWindowOpacity(1.0)
        self.resize(390, 240)
        self.show()
        self.update_summary()

    def show_as_floating(self):
        self.hide()
        flags = Qt.Tool | Qt.FramelessWindowHint
        if self.always_on_top:
            flags = flags | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.resize(340, 210)
        self.move_to_position()
        self.show()
        self.update_summary()

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
            self.last_saved_label.hide()
            self.resize(300, 165)
            self.layout.setSpacing(7)
        else:
            self.date_label.show()
            self.last_saved_label.show()
            self.resize(340, 210)
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

    def save_note(self):
        try:
            session = self.tracker.add_session(self.note_input.text())
        except ValueError as error:
            self.last_saved_label.setText(str(error))
            return

        if self.save_sessions is not None:
            self.save_sessions()

        self.note_input.clear()
        self.update_summary(session)

    def update_summary(self, last_session=None):
        sessions = self.tracker.get_sessions()
        self.summary_label.setText(f"Session: {len(sessions) + 1}")
        self.summary_label.setStyleSheet("background-color: #6b7280; color: white;")

        if last_session is not None:
            self.last_saved_label.setText(
                f"Last saved: #{last_session.get_session_number()} "
                f"on {last_session.get_date()} — {last_session.get_note()}"
            )

    def show_find_dialog(self):
        if self.open_find is not None:
            self.open_find()


class FindDialog(QDialog):
    def __init__(self, desktop_ui):
        super().__init__(desktop_ui.widget)
        self.desktop_ui = desktop_ui
        self.tracker = desktop_ui.tracker
        self.setWindowTitle("Find sessions")

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Session number")
        self.find_number_button = QPushButton("Find number")

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.is_formatting_date_input = False
        self.find_date_button = QPushButton("Find date")

        self.result_label = QLabel("Enter a session number or date.")
        self.result_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Find by number"))
        layout.addWidget(self.number_input)
        layout.addWidget(self.find_number_button)
        layout.addWidget(QLabel("Find by date"))
        layout.addWidget(self.date_input)
        layout.addWidget(self.find_date_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        self.number_input.returnPressed.connect(self.find_by_number)
        self.date_input.textEdited.connect(self.format_date_input)
        self.date_input.returnPressed.connect(self.find_by_date)
        self.find_number_button.clicked.connect(self.find_by_number)
        self.find_date_button.clicked.connect(self.find_by_date)

    def format_date_input(self, text):
        if self.is_formatting_date_input:
            return

        self.is_formatting_date_input = True
        digits = "".join(character for character in text if character.isdigit())[:8]

        if len(digits) <= 4:
            formatted_date = digits
        elif len(digits) <= 6:
            formatted_date = f"{digits[:4]}-{digits[4:]}"
        else:
            formatted_date = f"{digits[:4]}-{digits[4:6]}-{digits[6:]}"

        self.date_input.setText(formatted_date)
        self.date_input.setCursorPosition(len(formatted_date))
        self.is_formatting_date_input = False

    def find_by_number(self):
        self.date_input.clear()

        try:
            session_number = int(self.number_input.text())
        except ValueError:
            self.result_label.setText("Please enter a valid session number.")
            return

        session = self.tracker.get_session_by_number(session_number)
        if session is None:
            self.result_label.setText("No session found for that number.")
            return

        self.result_label.setText(self.format_session(session))

    def find_by_date(self):
        self.number_input.clear()
        sessions = self.tracker.get_sessions_by_date(self.date_input.text())
        if not sessions:
            self.result_label.setText("No sessions found for that date.")
            return

        self.result_label.setText("\n".join(self.format_session(session) for session in sessions))

    def format_session(self, session):
        return f"#{session.get_session_number()} | {session.get_date()} | {session.get_note()}"


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
    def __init__(self, tracker=None, storage=None):
        QApplication.instance().setStyleSheet(DARK_STYLE)
        self.tracker = tracker or SessionTracker()
        self.storage = storage
        self.settings_dialog = None
        self.find_dialog = None
        self.widget = CodingSessionWidget(self.tracker, self.show_settings, self.save_sessions)
        self.widget.open_find = self.show_find
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

    def save_sessions(self):
        if self.storage is not None:
            self.storage.save_sessions(self.tracker.get_sessions())

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
        self.widget.update_summary()

    def show_settings(self):
        if self.settings_dialog is None or not self.settings_dialog.isVisible():
            self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.show()
        self.settings_dialog.raise_()
        self.settings_dialog.activateWindow()

    def show_find(self):
        if self.find_dialog is None or not self.find_dialog.isVisible():
            self.find_dialog = FindDialog(self)
        self.find_dialog.show()
        self.find_dialog.raise_()
        self.find_dialog.activateWindow()

    def run(self):
        self.set_mode("Floating")
        self.tray_icon.show()
