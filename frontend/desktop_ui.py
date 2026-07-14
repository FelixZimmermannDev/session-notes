from datetime import date

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QAction, QCloseEvent, QCursor, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
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

from backend.coding_session import (
    CodingSession,
    EmptyNoteError,
    FutureDateError,
    InvalidDateError,
)
from backend.session_tracker import SessionTracker
from frontend.styles import DARK_STYLE, LIGHT_STYLE


class CodingSessionWidget(QWidget):
    def __init__(self, tracker, open_settings=None, save_sessions=None):
        super().__init__()
        self.session_tracker = tracker
        self.open_settings = open_settings
        self.save_sessions = save_sessions
        self.open_find = None
        self.today = date.today().isoformat()
        self.position = "top-right"
        self.always_on_top = True
        self.compact_mode = False
        self._drag_offset = None

        self.setObjectName("sessionCard")
        self.setWindowTitle("Coding Session Tracker")

        self.title_label = QLabel("Coding Session")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setCursor(Qt.CursorShape.SizeAllCursor)
        self.title_label.installEventFilter(self)
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
        self.find_button = QPushButton("Find / update / archive")
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

    def eventFilter(self, watched, event):
        if watched is self.title_label:
            if event.type() == QEvent.Type.MouseButtonPress:
                if self._begin_window_drag(event):
                    return True
            elif event.type() == QEvent.Type.MouseMove:
                if self._move_dragged_window(event):
                    return True
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if self._finish_window_drag(event):
                    return True

        return super().eventFilter(watched, event)

    def mousePressEvent(self, event: QMouseEvent):
        header_bottom = self.close_button.geometry().bottom()
        if event.position().y() <= header_bottom:
            if self._begin_window_drag(event):
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._move_dragged_window(event):
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._finish_window_drag(event):
            return

        super().mouseReleaseEvent(event)

    def _begin_window_drag(self, event):
        if not self.windowFlags() & Qt.FramelessWindowHint:
            return False

        if event.button() != Qt.MouseButton.LeftButton:
            return False

        self._drag_offset = (
            event.globalPosition().toPoint()
            - self.frameGeometry().topLeft()
        )
        event.accept()
        return True

    def _move_dragged_window(self, event):
        if self._drag_offset is None:
            return False

        if not event.buttons() & Qt.MouseButton.LeftButton:
            return False

        self.move(event.globalPosition().toPoint() - self._drag_offset)
        event.accept()
        return True

    def _finish_window_drag(self, event):
        if self._drag_offset is None:
            return False

        self._drag_offset = None
        event.accept()
        return True

    def show_as_window(self):
        self.hide()
        self.setWindowFlags(Qt.Window)
        self.setWindowOpacity(1.0)
        self._apply_layout_density(windowed=True)
        self.show()
        self.update_summary()

    def show_as_floating(self):
        self.hide()
        flags = Qt.Tool | Qt.FramelessWindowHint
        if self.always_on_top:
            flags = flags | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self._apply_layout_density(windowed=False)
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
        self.setProperty("compact", enabled)
        self.date_label.setVisible(not enabled)
        self.last_saved_label.setVisible(not enabled)
        self._apply_layout_density(
            windowed=not bool(self.windowFlags() & Qt.FramelessWindowHint)
        )

        for widget in [self, *self.findChildren(QWidget)]:
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.updateGeometry()
            widget.update()

        QApplication.instance().processEvents()
        self._apply_layout_density(
            windowed=not bool(self.windowFlags() & Qt.FramelessWindowHint)
        )
        self.move_to_position()

    def _apply_layout_density(self, windowed):
        if self.compact_mode:
            self.layout.setContentsMargins(8, 8, 8, 8)
            self.layout.setSpacing(5)
            control_width = 26
            size = (320, 170) if windowed else (285, 145)
        else:
            self.layout.setContentsMargins(14, 14, 14, 14)
            self.layout.setSpacing(10)
            control_width = 30
            size = (390, 240) if windowed else (340, 210)

        for button in (
            self.settings_button,
            self.hide_button,
            self.close_button,
        ):
            button.setFixedWidth(control_width)

        self.resize(*size)

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
            session = self.session_tracker.add_session(self.note_input.text())
        except EmptyNoteError as error:
            self.last_saved_label.setText(str(error))
            return

        if self.save_sessions is not None:
            self.save_sessions()

        self.note_input.clear()
        self.update_summary(session)

    def update_summary(self, last_session=None):
        next_session_number = self.session_tracker.get_next_session_number()
        self.summary_label.setText(f"Session: {next_session_number}")

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
        self.setWindowTitle("Find / update / archive sessions")
        self.setMinimumWidth(480)
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
        self.search_back_button = QPushButton("Back")
        self.search_back_button.setObjectName("backButton")

        self.search_panel = QWidget()
        self.search_panel.setObjectName("dialogCard")
        search_layout = QVBoxLayout()
        search_layout.setContentsMargins(14, 14, 14, 14)
        search_layout.setSpacing(8)
        search_layout.addWidget(QLabel("Session number"))
        search_layout.addWidget(self.number_input)
        search_layout.addWidget(QLabel("Note keyword"))
        search_layout.addWidget(self.note_search_input)
        search_layout.addWidget(QLabel("Date"))
        search_layout.addWidget(self.date_input)

        self.search_actions_layout = QHBoxLayout()
        self.search_actions_layout.addWidget(self.find_sessions_button, 1)
        self.search_actions_layout.addWidget(self.search_back_button, 1)
        search_layout.addLayout(self.search_actions_layout)
        self.search_panel.setLayout(search_layout)

        self.result_label = QLabel("Enter one or more search values.")
        self.result_label.setObjectName("dialogMessage")
        self.result_label.setWordWrap(True)

        self.results_title_label = QLabel("Matching sessions")
        self.results_title_label.setObjectName("sectionTitle")
        self.results_help_label = QLabel(
            "Choose a session below, then update or archive it."
        )
        self.results_help_label.setObjectName("mutedLabel")
        self.results_help_label.setWordWrap(True)

        self.result_selector = QComboBox()
        self.result_selector.setObjectName("sessionSelector")
        self.result_selector.setMinimumHeight(38)
        self.result_selector.setMaxVisibleItems(5)
        self.result_selector.setMinimumContentsLength(35)
        self.result_selector.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.result_selector.view().setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.update_selected_button = QPushButton("Update selected")
        self.update_selected_button.setObjectName("findButton")
        self.archive_selected_button = QPushButton("Archive session")
        self.archive_selected_button.setObjectName("closeButton")
        self.results_back_button = QPushButton("Back")
        self.results_back_button.setObjectName("backButton")

        result_actions = QHBoxLayout()
        result_actions.addWidget(self.update_selected_button)
        result_actions.addWidget(self.archive_selected_button)
        result_actions.addWidget(self.results_back_button)

        self.result_panel = QWidget()
        self.result_panel.setObjectName("dialogCard")
        result_layout = QVBoxLayout()
        result_layout.setContentsMargins(14, 14, 14, 14)
        result_layout.setSpacing(10)
        result_layout.addWidget(self.results_title_label)
        result_layout.addWidget(self.results_help_label)
        result_layout.addWidget(self.result_selector)
        result_layout.addLayout(result_actions)
        self.result_panel.setLayout(result_layout)
        self.result_panel.hide()

        self.current_session_label = QLabel()
        self.current_session_label.setObjectName("sessionDetails")
        self.current_session_label.setWordWrap(True)
        self.new_note_input = QLineEdit()
        self.new_note_input.setPlaceholderText("New session note")
        self.save_update_button = QPushButton("Save update")
        self.save_update_button.setObjectName("saveNoteButton")
        self.update_back_button = QPushButton("Back")
        self.update_back_button.setObjectName("backButton")

        update_actions = QHBoxLayout()
        update_actions.addWidget(self.save_update_button)
        update_actions.addWidget(self.update_back_button)

        self.update_panel = QWidget()
        self.update_panel.setObjectName("dialogCard")
        update_layout = QVBoxLayout()
        update_layout.setContentsMargins(14, 14, 14, 14)
        update_layout.setSpacing(10)
        update_layout.addWidget(QLabel("Current session"))
        update_layout.addWidget(self.current_session_label)
        update_layout.addWidget(QLabel("New note"))
        update_layout.addWidget(self.new_note_input)
        update_layout.addLayout(update_actions)
        self.update_panel.setLayout(update_layout)
        self.update_panel.hide()

        self.archive_session_label = QLabel()
        self.archive_session_label.setObjectName("sessionDetails")
        self.archive_session_label.setWordWrap(True)
        self.confirm_archive_button = QPushButton("Archive session")
        self.confirm_archive_button.setObjectName("closeButton")
        self.archive_back_button = QPushButton("Back")
        self.archive_back_button.setObjectName("backButton")

        archive_actions = QHBoxLayout()
        archive_actions.addWidget(self.confirm_archive_button)
        archive_actions.addWidget(self.archive_back_button)

        self.archive_panel = QWidget()
        self.archive_panel.setObjectName("dialogCard")
        archive_layout = QVBoxLayout()
        archive_layout.setContentsMargins(14, 14, 14, 14)
        archive_layout.setSpacing(10)
        archive_layout.addWidget(QLabel("Selected session"))
        archive_layout.addWidget(self.archive_session_label)
        archive_layout.addWidget(QLabel("Archive this session?"))
        archive_layout.addLayout(archive_actions)
        self.archive_panel.setLayout(archive_layout)
        self.archive_panel.hide()

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(self.search_panel)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_panel)
        layout.addWidget(self.update_panel)
        layout.addWidget(self.archive_panel)
        self.setLayout(layout)

        self.number_input.returnPressed.connect(self.find_sessions)
        self.note_search_input.returnPressed.connect(self.find_sessions)
        self.date_input.textEdited.connect(self.format_date_input)
        self.date_input.returnPressed.connect(self.find_sessions)
        self.find_sessions_button.clicked.connect(self.find_sessions)
        self.search_back_button.clicked.connect(self.close)
        self.update_selected_button.clicked.connect(self.begin_update)
        self.archive_selected_button.clicked.connect(self.begin_archive)
        self.results_back_button.clicked.connect(self.show_search_step)
        self.new_note_input.returnPressed.connect(self.save_update)
        self.save_update_button.clicked.connect(self.save_update)
        self.update_back_button.clicked.connect(self.show_results_step)
        self.confirm_archive_button.clicked.connect(self.confirm_archive)
        self.archive_back_button.clicked.connect(self.show_results_step)

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

        if target_date:
            try:
                target_date = CodingSession._clean_date(target_date)
            except (InvalidDateError, FutureDateError) as error:
                self.result_label.setText(str(error))
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
        self.archive_panel.hide()
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

        session_count = len(self.matching_sessions)
        session_word = "session" if session_count == 1 else "sessions"
        self.result_label.setText(
            f"{session_count} matching {session_word} found."
        )
        self.search_panel.hide()
        self.update_panel.hide()
        self.archive_panel.hide()
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
        self.archive_panel.hide()
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

    def begin_archive(self):
        session_number = self.result_selector.currentData()
        session = self.tracker.get_session_by_number(session_number)

        if session is None:
            self.result_label.setText("Session not found.")
            return

        self.selected_session_number = session_number
        self.archive_session_label.setText(self.format_session(session))
        self.result_label.setText(
            f"Confirm archiving session #{session_number}."
        )
        self.search_panel.hide()
        self.result_panel.hide()
        self.update_panel.hide()
        self.archive_panel.show()

    def confirm_archive(self):
        session = self.tracker.archive_session(
            self.selected_session_number
        )

        if session is None:
            self.result_label.setText("Session not found.")
            return

        self.desktop_ui.save_sessions()
        self.matching_sessions = [
            matching_session
            for matching_session in self.matching_sessions
            if matching_session.get_session_number()
            != session.get_session_number()
        ]

        if self.matching_sessions:
            self.show_results_step()
        else:
            self.result_panel.hide()
            self.update_panel.hide()
            self.archive_panel.hide()
            self.search_panel.show()

        self.result_label.setText(
            f"Session #{session.get_session_number()} archived: "
            f"{session.get_note()}"
        )

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
        self.setObjectName("settingsDialog")
        self.setWindowTitle("Settings")
        self.setMinimumWidth(380)

        self.mode_input = QComboBox()
        self.mode_input.addItems(["Hidden", "Window", "Floating"])
        self.mode_input.setCurrentText(desktop_ui.mode)

        self.position_input = QComboBox()
        self.position_input.addItems(
            ["top-right", "top-left", "bottom-right", "bottom-left"]
        )
        self.position_input.setCurrentText(desktop_ui.widget.position)

        self.theme_input = QComboBox()
        self.theme_input.addItems(["Dark", "Light"])
        self.theme_input.setCurrentText(desktop_ui.theme)

        self.opacity_input = QComboBox()
        self.opacity_input.addItems(["100%", "90%", "75%", "60%", "50%"])
        self.opacity_input.setMaxVisibleItems(5)
        self.opacity_input.setCurrentText(desktop_ui.opacity_label)

        settings_card = QWidget()
        settings_card.setObjectName("settingsCard")
        settings_layout = QGridLayout()
        settings_layout.setContentsMargins(14, 14, 14, 14)
        settings_layout.setHorizontalSpacing(18)
        settings_layout.setVerticalSpacing(9)

        fields = (
            ("Window mode", self.mode_input),
            ("Screen position", self.position_input),
            ("Opacity", self.opacity_input),
            ("Theme", self.theme_input),
        )
        for row, (label_text, field) in enumerate(fields):
            label = QLabel(label_text)
            label.setObjectName("fieldLabel")
            field.setObjectName("settingsComboBox")
            field.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )
            settings_layout.addWidget(label, row, 0)
            settings_layout.addWidget(field, row, 1)

        settings_layout.setColumnStretch(1, 1)
        settings_card.setLayout(settings_layout)

        self.always_on_top_input = QCheckBox("Always on top")
        self.always_on_top_input.setObjectName("settingsOption")
        self.always_on_top_input.setChecked(desktop_ui.widget.always_on_top)

        self.compact_mode_input = QCheckBox("Compact mode")
        self.compact_mode_input.setObjectName("settingsOption")
        self.compact_mode_input.setToolTip("Use compact layout")
        self.compact_mode_input.setChecked(desktop_ui.widget.compact_mode)

        options_card = QWidget()
        options_card.setObjectName("settingsOptions")
        options_layout = QHBoxLayout()
        options_layout.setContentsMargins(16, 13, 16, 13)
        options_layout.setSpacing(20)
        options_layout.addWidget(self.always_on_top_input)
        options_layout.addStretch()
        options_layout.addWidget(self.compact_mode_input)
        options_card.setLayout(options_layout)

        self.apply_button = QPushButton("Apply changes")
        self.apply_button.setObjectName("primaryButton")
        self.apply_button.setMinimumWidth(140)
        self.apply_button.clicked.connect(self.apply_settings)

        action_layout = QHBoxLayout()
        action_layout.addStretch()
        action_layout.addWidget(self.apply_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(settings_card)
        layout.addWidget(options_card)
        layout.addLayout(action_layout)
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
            "75%": 0.75,
            "60%": 0.6,
            "50%": 0.5,
        }
        self.widget.setWindowOpacity(opacity_map[opacity_label])

    def set_compact_mode(self, enabled):
        self.widget.set_compact_mode(enabled)

    def set_theme(self, theme):
        stylesheets = {
            "Dark": DARK_STYLE,
            "Light": LIGHT_STYLE,
        }
        if theme not in stylesheets:
            raise ValueError(f"Unknown theme: {theme}")

        self.theme = theme
        QApplication.instance().setStyleSheet(stylesheets[theme])

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
