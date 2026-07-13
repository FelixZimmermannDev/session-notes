import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from backend.coding_session import CodingSession
from backend.session_tracker import SessionTracker
from frontend.desktop_ui import (
    CodingSessionWidget,
    DesktopUI,
    FindDialog,
    SettingsDialog,
)
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
    assert widget.last_saved_label.text() == "Please enter a session note"


def test_desktop_widget_does_not_hide_unexpected_value_errors(app, monkeypatch):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    def raise_unexpected_value_error(note):
        raise ValueError("Unexpected error")

    monkeypatch.setattr(tracker, "add_session", raise_unexpected_value_error)

    with pytest.raises(ValueError, match="Unexpected error"):
        widget.save_note()


def test_desktop_widget_uses_first_word_for_last_saved_note_preview(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)
    widget.note_input.setText("This is a very long note")

    widget.save_note_button.click()

    assert widget.last_saved_label.text().endswith("This...")
    assert "very long note" not in widget.last_saved_label.text()


def test_desktop_widget_shortens_very_long_first_word_in_last_saved_note(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)
    widget.note_input.setText("supercalifragilisticexpialidocious note")

    widget.save_note_button.click()

    assert widget.last_saved_label.text().endswith("supercalifragil...")


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


def test_find_dialog_finds_session_with_number_only(app):
    tracker = SessionTracker()
    tracker.add_session("First note")
    tracker.add_session("Second note")
    ui = DesktopUI()
    ui.tracker = tracker
    dialog = FindDialog(ui)

    dialog.number_input.setText("1")
    dialog.find_sessions_button.click()

    assert "#1" in dialog.result_label.text()
    assert "First note" in dialog.result_label.text()
    assert "Second note" not in dialog.result_label.text()
    assert dialog.result_panel.isHidden() is False
    assert dialog.update_selected_button.isHidden() is False
    assert dialog.archive_selected_button.isHidden() is False


def test_find_dialog_finds_sessions_with_note_only(app):
    tracker = SessionTracker()
    tracker.add_session("Worked on backend search")
    tracker.add_session("Learned JSON")
    ui = DesktopUI()
    ui.tracker = tracker
    dialog = FindDialog(ui)

    dialog.note_search_input.setText("BACKEND")
    dialog.find_sessions_button.click()

    assert "Worked on backend search" in dialog.result_label.text()
    assert "Learned JSON" not in dialog.result_label.text()
    assert dialog.result_panel.isHidden() is False
    assert dialog.update_selected_button.isHidden() is False
    assert dialog.archive_selected_button.isHidden() is False


def test_find_dialog_finds_sessions_with_date_only(app):
    tracker = SessionTracker()
    tracker.set_sessions([
        CodingSession(1, "2026-07-08", "First date"),
        CodingSession(2, "2026-07-09", "Second date"),
    ])
    ui = DesktopUI()
    ui.tracker = tracker
    dialog = FindDialog(ui)

    dialog.date_input.setText("2026-07-09")
    dialog.find_sessions_button.click()

    assert "Second date" in dialog.result_label.text()
    assert "First date" not in dialog.result_label.text()
    assert dialog.result_panel.isHidden() is False
    assert dialog.update_selected_button.isHidden() is False
    assert dialog.archive_selected_button.isHidden() is False


def test_find_dialog_does_not_find_archived_sessions(app):
    tracker = SessionTracker()
    session = tracker.add_session("Archived desktop note")
    tracker.archive_session(session.get_session_number())
    ui = DesktopUI(tracker)
    dialog = FindDialog(ui)
    dialog.note_search_input.setText("archived")

    dialog.find_sessions_button.click()

    assert dialog.result_label.text() == "No sessions found."
    assert dialog.result_panel.isHidden() is True


def test_find_dialog_combines_two_search_values(app):
    tracker = SessionTracker()
    tracker.set_sessions([
        CodingSession(1, "2026-07-08", "Backend work"),
        CodingSession(2, "2026-07-09", "Backend tests"),
        CodingSession(3, "2026-07-09", "Learned JSON"),
    ])
    ui = DesktopUI()
    ui.tracker = tracker
    dialog = FindDialog(ui)

    dialog.note_search_input.setText("backend")
    dialog.date_input.setText("2026-07-09")
    dialog.find_sessions_button.click()

    assert "Backend tests" in dialog.result_label.text()
    assert "Backend work" not in dialog.result_label.text()
    assert "Learned JSON" not in dialog.result_label.text()


def test_find_dialog_combines_all_three_search_values(app):
    tracker = SessionTracker()
    tracker.set_sessions([
        CodingSession(1, "2026-07-09", "Backend tests"),
        CodingSession(2, "2026-07-09", "Backend tests"),
    ])
    ui = DesktopUI()
    ui.tracker = tracker
    dialog = FindDialog(ui)

    dialog.number_input.setText("2")
    dialog.note_search_input.setText("backend")
    dialog.date_input.setText("2026-07-09")
    dialog.find_sessions_button.click()

    assert "#2" in dialog.result_label.text()
    assert "#1" not in dialog.result_label.text()


def test_find_dialog_requires_at_least_one_search_value(app):
    ui = DesktopUI()
    dialog = FindDialog(ui)

    dialog.find_sessions_button.click()

    assert dialog.result_label.text() == "Please enter at least one search value."


def test_find_dialog_rejects_non_numeric_session_number(app):
    ui = DesktopUI()
    dialog = FindDialog(ui)

    dialog.number_input.setText("not-a-number")
    dialog.find_sessions_button.click()

    assert dialog.result_label.text() == "Please enter a valid session number."


def test_desktop_widget_buttons_have_style_object_names(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    assert widget.save_note_button.objectName() == "saveNoteButton"
    assert widget.find_button.objectName() == "findButton"
    assert widget.find_button.text() == "Find / update / archive"
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


def test_find_dialog_updates_session_found_by_number_and_saves(app):
    tracker = SessionTracker()
    session = tracker.add_session("Old note")
    storage = FakeStorage()
    ui = DesktopUI(tracker, storage)
    dialog = FindDialog(ui)
    dialog.number_input.setText("1")

    dialog.find_sessions_button.click()
    dialog.update_selected_button.click()

    assert "Old note" in dialog.current_session_label.text()
    assert dialog.update_panel.isHidden() is False

    dialog.new_note_input.setText("  New note  ")
    dialog.save_update_button.click()

    assert session.get_note() == "New note"
    assert storage.save_call_count == 1
    assert storage.saved_sessions == [session]
    assert dialog.result_label.text() == "Session #1 updated: New note"


def test_find_dialog_can_choose_session_from_multiple_results_to_update(app):
    tracker = SessionTracker()
    first_session = CodingSession(1, "2026-07-09", "First note")
    second_session = CodingSession(2, "2026-07-09", "Second note")
    tracker.set_sessions([first_session, second_session])
    storage = FakeStorage()
    ui = DesktopUI(tracker, storage)
    dialog = FindDialog(ui)
    dialog.date_input.setText("2026-07-09")

    dialog.find_sessions_button.click()
    dialog.result_selector.setCurrentIndex(1)
    dialog.update_selected_button.click()
    dialog.new_note_input.setText("Updated second note")
    dialog.save_update_button.click()

    assert first_session.get_note() == "First note"
    assert second_session.get_note() == "Updated second note"
    assert storage.save_call_count == 1


def test_find_dialog_back_buttons_move_between_search_results_and_update(app):
    tracker = SessionTracker()
    tracker.add_session("Backend work")
    ui = DesktopUI(tracker, FakeStorage())
    dialog = FindDialog(ui)
    dialog.note_search_input.setText("backend")

    dialog.find_sessions_button.click()
    dialog.update_selected_button.click()
    dialog.update_back_button.click()

    assert dialog.result_panel.isHidden() is False
    assert dialog.update_panel.isHidden() is True

    dialog.results_back_button.click()

    assert dialog.search_panel.isHidden() is False
    assert dialog.result_panel.isHidden() is True


def test_find_dialog_archives_selected_session_and_saves(app):
    tracker = SessionTracker()
    session = tracker.add_session("Archive desktop note")
    storage = FakeStorage()
    ui = DesktopUI(tracker, storage)
    dialog = FindDialog(ui)
    dialog.number_input.setText("1")
    dialog.find_sessions_button.click()

    dialog.archive_selected_button.click()

    assert dialog.archive_panel.isHidden() is False
    assert "#1" in dialog.archive_session_label.text()
    assert session.get_date() in dialog.archive_session_label.text()
    assert "Archive desktop note" in dialog.archive_session_label.text()
    assert session.is_archived() is False
    assert storage.save_call_count == 0

    dialog.confirm_archive_button.click()

    assert session.is_archived() is True
    assert tracker.get_session_by_number(1) is None
    assert storage.save_call_count == 1
    assert storage.saved_sessions == [session]
    assert dialog.result_label.text() == (
        "Session #1 archived: Archive desktop note"
    )


def test_find_dialog_archive_back_button_cancels_archive(app):
    tracker = SessionTracker()
    session = tracker.add_session("Keep desktop note")
    storage = FakeStorage()
    ui = DesktopUI(tracker, storage)
    dialog = FindDialog(ui)
    dialog.note_search_input.setText("keep")
    dialog.find_sessions_button.click()
    dialog.archive_selected_button.click()

    dialog.archive_back_button.click()

    assert dialog.result_panel.isHidden() is False
    assert dialog.archive_panel.isHidden() is True
    assert session.is_archived() is False
    assert storage.save_call_count == 0


def test_find_dialog_removes_archived_session_from_multiple_results(app):
    tracker = SessionTracker()
    first_session = tracker.add_session("Shared archive keyword")
    second_session = tracker.add_session("Shared active keyword")
    storage = FakeStorage()
    ui = DesktopUI(tracker, storage)
    dialog = FindDialog(ui)
    dialog.note_search_input.setText("shared")
    dialog.find_sessions_button.click()
    dialog.result_selector.setCurrentIndex(0)
    dialog.archive_selected_button.click()

    dialog.confirm_archive_button.click()

    assert first_session.is_archived() is True
    assert second_session.is_archived() is False
    assert dialog.result_panel.isHidden() is False
    assert dialog.result_selector.count() == 1
    assert dialog.result_selector.currentData() == 2


def test_find_dialog_rejects_empty_update_and_keeps_old_note(app):
    tracker = SessionTracker()
    session = tracker.add_session("Old note")
    storage = FakeStorage()
    ui = DesktopUI(tracker, storage)
    dialog = FindDialog(ui)
    dialog.number_input.setText("1")
    dialog.find_sessions_button.click()
    dialog.update_selected_button.click()
    dialog.new_note_input.setText("   ")

    dialog.save_update_button.click()

    assert dialog.result_label.text() == "Please enter a session note"
    assert session.get_note() == "Old note"
    assert storage.save_call_count == 0
