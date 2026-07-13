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
    QSizePolicy,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from backend.session_tracker import SessionTracker
from frontend.styles import DARK_STYLE, LIGHT_STYLE
from backend.coding_session import EmptyNoteError


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
        self.last_saved_label.setWordWrap(False)
        self.last_saved_label.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Preferred,
        )

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Write a session note")
        self.save_note_button = QPushButton("Save note")
        self.save_note_button.setObjectName("saveNoteButton")
        self.find_button = QPushButton("Find / update")
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
        except EmptyNoteError as error:
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
            note_preview = self.create_note_preview(last_session.get_note())
            self.last_saved_label.setText(
                f"Last saved: #{last_session.get_session_number()} "
                f"on {last_session.get_date()} — {note_preview}"
            )

    def create_note_preview(self, note):
        first_word = note.split()[0]

        if len(first_word) > 15:
            return first_word[:15] + "..."

        if len(note.split()) > 1:
            return first_word + "..."

        return first_word

    def show_find_dialog(self):
        if self.open_find is not None:
            self.open_find()


class FindDialog(QDialog):
    def __init__(self, desktop_ui):
        super().__init__(desktop_ui.widget)
        self.desktop_ui = desktop_ui
        self.tracker = desktop_ui.tracker
        self.setWindowTitle("Find / update sessions")
        self.matching_sessions = []
        self.selected_session_number = None

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Session number (optional)")

        self.note_search_input = QLineEdit()
        self.note_search_input.setPlaceholderText("Note keyword (optional)")

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD (optional)")
        self.is_formatting_date_input = False

        self.find_sessions_button = QPushButton("Find sessions")
        self.find_sessions_button.setObjectName("findButton")

        self.search_panel = QWidget()
        search_layout = QVBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.addWidget(QLabel("Session number"))
        search_layout.addWidget(self.number_input)
        search_layout.addWidget(QLabel("Note keyword"))
        search_layout.addWidget(self.note_search_input)
        search_layout.addWidget(QLabel("Date"))
        search_layout.addWidget(self.date_input)
        search_layout.addWidget(self.find_sessions_button)
        self.search_panel.setLayout(search_layout)

        self.result_label = QLabel("Enter one or more search values.")
        self.result_label.setWordWrap(True)

        self.result_selector = QComboBox()
        self.update_selected_button = QPushButton("Update selected")
        self.update_selected_button.setObjectName("findButton")
        self.results_back_button = QPushButton("Back")

        result_actions = QHBoxLayout()
        result_actions.addWidget(self.update_selected_button)
        result_actions.addWidget(self.results_back_button)

        self.result_panel = QWidget()
        result_layout = QVBoxLayout()
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.addWidget(QLabel("Select a session"))
        result_layout.addWidget(self.result_selector)
        result_layout.addLayout(result_actions)
        self.result_panel.setLayout(result_layout)
        self.result_panel.hide()

        self.current_session_label = QLabel()
        self.current_session_label.setWordWrap(True)
        self.new_note_input = QLineEdit()
        self.new_note_input.setPlaceholderText("New session note")
        self.save_update_button = QPushButton("Save update")
        self.save_update_button.setObjectName("saveNoteButton")
        self.update_back_button = QPushButton("Back")

        update_actions = QHBoxLayout()
        update_actions.addWidget(self.save_update_button)
        update_actions.addWidget(self.update_back_button)

        self.update_panel = QWidget()
        update_layout = QVBoxLayout()
        update_layout.setContentsMargins(0, 0, 0, 0)
        update_layout.addWidget(QLabel("Current session"))
        update_layout.addWidget(self.current_session_label)
        update_layout.addWidget(QLabel("New note"))
        update_layout.addWidget(self.new_note_input)
        update_layout.addLayout(update_actions)
        self.update_panel.setLayout(update_layout)
        self.update_panel.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.search_panel)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_panel)
        layout.addWidget(self.update_panel)
        self.setLayout(layout)

        self.number_input.returnPressed.connect(self.find_sessions)
        self.note_search_input.returnPressed.connect(self.find_sessions)
        self.date_input.textEdited.connect(self.format_date_input)
        self.date_input.returnPressed.connect(self.find_sessions)
        self.find_sessions_button.clicked.connect(self.find_sessions)
        self.update_selected_button.clicked.connect(self.begin_update)
        self.results_back_button.clicked.connect(self.show_search_step)
        self.new_note_input.returnPressed.connect(self.save_update)
        self.save_update_button.clicked.connect(self.save_update)
        self.update_back_button.clicked.connect(self.show_results_step)

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

    def find_sessions(self):
        number_text = self.number_input.text().strip()
        note_keyword = self.note_search_input.text().lower().strip()
        target_date = self.date_input.text().strip()

        if not number_text and not note_keyword and not target_date:
            self.result_label.setText("Please enter at least one search value.")
            return

        session_number = None
        if number_text:
            try:
                session_number = int(number_text)
            except ValueError:
                self.result_label.setText("Please enter a valid session number.")
                return

        matching_sessions = []

        for session in self.tracker.get_active_sessions():
            if (
                session_number is not None
                and session.get_session_number() != session_number
            ):
                continue

            if note_keyword and note_keyword not in session.get_note().lower():
                continue

            if target_date and session.get_date() != target_date:
                continue

            matching_sessions.append(session)

        if not matching_sessions:
            self.result_label.setText("No sessions found.")
            return

        self.matching_sessions = matching_sessions
        self.show_results_step()

    def show_search_step(self):
        self.result_panel.hide()
        self.update_panel.hide()
        self.search_panel.show()
        self.result_label.setText("Enter one or more search values.")

    def show_results_step(self):
        if not self.matching_sessions:
            self.show_search_step()
            return

        selected_number = self.result_selector.currentData()
        self.result_selector.clear()

        for session in self.matching_sessions:
            self.result_selector.addItem(
                self.format_session(session),
                session.get_session_number(),
            )

        if selected_number is not None:
            for index in range(self.result_selector.count()):
                if self.result_selector.itemData(index) == selected_number:
                    self.result_selector.setCurrentIndex(index)
                    break

        self.result_label.setText(
            "\n".join(
                self.format_session(session)
                for session in self.matching_sessions
            )
        )
        self.search_panel.hide()
        self.update_panel.hide()
        self.result_panel.show()

    def begin_update(self):
        session_number = self.result_selector.currentData()
        session = self.tracker.get_session_by_number(session_number)

        if session is None:
            self.result_label.setText("Session not found.")
            return

        self.selected_session_number = session_number
        self.current_session_label.setText(self.format_session(session))
        self.new_note_input.clear()
        self.result_label.setText(
            f"Enter a new note for session #{session_number}."
        )
        self.search_panel.hide()
        self.result_panel.hide()
        self.update_panel.show()
        self.new_note_input.setFocus()

    def save_update(self):
        try:
            session = self.tracker.update_session_note(
                self.selected_session_number,
                self.new_note_input.text(),
            )
        except EmptyNoteError as error:
            self.result_label.setText(str(error))
            return

        if session is None:
            self.result_label.setText("Session not found.")
            return

        self.desktop_ui.save_sessions()
        self.current_session_label.setText(self.format_session(session))
        self.result_label.setText(
            f"Session #{session.get_session_number()} updated: "
            f"{session.get_note()}"
        )
        self.new_note_input.clear()

    def format_session(self, session):
        return (
            f"#{session.get_session_number()} | "
            f"{session.get_date()} | "
            f"{session.get_note()}"
        )


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
        self.position_input.addItems(
            ["top-right", "top-left", "bottom-right", "bottom-left"]
        )
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
        self.widget = CodingSessionWidget(
            self.tracker,
            self.show_settings,
            self.save_sessions,
        )
        self.widget.open_find = self.show_find
        self.mode = "Floating"
        self.opacity_label = "100%"
        self.theme = "Dark"
        self.tray_icon = self.create_tray_icon()

    def create_tray_icon(self):
        icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogApplyButton
        )
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
