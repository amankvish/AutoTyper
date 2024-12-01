import sys
import time
import threading
from random import uniform
import pyautogui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QWidget, QComboBox, QRadioButton, QFileDialog, QShortcut
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from docx import Document  # To handle Word files


class AutoTyperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoTyper - Designed by IoT Labs")
        self.setGeometry(100, 100, 800, 650)
        self.is_typing = False
        self.thread = None  # Thread for typing process
        self.set_ui_style()

        # Main Layout
        layout = QVBoxLayout()

        # Header
        header = QLabel("AutoTyper")
        header.setStyleSheet("color: #2980b9; font-size: 36px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Control Buttons
        button_layout = QHBoxLayout()
        self.copy_button = self.create_button("Copy", "#3498db")
        self.paste_button = self.create_button("Paste", "#1abc9c")
        self.cut_button = self.create_button("Cut", "#e74c3c")
        self.clear_button = self.create_button("Clear", "#f39c12")
        self.load_button = self.create_button("Load Text", "#9b59b6")

        # Add Buttons
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.paste_button)
        button_layout.addWidget(self.cut_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.load_button)
        layout.addLayout(button_layout)

        # Text Box
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet(
            "font-size: 16px; background-color: #ecf0f1; color: black; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.text_edit)

        # Typing Options (Speed, Style)
        typing_options_layout = QHBoxLayout()
        self.speed_label = QLabel("Typing Speed:")
        self.speed_label.setStyleSheet("font-size: 16px; color: white;")

        self.speed_dropdown = QComboBox()
        self.speed_dropdown.addItems(["60 WPM", "100 WPM", "150 WPM"])
        self.speed_dropdown.setCurrentIndex(0)  # Default to 60 WPM
        self.speed_dropdown.setStyleSheet(""" 
            QComboBox {
                font-size: 14px;
                background-color: #bdc3c7;
                color: black;
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox:hover {
                background-color: #ecf0f1;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #ecf0f1;
                selection-background-color: #2980b9;
                color: black;
            }
        """)

        typing_options_layout.addWidget(self.speed_label)
        typing_options_layout.addWidget(self.speed_dropdown)

        self.style_label = QLabel("Typing Style:")
        self.style_label.setStyleSheet("font-size: 16px; color: white;")
        self.style_normal = QRadioButton("Normal")
        self.style_caps = QRadioButton("Uppercase")
        self.style_lower = QRadioButton("Lowercase")
        self.style_sentence = QRadioButton("Sentence Case")
        self.style_normal.setChecked(True)

        typing_style_layout = QHBoxLayout()
        typing_style_layout.addWidget(self.style_normal)
        typing_style_layout.addWidget(self.style_caps)
        typing_style_layout.addWidget(self.style_lower)
        typing_style_layout.addWidget(self.style_sentence)

        layout.addWidget(self.style_label)
        layout.addLayout(typing_style_layout)
        layout.addLayout(typing_options_layout)

        # Start and Stop Buttons
        start_stop_layout = QHBoxLayout()
        self.start_button = self.create_button("Start Typing", "#2ecc71", font_size="18px")
        self.stop_button = self.create_button("Stop Typing", "#c0392b", font_size="18px")
        start_stop_layout.addWidget(self.start_button)
        start_stop_layout.addWidget(self.stop_button)
        layout.addLayout(start_stop_layout)

        # Footer
        footer = QLabel("Paste your code and wait for 5 seconds.")
        footer.setStyleSheet("color: white; font-size: 14px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        # Main Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect Buttons
        self.start_button.clicked.connect(self.start_typing)
        self.stop_button.clicked.connect(self.stop_typing)
        self.copy_button.clicked.connect(self.copy_text)
        self.paste_button.clicked.connect(self.paste_text)
        self.cut_button.clicked.connect(self.cut_text)
        self.clear_button.clicked.connect(self.clear_text)
        self.load_button.clicked.connect(self.load_text)

        # Keyboard Shortcut to Stop Typing
        self.stop_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.stop_shortcut.activated.connect(self.stop_typing)

    def set_ui_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                color: white;
            }
            QRadioButton {
                color: white;
                font-size: 14px;
            }
        """)

    def create_button(self, text, color, font_size="16px"):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                font-size: {font_size};
                background-color: {color};
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 15px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
            QPushButton:pressed {{
                background-color: #1abc9c;
            }}
        """)
        return button

    def start_typing(self):
        text = self.text_edit.toPlainText()
        if not text.strip():
            return  # Do nothing if text is empty

        self.is_typing = True
        self.thread = threading.Thread(target=self.typing_process, args=(text,))
        self.thread.start()

    def typing_process(self, text):
        typing_speed_map = {"60 WPM": 60, "100 WPM": 100, "150 WPM": 150}
        typing_speed = typing_speed_map[self.speed_dropdown.currentText()]
        delay_min = 60 / typing_speed  # Delay based on WPM

        for char in text:
            if not self.is_typing:
                return  # Stop typing if flag is set to False

            # Apply style based on radio buttons
            if self.style_caps.isChecked():
                char = char.upper()
            elif self.style_lower.isChecked():
                char = char.lower()
            elif self.style_sentence.isChecked() and char.isalpha():
                char = char.upper() if text.index(char) == 0 or text[text.index(char) - 1] == ' ' else char

            pyautogui.typewrite(char)
            time.sleep(uniform(delay_min / 10, delay_min / 5))  # Random delay for more natural typing

    def stop_typing(self):
        self.is_typing = False
        if self.thread and self.thread.is_alive():
            self.thread.join()  # Ensure the typing thread stops safely

    def copy_text(self):
        self.text_edit.selectAll()
        self.text_edit.copy()

    def paste_text(self):
        self.text_edit.paste()

    def cut_text(self):
        self.text_edit.selectAll()
        self.text_edit.cut()

    def clear_text(self):
        self.text_edit.clear()

    def load_text(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Text", "", "Text Files (*.txt);;Word Files (*.docx)"
        )
        if file_name:
            if file_name.endswith(".txt"):
                with open(file_name, "r") as file:
                    self.text_edit.setText(file.read())
            elif file_name.endswith(".docx"):
                document = Document(file_name)
                content = "\n".join([para.text for para in document.paragraphs])
                self.text_edit.setText(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoTyperApp()
    window.show()
    sys.exit(app.exec_())
