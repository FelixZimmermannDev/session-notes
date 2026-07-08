from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from backend.session_tracker import SessionTracker


class CodingSessionWidget(QWidget):
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker
        self.today = date.today().isoformat()

        self.setWindowTitle("Coding Session Tracker")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.status_label = QLabel("Status: unset")
        self.coded_button = QPushButton("Coded")
        self.not_coded_button = QPushButton("Not coded")
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Note for today")
        self.save_note_button = QPushButton("Submit note")

        self.coded_button.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
        self.not_coded_button.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        self.save_note_button.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.coded_button)
        button_layout.addWidget(self.not_coded_button)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Today: {self.today}"))
        layout.addWidget(self.status_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.note_input)
        layout.addWidget(self.save_note_button)
        self.setLayout(layout)

        self.coded_button.clicked.connect(self.mark_coded)
        self.not_coded_button.clicked.connect(self.mark_not_coded)
        self.save_note_button.clicked.connect(self.save_note)

        self.resize(300, 150)
        self.move_to_top_right()
        self.update_status_label()

    def move_to_top_right(self):
        screen = QApplication.primaryScreen()
        if screen is None:
            return

        screen_area = screen.availableGeometry()
        x = screen_area.right() - self.width() - 20
        y = screen_area.top() + 20
        self.move(x, y)

    def mark_coded(self):
        self.tracker.mark_day_coded(self.today)
        self.update_status_label()

    def mark_not_coded(self):
        self.tracker.mark_day_not_coded(self.today)
        self.update_status_label()

    def save_note(self):
        self.tracker.update_note_for_date(self.today, self.note_input.text())
        self.note_input.clear()
        self.status_label.setText("Status: unset")

    def update_status_label(self):
        session = self.tracker.get_or_create_session(self.today)
        self.status_label.setText(f"Status: {session.get_status().value}")


class DesktopUI:
    def __init__(self):
        self.tracker = SessionTracker()
        self.widget = CodingSessionWidget(self.tracker)
        self.tray_icon = self.create_tray_icon()

    def create_tray_icon(self):
        icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        tray_icon = QSystemTrayIcon(icon)
        tray_icon.setToolTip("Coding Session Tracker")

        menu = QMenu()

        show_action = QAction("Show widget")
        hide_action = QAction("Hide widget")
        mark_coded_action = QAction("Mark coded today")
        mark_not_coded_action = QAction("Mark not coded today")
        bug_report_action = QAction("Report bug")
        quit_action = QAction("Quit")

        show_action.triggered.connect(self.widget.show)
        hide_action.triggered.connect(self.widget.hide)
        mark_coded_action.triggered.connect(self.widget.mark_coded)
        mark_not_coded_action.triggered.connect(self.widget.mark_not_coded)
        bug_report_action.triggered.connect(self.show_bug_report_message)
        quit_action.triggered.connect(QApplication.quit)

        menu.addAction(show_action)
        menu.addAction(hide_action)
        menu.addSeparator()
        menu.addAction(mark_coded_action)
        menu.addAction(mark_not_coded_action)
        menu.addSeparator()
        menu.addAction(bug_report_action)
        menu.addAction(quit_action)

        tray_icon.setContextMenu(menu)
        tray_icon.activated.connect(self.handle_tray_click)
        return tray_icon

    def handle_tray_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.widget.show()
            self.tray_icon.contextMenu().popup(QCursor.pos())

    def show_bug_report_message(self):
        QMessageBox.information(
            self.widget,
            "Report bug",
            "Bug reporting is not connected yet. For now, write down what happened.",
        )

    def run(self):
        self.widget.show()
        self.tray_icon.show()
