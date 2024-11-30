import sys
import time
import threading
import keyboard
import pyautogui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QWidget,
    QHeaderView, QMessageBox, QDialog, QGridLayout, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt


class AutoTyperApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto Typer by IoT Labs")
        self.setGeometry(200, 200, 900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        main_layout = QVBoxLayout()

        # Header with Branding
        header = QLabel("Auto Typer - Designed and Developed by IoT Labs")
        header.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #ffffff; background-color: #4CAF50; padding: 10px; text-align: center;"
        )
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Table for Records
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Shortcut Key", "Comment", "Text", "Delay", "Repeats"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet(
            "background-color: #f9f9f9; border: 1px solid #ddd; font-size: 14px;"
        )
        main_layout.addWidget(self.table)

        # Enable row selection by clicking anywhere
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add New")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.start_button = QPushButton("Start Auto Typer")

        for button in [self.add_button, self.edit_button, self.delete_button, self.start_button]:
            button.setStyleSheet(
                "padding: 10px; font-size: 14px; margin: 5px; background-color: #4CAF50; color: white; border-radius: 5px;"
            )
            button_layout.addWidget(button)

        main_layout.addLayout(button_layout)
        self.central_widget.setLayout(main_layout)

        # Connect Buttons
        self.add_button.clicked.connect(self.open_add_new_dialog)
        self.edit_button.clicked.connect(self.open_edit_dialog)
        self.delete_button.clicked.connect(self.delete_selected_row)
        self.start_button.clicked.connect(self.start_auto_typer)

        # Store records
        self.records = []

    def open_add_new_dialog(self):
        dialog = AddEditDialog(self)
        dialog.exec_()

    def open_edit_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a row to edit.")
            return

        dialog = AddEditDialog(self, selected_row)
        dialog.exec_()

    def delete_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return

        self.table.removeRow(selected_row)
        del self.records[selected_row]

    def add_to_table(self, shortcut, comment, text, delay, repeats, row_position=None):
        if row_position is None:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(shortcut))
        self.table.setItem(row_position, 1, QTableWidgetItem(comment))
        self.table.setItem(row_position, 2, QTableWidgetItem(text))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(delay)))
        self.table.setItem(row_position, 4, QTableWidgetItem(str(repeats)))

        if row_position >= len(self.records):
            self.records.append({"shortcut": shortcut, "comment": comment, "text": text, "delay": delay, "repeats": repeats})
        else:
            self.records[row_position] = {"shortcut": shortcut, "comment": comment, "text": text, "delay": delay, "repeats": repeats}

    def start_auto_typer(self):
        if not self.records:
            QMessageBox.warning(self, "No Records", "No auto-typing records found. Please add at least one.")
            return

        for record in self.records:
            shortcut = record["shortcut"]
            text = record["text"]
            delay = record["delay"]
            repeats = record["repeats"]

            keyboard.add_hotkey(shortcut, self.perform_typing, args=(text, delay, repeats))

        QMessageBox.information(self, "Auto Typer Started", "Auto Typer is now active. Press the configured shortcuts to trigger.")

    def perform_typing(self, text, delay, repeats):
        def type_text():
            for _ in range(repeats):
                for char in text:
                    pyautogui.typewrite(char)
                    time.sleep(delay / 1000.0)
                time.sleep(1)

        threading.Thread(target=type_text, daemon=True).start()


class AddEditDialog(QDialog):
    def __init__(self, parent=None, row=None):
        super().__init__(parent)

        self.row = row
        self.setWindowTitle("Add Record" if row is None else "Edit Record")
        self.setGeometry(300, 300, 600, 400)

        layout = QGridLayout()

        # Shortcut Key
        layout.addWidget(QLabel("Shortcut Key:"), 0, 0)
        self.shortcut_key = QLineEdit()
        self.shortcut_key.setPlaceholderText("Click here and press a shortcut")
        self.shortcut_key.setReadOnly(True)
        self.shortcut_key.mousePressEvent = self.capture_shortcut_key
        layout.addWidget(self.shortcut_key, 0, 1)

        # Text
        layout.addWidget(QLabel("Text to Type:"), 1, 0)
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input, 1, 1, 1, 2)

        # Comment
        layout.addWidget(QLabel("Comments:"), 2, 0)
        self.comment_input = QLineEdit()
        layout.addWidget(self.comment_input, 2, 1)

        # Delay Settings
        layout.addWidget(QLabel("Typing Delay (ms):"), 3, 0)
        self.delay_input = QSpinBox()
        self.delay_input.setRange(0, 5000)
        self.delay_input.setValue(150)
        layout.addWidget(self.delay_input, 3, 1)

        # Number of Repeats
        layout.addWidget(QLabel("Number of Times to Type:"), 4, 0)
        self.repeat_input = QSpinBox()
        self.repeat_input.setRange(1, 100)
        layout.addWidget(self.repeat_input, 4, 1)

        # Buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.save_record)
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout, 5, 1, 1, 2)

        self.setLayout(layout)

        if self.row is not None:
            record = self.parent().records[self.row]
            self.shortcut_key.setText(record["shortcut"])
            self.comment_input.setText(record["comment"])
            self.text_input.setText(record["text"])
            self.delay_input.setValue(record["delay"])
            self.repeat_input.setValue(record["repeats"])

    def capture_shortcut_key(self, event):
        QMessageBox.information(self, "Shortcut Capture", "Press a key combination now!")
        shortcut = keyboard.read_hotkey(suppress=True)
        self.shortcut_key.setText(shortcut)

    def save_record(self):
        shortcut = self.shortcut_key.text()
        comment = self.comment_input.text()
        text = self.text_input.toPlainText()
        delay = self.delay_input.value()
        repeats = self.repeat_input.value()

        if not shortcut.strip() or not text.strip():
            QMessageBox.warning(self, "Validation Error", "Shortcut Key and Text cannot be empty!")
            return

        if self.row is None:
            self.parent().add_to_table(shortcut, comment, text, delay, repeats)
        else:
            self.parent().add_to_table(shortcut, comment, text, delay, repeats, self.row)

        self.close()


# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoTyperApp()
    window.show()
    sys.exit(app.exec_())
