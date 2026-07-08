DARK_STYLE = """
QWidget {
    background-color: #1f2329;
    color: #f4f4f5;
    font-size: 13px;
}

QWidget#sessionCard {
    background-color: #252a32;
    border: 1px solid #3a404c;
    border-radius: 14px;
}

QLabel#titleLabel {
    font-size: 16px;
    font-weight: bold;
}

QLabel#dateLabel {
    color: #aeb6c2;
}

QLabel#statusLabel {
    border-radius: 8px;
    padding: 6px 10px;
    font-weight: bold;
}

QLineEdit {
    background-color: #15181d;
    border: 1px solid #3a404c;
    border-radius: 8px;
    padding: 8px;
}

QPushButton {
    border: none;
    border-radius: 8px;
    padding: 8px 10px;
    font-weight: bold;
}

QPushButton#codedButton {
    background-color: #2ecc71;
    color: white;
}

QPushButton#notCodedButton {
    background-color: #e74c3c;
    color: white;
}

QPushButton#unsetButton {
    background-color: #6b7280;
    color: white;
}

QPushButton#saveNoteButton, QPushButton#findButton {
    background-color: #3498db;
    color: white;
}

QPushButton#settingsButton, QPushButton#windowControlButton {
    background-color: #3a404c;
    color: white;
    padding: 6px;
}

QPushButton#closeButton {
    background-color: #4b2630;
    color: white;
    padding: 6px;
}

QPushButton:hover {
    opacity: 0.9;
}

QMenu {
    background-color: #252a32;
    color: #f4f4f5;
    border: 1px solid #3a404c;
}

QMenu::item:selected {
    background-color: #3498db;
}

QDialog, QComboBox, QCheckBox {
    background-color: #1f2329;
    color: #f4f4f5;
}
"""


LIGHT_STYLE = """
QWidget {
    background-color: #f4f4f5;
    color: #18181b;
    font-size: 13px;
}

QWidget#sessionCard {
    background-color: #ffffff;
    border: 1px solid #d4d4d8;
    border-radius: 14px;
}

QLabel#titleLabel {
    font-size: 16px;
    font-weight: bold;
}

QLabel#dateLabel {
    color: #52525b;
}

QLabel#statusLabel {
    border-radius: 8px;
    padding: 6px 10px;
    font-weight: bold;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #d4d4d8;
    border-radius: 8px;
    padding: 8px;
}

QPushButton {
    border: none;
    border-radius: 8px;
    padding: 8px 10px;
    font-weight: bold;
}

QPushButton#codedButton {
    background-color: #2ecc71;
    color: white;
}

QPushButton#notCodedButton {
    background-color: #e74c3c;
    color: white;
}

QPushButton#unsetButton {
    background-color: #71717a;
    color: white;
}

QPushButton#saveNoteButton, QPushButton#findButton {
    background-color: #2563eb;
    color: white;
}

QPushButton#settingsButton, QPushButton#windowControlButton {
    background-color: #e4e4e7;
    color: #18181b;
    padding: 6px;
}

QPushButton#closeButton {
    background-color: #fecdd3;
    color: #18181b;
    padding: 6px;
}

QMenu {
    background-color: #ffffff;
    color: #18181b;
    border: 1px solid #d4d4d8;
}

QMenu::item:selected {
    background-color: #2563eb;
    color: white;
}

QDialog, QComboBox, QCheckBox {
    background-color: #f4f4f5;
    color: #18181b;
}
"""
