import pytest
from PySide6.QtWidgets import QApplication

from backend.session_tracker import SessionTracker
from frontend.desktop_ui import CodingSessionWidget


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


def test_desktop_widget_submit_note_saves_note_then_resets_visible_fields(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)
    widget.coded_button.click()
    widget.note_input.setText("Worked on desktop UI")

    widget.save_note_button.click()

    session = tracker.get_session_by_date(widget.today)
    assert session.get_note() == "Worked on desktop UI"
    assert widget.note_input.text() == ""
    assert widget.status_label.text() == "Status: unset"


def test_desktop_widget_buttons_are_colorful(app):
    tracker = SessionTracker()
    widget = CodingSessionWidget(tracker)

    assert "#2ecc71" in widget.coded_button.styleSheet()
    assert "#e74c3c" in widget.not_coded_button.styleSheet()
    assert "#3498db" in widget.save_note_button.styleSheet()
