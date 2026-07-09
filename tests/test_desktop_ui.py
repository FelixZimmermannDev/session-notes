import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from backend.coding_session import CodingSession
from backend.session_tracker import SessionTracker
from frontend.desktop_ui import CodingSessionWidget, DesktopUI, FindDialog, SettingsDialog
from frontend.styles import DARK_STYLE, LIGHT_STYLE


@pytest.fixture
def app():
    existing_app = QApplication.instance()
    if existing_app is not None:
        return existing_app

    return QApplication([])


class FakeStorage:
    def __init__(self):
        self.saved_sessions = None
        self.save_call_count = 0

    def save_sessions(self, sessions):
        self.saved_sessions = list(sessions)
        self.save_call_count += 1


def test_desktop_widget_starts_on_current_session_one(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    assert widget.summary_label.text() == "Session: 1"


def test_desktop_widget_save_button_adds_session_and_shows_next_current_session(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)
    widget.note_input.setText("Worked on desktop UI")

    widget.save_note_button.click()

    sessions = tracker.get_sessions()
    assert len(sessions) == 1
    assert sessions[0].get_note() == "Worked on desktop UI"
    assert widget.note_input.text() == ""
    assert widget.summary_label.text() == "Session: 2"
    assert "#1" in widget.last_saved_label.text()


def test_desktop_widget_enter_adds_session(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)
    widget.note_input.setText("Saved with enter")

    widget.note_input.returnPressed.emit()

    assert tracker.get_sessions()[0].get_note() == "Saved with enter"
    assert widget.summary_label.text() == "Session: 2"


def test_desktop_widget_empty_note_shows_error(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    widget.save_note_button.click()

    assert tracker.get_sessions() == []
    assert widget.last_saved_label.text() == "Session note cannot be empty."


def test_desktop_widget_shortens_long_last_saved_note(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)
    long_note = "This is a very long note " * 20
    widget.note_input.setText(long_note)

    widget.save_note_button.click()

    assert widget.last_saved_label.text().endswith("...")
    assert len(widget.last_saved_label.text()) < len(long_note)


def test_desktop_ui_starts_with_loaded_sessions(app):
    tracker = SessionTracker()
    tracker.set_sessions([CodingSession(1, "2026-07-08", "Loaded desktop note")])

    ui = DesktopUI(tracker, FakeStorage())

    assert ui.tracker.get_sessions()[0].get_note() == "Loaded desktop note"
    assert ui.widget.summary_label.text() == "Session: 2"


def test_desktop_ui_saves_sessions_to_storage(app):
    tracker = SessionTracker()
    storage = FakeStorage()
    ui = DesktopUI(tracker, storage)
    ui.widget.note_input.setText("Saved from desktop")

    ui.widget.save_note_button.click()

    assert storage.save_call_count == 1
    assert len(storage.saved_sessions) == 1
    assert storage.saved_sessions[0].get_note() == "Saved from desktop"


def test_find_dialog_date_input_starts_empty(app):
    ui = DesktopUI()
    dialog = FindDialog(ui)

    assert dialog.date_input.text() == ""


def test_find_dialog_formats_date_input_with_dashes_and_only_allows_numbers(app):
    ui = DesktopUI()
    dialog = FindDialog(ui)

    dialog.date_input.setText("2026a07-08x")
    dialog.format_date_input(dialog.date_input.text())

    assert dialog.date_input.text() == "2026-07-08"


def test_find_dialog_limits_date_input_to_eight_digits(app):
    ui = DesktopUI()
    dialog = FindDialog(ui)

    dialog.date_input.setText("202607081234")
    dialog.format_date_input(dialog.date_input.text())

    assert dialog.date_input.text() == "2026-07-08"


def test_find_dialog_finds_session_by_number_and_clears_date_input(app):
    tracker = SessionTracker()
    tracker.add_session("First note")
    ui = DesktopUI()
    ui.tracker = tracker
    dialog = FindDialog(ui)

    dialog.date_input.setText("2026-07-08")
    dialog.number_input.setText("1")
    dialog.find_number_button.click()

    assert dialog.date_input.text() == ""
    assert "#1" in dialog.result_label.text()
    assert "First note" in dialog.result_label.text()


def test_find_dialog_finds_sessions_by_date_and_clears_number_input(app):
    tracker = SessionTracker()
    session = tracker.add_session("Today note")
    ui = DesktopUI()
    ui.tracker = tracker
    dialog = FindDialog(ui)

    dialog.number_input.setText("1")
    dialog.date_input.setText(session.get_date())
    dialog.find_date_button.click()

    assert dialog.number_input.text() == ""
    assert "Today note" in dialog.result_label.text()


def test_desktop_widget_buttons_have_style_object_names(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    assert widget.save_note_button.objectName() == "saveNoteButton"
    assert widget.find_button.objectName() == "findButton"
    assert widget.settings_button.objectName() == "settingsButton"
    assert widget.hide_button.objectName() == "windowControlButton"
    assert widget.close_button.objectName() == "closeButton"
    assert "#3498db" in DARK_STYLE
    assert "#2563eb" in LIGHT_STYLE
    assert "findButton" in DARK_STYLE
    assert "settingsButton" in LIGHT_STYLE


def test_desktop_ui_can_switch_between_hidden_window_and_floating_modes(app):
    ui = DesktopUI()

    ui.set_mode("Hidden")
    assert ui.mode == "Hidden"
    assert ui.widget.isHidden() is True

    ui.set_mode("Window")
    assert ui.mode == "Window"
    assert ui.widget.isVisible() is True
    assert not ui.widget.windowFlags() & Qt.FramelessWindowHint

    ui.set_mode("Floating")
    assert ui.mode == "Floating"
    assert ui.widget.isVisible() is True
    assert ui.widget.windowFlags() & Qt.FramelessWindowHint


def test_desktop_ui_settings_are_stored_in_memory(app):
    ui = DesktopUI()

    ui.set_position("bottom-left")
    ui.set_opacity("80%")
    ui.set_compact_mode(True)
    ui.set_always_on_top(False)
    ui.set_theme("Light")

    assert ui.widget.position == "bottom-left"
    assert ui.opacity_label == "80%"
    assert ui.widget.compact_mode is True
    assert ui.widget.always_on_top is False
    assert ui.theme == "Light"


def test_tray_right_click_menu_has_settings_above_show(app):
    ui = DesktopUI()

    action_names = [action.text() for action in ui.tray_icon.contextMenu().actions()]

    assert action_names == ["Settings", "Show", "Hide", "Quit"]


def test_widget_hide_button_hides_widget(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    widget.hide_button.click()

    assert widget.isHidden() is True


def test_settings_dialog_apply_keeps_dialog_open(app):
    ui = DesktopUI()
    dialog = SettingsDialog(ui)
    dialog.show()

    dialog.mode_input.setCurrentText("Hidden")
    dialog.apply_settings()

    assert ui.mode == "Hidden"
    assert dialog.isVisible() is True


def test_settings_dialog_enter_closes_dialog(app):
    ui = DesktopUI()
    dialog = SettingsDialog(ui)
    dialog.show()

    event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
    dialog.keyPressEvent(event)

    assert dialog.isVisible() is False


def test_widget_settings_button_opens_settings_dialog(app):
    ui = DesktopUI()

    ui.widget.settings_button.click()

    assert ui.settings_dialog is not None
    assert ui.settings_dialog.isVisible() is True


def test_widget_find_button_opens_find_dialog(app):
    ui = DesktopUI()

    ui.widget.find_button.click()

    assert ui.find_dialog is not None
    assert ui.find_dialog.isVisible() is True
