import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from backend.session_tracker import SessionTracker
from frontend.desktop_ui import CodingSessionWidget, DesktopUI, SettingsDialog
from frontend.styles import DARK_STYLE, LIGHT_STYLE


@pytest.fixture
def app():
    existing_app = QApplication.instance()
    if existing_app is not None:
        return existing_app

    return QApplication([])


def test_desktop_widget_coded_button_updates_status_label(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    widget.coded_button.click()

    assert widget.status_label.text() == "Status: coded"


def test_desktop_widget_not_coded_button_updates_status_label(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    widget.not_coded_button.click()

    assert widget.status_label.text() == "Status: uncoded"


def test_desktop_widget_unset_button_resets_status_label(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)
    widget.coded_button.click()

    widget.unset_button.click()

    assert widget.status_label.text() == "Status: unset"
    assert tracker.get_session_by_date(widget.today).is_unset() is True


def test_desktop_widget_submit_note_saves_note_and_keeps_status_visible(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)
    widget.coded_button.click()
    widget.note_input.setText("Worked on desktop UI")

    widget.save_note_button.click()

    session = tracker.get_session_by_date(widget.today)
    assert session.get_note() == "Worked on desktop UI"
    assert widget.note_input.text() == ""
    assert widget.status_label.text() == "Status: coded"


def test_desktop_widget_buttons_have_style_object_names(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    assert widget.coded_button.objectName() == "codedButton"
    assert widget.not_coded_button.objectName() == "notCodedButton"
    assert widget.unset_button.objectName() == "unsetButton"
    assert widget.unset_button.text() == "Unset"
    assert widget.save_note_button.objectName() == "saveNoteButton"
    assert widget.settings_button.objectName() == "settingsButton"
    assert widget.hide_button.objectName() == "windowControlButton"
    assert widget.close_button.objectName() == "closeButton"
    assert "#2ecc71" in DARK_STYLE
    assert "#e74c3c" in DARK_STYLE
    assert "#3498db" in DARK_STYLE
    assert "#6b7280" in DARK_STYLE
    assert "#2563eb" in LIGHT_STYLE
    assert "#71717a" in LIGHT_STYLE
    assert "settingsButton" in DARK_STYLE
    assert "settingsButton" in LIGHT_STYLE
    assert "windowControlButton" in DARK_STYLE
    assert "closeButton" in LIGHT_STYLE


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
