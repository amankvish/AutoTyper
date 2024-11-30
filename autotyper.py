import sys
import json
import time
from random import random

import pyautogui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QWidget,
    QHeaderView, QDialog, QSpinBox, QTextEdit, QRadioButton, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence


class AddNewDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Add/Edit Record")
        self.setFixedSize(600, 450)
        self.setStyleSheet("""
            QDialog {
                background-color: #dfe6e9;
                border-radius: 10px;
                font-family: 'Arial', sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
            }
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                border: 2px solid #2980b9;
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff;
            }
            QTextEdit {
                min-height: 80px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 14px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)

        layout = QVBoxLayout(self)

        # Shortcut Key Input
        self.shortcut_key_label = QLabel("Shortcut Key:")
        self.shortcut_key_input = QLineEdit(self)
        self.shortcut_key_input.setPlaceholderText("Press keys")
        self.shortcut_key_input.setReadOnly(True)
        self.shortcut_key_input.keyPressEvent = self.capture_shortcut_key

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_shortcut_key)

        # Arrange Shortcut Key Input and Clear Button side by side
        shortcut_layout = QHBoxLayout()
        shortcut_layout.addWidget(self.shortcut_key_input)
        shortcut_layout.addWidget(self.clear_button)

        # Text Input
        self.text_input_label = QLabel("Text:")
        self.text_input = QTextEdit(self)

        # Random Delay Section
        self.delay_label = QLabel("Random Delay:")

        # Min and Max Delay Inputs
        self.delay_min_label = QLabel("Min:")
        self.delay_min = QSpinBox(self)
        self.delay_min.setRange(0, 5000)
        self.delay_min.setValue(15)  # Default delay is set to 15 ms

        self.delay_max_label = QLabel("Max:")
        self.delay_max = QSpinBox(self)
        self.delay_max.setRange(0, 5000)
        self.delay_max.setValue(15)  # Default delay max is also 15 ms

        # Speed Unit Option (Milliseconds/Seconds)
        self.speed_label = QLabel("Speed:")
        self.speed_combo = QComboBox(self)
        self.speed_combo.addItems(["ms", "s"])

        # Repeats
        self.repeats_label = QLabel("How Many Times to Type:")
        self.repeats_input = QSpinBox(self)
        self.repeats_input.setRange(1, 100)

        # Arrange Min, Max, Speed Unit, and Repeats side by side
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(self.delay_min_label)
        delay_layout.addWidget(self.delay_min)
        delay_layout.addWidget(self.delay_max_label)
        delay_layout.addWidget(self.delay_max)
        delay_layout.addWidget(self.speed_label)
        delay_layout.addWidget(self.speed_combo)
        delay_layout.addWidget(self.repeats_label)
        delay_layout.addWidget(self.repeats_input)

        # Typing Style
        self.typing_style_label = QLabel("Typing Style:")
        self.style_normal = QRadioButton("Type As it Is")
        self.style_caps = QRadioButton("Type All CAPS")
        self.style_sentence = QRadioButton("Type Sentence Case")
        self.style_lower = QRadioButton("Type Lowercase")
        self.style_normal.setChecked(True)

        # Arrange typing styles side by side
        typing_style_layout = QHBoxLayout()
        typing_style_layout.addWidget(self.style_normal)
        typing_style_layout.addWidget(self.style_caps)
        typing_style_layout.addWidget(self.style_sentence)
        typing_style_layout.addWidget(self.style_lower)

        # Buttons
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        # Add widgets to layout
        layout.addWidget(self.shortcut_key_label)
        layout.addLayout(shortcut_layout)

        layout.addWidget(self.text_input_label)
        layout.addWidget(self.text_input)

        layout.addWidget(self.delay_label)
        layout.addLayout(delay_layout)

        layout.addWidget(self.typing_style_label)
        layout.addLayout(typing_style_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def capture_shortcut_key(self, event):
        key = QKeySequence(event.key() | int(event.modifiers()))
        self.shortcut_key_input.setText(key.toString())

    def clear_shortcut_key(self):
        self.shortcut_key_input.clear()


class AutoTyperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Typer")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
                font-family: 'Arial', sans-serif;
                font-size: 14px;
            }
            QTableWidget {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 14px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                margin-top: 10px;
            }
            QCheckBox {
                color: #34495e;
            }
        """)

        # Table to Display Entries
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Shortcut Key", "Text", "Delay", "Repeats", "Comments"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Buttons
        self.add_button = QPushButton("Add New")
        self.add_button.clicked.connect(self.show_add_new_dialog)
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.show_edit_dialog)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_selected_row)
        self.start_button = QPushButton("Start AutoTyper")
        self.start_button.clicked.connect(self.start_autotyper)

        # Layout for Buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.start_button)

        # Footer
        footer = QLabel("Designed and Developed by IoT Labs")
        footer.setAlignment(Qt.AlignCenter)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(footer)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.load_data()

    def show_add_new_dialog(self):
        dialog = AddNewDialog()
        if dialog.exec_() == QDialog.Accepted:
            shortcut = dialog.shortcut_key_input.text()
            text = dialog.text_input.toPlainText()
            delay_min = dialog.delay_min.value()
            delay_max = dialog.delay_max.value()
            repeats = dialog.repeats_input.value()

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(shortcut))
            self.table.setItem(row, 1, QTableWidgetItem(text))
            self.table.setItem(row, 2, QTableWidgetItem(f"{delay_min}-{delay_max}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(repeats)))

    def show_edit_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            data = []
            for col in range(self.table.columnCount()):
                data.append(self.table.item(selected_row, col).text())
            dialog = AddNewDialog(data)
            if dialog.exec_() == QDialog.Accepted:
                shortcut = dialog.shortcut_key_input.text()
                text = dialog.text_input.toPlainText()
                delay_min = dialog.delay_min.value()
                delay_max = dialog.delay_max.value()
                repeats = dialog.repeats_input.value()

                self.table.setItem(selected_row, 0, QTableWidgetItem(shortcut))
                self.table.setItem(selected_row, 1, QTableWidgetItem(text))
                self.table.setItem(selected_row, 2, QTableWidgetItem(f"{delay_min}-{delay_max}"))
                self.table.setItem(selected_row, 3, QTableWidgetItem(str(repeats)))

    def delete_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)

    def start_autotyper(self):
        rows = self.table.rowCount()
        for row in range(rows):
            # Get data from table
            shortcut = self.table.item(row, 0).text()
            text = self.table.item(row, 1).text()
            delay_str = self.table.item(row, 2).text().split('-')
            delay_min = int(delay_str[0])
            delay_max = int(delay_str[1])
            repeats = int(self.table.item(row, 3).text())

            # Typing logic (just a placeholder)
            for _ in range(repeats):
                pyautogui.typewrite(text)
                time.sleep(random.uniform(delay_min / 1000, delay_max / 1000))

    def load_data(self):
        # Load data into table (for demo purposes, static data is used here)
        data = [
            ["Ctrl+Alt+T", "Hello World!", "10-50", "5", "Test entry"]
        ]
        for entry in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(entry):
                self.table.setItem(row, col, QTableWidgetItem(value))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = AutoTyperApp()
    main_win.show()
    sys.exit(app.exec_())
