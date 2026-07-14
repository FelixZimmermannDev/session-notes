DARK_STYLE = """
QWidget {
    background-color: #171a21;
    color: #f4f7fb;
    font-size: 13px;
}

QLabel {
    background-color: transparent;
}

QWidget#sessionCard, QWidget#dialogCard {
    background-color: #222733;
    border: 1px solid #3b4352;
    border-radius: 12px;
}

QWidget#sessionCard {
    border-radius: 14px;
}

QLabel#dialogMessage {
    background-color: #172b3d;
    border: 1px solid #32658c;
    border-radius: 9px;
    padding: 10px 12px;
    color: #d8efff;
    font-weight: bold;
}

QLabel#sectionTitle {
    font-size: 15px;
    font-weight: bold;
}

QLabel#mutedLabel, QLabel#dateLabel {
    color: #adb8c8;
}

QLabel#sessionDetails {
    background-color: #11141a;
    border: 1px solid #3b4352;
    border-radius: 8px;
    padding: 10px;
}

QLabel#titleLabel {
    font-size: 16px;
    font-weight: bold;
}

QLabel#statusLabel {
    background-color: #2b313e;
    border: 1px solid #414b5d;
    border-radius: 8px;
    padding: 6px 10px;
    font-weight: bold;
}

QLabel#fieldLabel,
QComboBox#settingsComboBox,
QComboBox#settingsComboBox QAbstractItemView,
QCheckBox#settingsOption {
    color: #c0cad8;
    font-size: 12px;
    font-weight: bold;
}

QWidget#settingsCard, QWidget#settingsOptions {
    background-color: #222733;
    border: 1px solid #3b4352;
    border-radius: 10px;
}

QLineEdit, QComboBox {
    background-color: #101319;
    border: 1px solid #465063;
    border-radius: 8px;
    padding: 8px 10px;
    selection-background-color: #3498db;
    selection-color: white;
}

QLineEdit:hover, QComboBox:hover {
    border-color: #68758d;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #3498db;
}

QComboBox {
    padding-right: 32px;
}

QComboBox#settingsComboBox {
    padding: 6px 30px 6px 9px;
}

QComboBox#sessionSelector {
    min-height: 20px;
}

QComboBox QAbstractItemView {
    background-color: #222733;
    border: 1px solid #59667d;
    color: #f4f7fb;
    outline: none;
    padding: 4px;
    selection-background-color: #3498db;
    selection-color: white;
}

QCheckBox {
    spacing: 8px;
    background-color: transparent;
}

QCheckBox::indicator {
    width: 17px;
    height: 17px;
    background-color: #101319;
    border: 2px solid #59667d;
    border-radius: 4px;
}

QCheckBox::indicator:hover {
    border-color: #7fc5f4;
}

QCheckBox::indicator:checked {
    background-color: #3498db;
    border-color: #7fc5f4;
}

QCheckBox#settingsOption {
    padding: 4px 2px;
}

QPushButton {
    background-color: #343c4b;
    border: 1px solid #465063;
    border-radius: 8px;
    color: #f4f7fb;
    padding: 8px 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #414b5d;
    border-color: #68758d;
}

QPushButton:pressed {
    background-color: #29303c;
}

QPushButton#codedButton {
    background-color: #239b56;
    border-color: #2ecc71;
    color: white;
}

QPushButton#codedButton:hover {
    background-color: #2ecc71;
}

QPushButton#notCodedButton {
    background-color: #c83c32;
    border-color: #e74c3c;
    color: white;
}

QPushButton#notCodedButton:hover {
    background-color: #e74c3c;
}

QPushButton#unsetButton {
    background-color: #596273;
    border-color: #6f7a8f;
    color: white;
}

QPushButton#unsetButton:hover {
    background-color: #6b7280;
}

QPushButton#saveNoteButton, QPushButton#findButton,
QPushButton#primaryButton {
    background-color: #237eb8;
    border-color: #3498db;
    color: white;
}

QPushButton#primaryButton {
    font-size: 12px;
}

QPushButton#saveNoteButton:hover, QPushButton#findButton:hover,
QPushButton#primaryButton:hover {
    background-color: #3498db;
    border-color: #75c1f2;
}

QPushButton#settingsButton, QPushButton#windowControlButton {
    background-color: #343c4b;
    border-color: #465063;
    color: white;
    padding: 6px;
}

QPushButton#settingsButton:hover, QPushButton#windowControlButton:hover {
    background-color: #4a566a;
    border-color: #68758d;
}

QPushButton#closeButton {
    background-color: #512832;
    border-color: #713542;
    color: white;
    padding: 6px;
}

QPushButton#closeButton:hover {
    background-color: #b63d4c;
    border-color: #dc5968;
}

QPushButton#backButton {
    background-color: #343c4b;
    border-color: #59667d;
    color: #f4f7fb;
}

QPushButton#backButton:hover {
    background-color: #4a566a;
    border-color: #718099;
}

QWidget#sessionCard[compact="true"] QLabel#titleLabel {
    font-size: 15px;
}

QWidget#sessionCard[compact="true"] QLabel#statusLabel {
    padding: 4px 8px;
}

QWidget#sessionCard[compact="true"] QLineEdit,
QWidget#sessionCard[compact="true"] QPushButton {
    padding-top: 3px;
    padding-bottom: 3px;
}

QMenu {
    background-color: #222733;
    color: #f4f7fb;
    border: 1px solid #465063;
    padding: 4px;
}

QMenu::item {
    border-radius: 5px;
    padding: 7px 24px 7px 10px;
}

QMenu::item:selected {
    background-color: #3498db;
    color: white;
}

QDialog {
    background-color: #171a21;
}
"""


LIGHT_STYLE = """
QWidget {
    background-color: #edf2f7;
    color: #172033;
    font-size: 13px;
}

QLabel {
    background-color: transparent;
}

QWidget#sessionCard, QWidget#dialogCard {
    background-color: #ffffff;
    border: 1px solid #c7d2e0;
    border-radius: 12px;
}

QWidget#sessionCard {
    border: 2px solid #b9c7d8;
    border-radius: 14px;
}

QLabel#dialogMessage {
    background-color: #e5f1ff;
    border: 1px solid #86b9f4;
    border-radius: 9px;
    padding: 10px 12px;
    color: #153e75;
    font-weight: bold;
}

QLabel#sectionTitle {
    color: #153e75;
    font-size: 15px;
    font-weight: bold;
}

QLabel#mutedLabel, QLabel#dateLabel {
    color: #58677a;
}

QLabel#sessionDetails {
    background-color: #f3f6fa;
    border: 1px solid #c7d2e0;
    border-radius: 8px;
    padding: 10px;
}

QLabel#titleLabel {
    color: #153e75;
    font-size: 16px;
    font-weight: bold;
}

QLabel#statusLabel {
    background-color: #e7eef7;
    border: 1px solid #bdcadb;
    border-radius: 8px;
    color: #26364d;
    padding: 6px 10px;
    font-weight: bold;
}

QLabel#fieldLabel,
QComboBox#settingsComboBox,
QComboBox#settingsComboBox QAbstractItemView,
QCheckBox#settingsOption {
    color: #58677a;
    font-size: 12px;
    font-weight: bold;
}

QWidget#settingsCard, QWidget#settingsOptions {
    background-color: #ffffff;
    border: 1px solid #c7d2e0;
    border-radius: 10px;
}

QLineEdit, QComboBox {
    background-color: #ffffff;
    border: 1px solid #aebdce;
    border-radius: 8px;
    color: #172033;
    padding: 8px 10px;
    selection-background-color: #2563eb;
    selection-color: white;
}

QLineEdit:hover, QComboBox:hover {
    border-color: #7489a3;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #2563eb;
}

QComboBox {
    padding-right: 32px;
}

QComboBox#settingsComboBox {
    padding: 6px 30px 6px 9px;
}

QComboBox#sessionSelector {
    min-height: 20px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #8ea2ba;
    color: #172033;
    outline: none;
    padding: 4px;
    selection-background-color: #2563eb;
    selection-color: white;
}

QCheckBox {
    spacing: 8px;
    background-color: transparent;
}

QCheckBox::indicator {
    width: 17px;
    height: 17px;
    background-color: #ffffff;
    border: 2px solid #8ea2ba;
    border-radius: 4px;
}

QCheckBox::indicator:hover {
    border-color: #2563eb;
}

QCheckBox::indicator:checked {
    background-color: #2563eb;
    border-color: #1d4ed8;
}

QCheckBox#settingsOption {
    padding: 4px 2px;
}

QPushButton {
    background-color: #dce6f1;
    border: 1px solid #aebdce;
    border-radius: 8px;
    color: #172033;
    padding: 8px 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #c9d7e7;
    border-color: #7489a3;
}

QPushButton:pressed {
    background-color: #b9c9dc;
}

QPushButton#codedButton {
    background-color: #16864a;
    border-color: #10723d;
    color: white;
}

QPushButton#codedButton:hover {
    background-color: #20a35b;
    border-color: #16864a;
}

QPushButton#notCodedButton {
    background-color: #c83232;
    border-color: #a82424;
    color: white;
}

QPushButton#notCodedButton:hover {
    background-color: #e04444;
    border-color: #c83232;
}

QPushButton#unsetButton {
    background-color: #596579;
    border-color: #475367;
    color: white;
}

QPushButton#unsetButton:hover {
    background-color: #6b778a;
}

QPushButton#saveNoteButton, QPushButton#findButton,
QPushButton#primaryButton {
    background-color: #2563eb;
    border-color: #1d4ed8;
    color: white;
}

QPushButton#primaryButton {
    font-size: 12px;
}

QPushButton#saveNoteButton:hover, QPushButton#findButton:hover,
QPushButton#primaryButton:hover {
    background-color: #174fc7;
    border-color: #123fa3;
}

QPushButton#settingsButton, QPushButton#windowControlButton {
    background-color: #dce6f1;
    border-color: #aebdce;
    color: #153e75;
    padding: 6px;
}

QPushButton#settingsButton:hover, QPushButton#windowControlButton:hover {
    background-color: #c3d2e3;
    border-color: #7489a3;
}

QPushButton#closeButton {
    background-color: #ffe1e4;
    border-color: #ef9aa3;
    color: #8f1f2d;
    padding: 6px;
}

QPushButton#closeButton:hover {
    background-color: #dc3545;
    border-color: #b92534;
    color: white;
}

QPushButton#backButton {
    background-color: #e1e8f0;
    border-color: #aebdce;
    color: #26364d;
}

QPushButton#backButton:hover {
    background-color: #c9d7e7;
    border-color: #7489a3;
}

QWidget#sessionCard[compact="true"] QLabel#titleLabel {
    font-size: 15px;
}

QWidget#sessionCard[compact="true"] QLabel#statusLabel {
    padding: 4px 8px;
}

QWidget#sessionCard[compact="true"] QLineEdit,
QWidget#sessionCard[compact="true"] QPushButton {
    padding-top: 3px;
    padding-bottom: 3px;
}

QMenu {
    background-color: #ffffff;
    color: #172033;
    border: 1px solid #aebdce;
    padding: 4px;
}

QMenu::item {
    border-radius: 5px;
    padding: 7px 24px 7px 10px;
}

QMenu::item:selected {
    background-color: #2563eb;
    color: white;
}

QDialog {
    background-color: #edf2f7;
}
"""
