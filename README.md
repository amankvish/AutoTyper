# AutoTyper

```markdown
AutoTyper is a Python-based desktop application built using PyQt5 and pyautogui that allows you to automate typing tasks. The app can simulate typing with random delays, support multiple typing styles, and automate repetitive typing processes with customizable shortcut keys.

## Features

- Custom Shortcut Keys: Assign shortcut keys to start the auto-typing process.
- Text to Type: Define the text that should be typed when the shortcut is activated.
- Random Delay: Set a random delay (min/max) between key presses for more human-like typing.
- Typing Styles: Choose from multiple typing styles:
  - Normal: Type text as it is.
  - All CAPS: Type all text in uppercase.
  - Sentence Case: Capitalize the first letter of each sentence.
  - Lowercase: Type all text in lowercase.
- Repeats: Set how many times the text should be typed.
- Start/Stop Typing: Activate or stop auto-typing by pressing the assigned shortcut key.

---

## Installation

### Prerequisites

Before you install and run AutoTyper, make sure you have the following software installed on your machine:

- Python 3.x: [Download Python](https://www.python.org/downloads/)
- pip: Python’s package manager. If you don’t have it, install it from [here](https://pip.pypa.io/en/stable/installation/).

### Setting Up the Project

1. Clone the repository or download the source code:
   ```bash
   git clone https://github.com/yourusername/AutoTyper.git
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv autotyper_env
   source autotyper_env/bin/activate   # For Linux/macOS
   autotyper_env\Scripts\activate      # For Windows
   ```

3. Install dependencies:
   - Create and activate a virtual environment if you haven't already, then run the following:
   ```bash
   pip install -r requirements.txt
   ```
   This will install the required dependencies:
   - `PyQt5`: For the graphical user interface (GUI).
   - `pyautogui`: For simulating keystrokes.

---

## Running the Application

To run the AutoTyper GUI application, execute the following command in the terminal or command prompt:

```bash
python autotyper.py
```

This will launch the AutoTyper application window.

---

## Features in Detail

### 1. Add New Shortcut
   - Click the "Add New" button to add a new typing task.
   - You can configure the shortcut key, the text to type, the delay between key presses, the number of repetitions, and the typing style.

### 2. Edit Existing Shortcut
   - Select an existing row in the table and click the "Edit" button to modify the task.
   - Update the shortcut, text, delay, repetitions, and typing style as needed.

### 3. Delete Shortcut
   - Select the task from the table and click the "Delete" button to remove it.

### 4. Start AutoTyper
   - Press the "Start AutoTyper" button to activate the typing process. Once started, the app will type the text as defined, simulating human typing behavior based on the settings you've provided.

   - The typing process will start automatically after pressing the assigned shortcut key and will stop when the same key is pressed again.

### 5. Typing Style Options
   - You can choose from four typing styles:
     - Normal: Text is typed as-is.
     - All CAPS: Text is converted to uppercase before typing.
     - Sentence Case: The first letter of each sentence is capitalized.
     - Lowercase: All text is converted to lowercase.

### 6. Random Delay
   - Set Min and Max values for a random delay (in ms). This will introduce variability in the typing speed for a more natural look.
   - Optionally, set the delay unit to milliseconds (ms) or seconds (s).

### 7. Repeats
   - Configure how many times you want the text to be typed. This can be useful for automating repetitive tasks.

---

## PyInstaller – Creating a Standalone Executable

If you want to distribute the app as a standalone `.exe` file for Windows users, you can use PyInstaller to package the Python script into an executable.

### Steps to Create an Executable

1. Install PyInstaller (if not installed already):
   ```bash
   pip install pyinstaller
   ```

2. To generate the `.exe` file, run:
   ```bash
   pyinstaller --onefile --windowed autotyper.py
   ```

   The `--onefile` flag creates a single executable file, while `--windowed` suppresses the terminal/console window from appearing when the GUI is launched.

3. Once the build process completes, navigate to the `dist` directory. You will find the `autotyper.exe` file there.

4. You can now share the executable with others without requiring Python to be installed on their machines.

---

## Troubleshooting

If you encounter any issues with the application:

- Ensure you have installed all dependencies in the `requirements.txt` file.
- Double-check that your system's Python version is compatible (Python 3.6 or above).
- If there are any GUI layout issues, make sure your PyQt5 installation is up to date.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- PyQt5: Used for creating the graphical user interface.
- pyautogui: Used for simulating keystrokes and mouse movements.
- MIT License: This project is open-source and free to use.

---

## Contact

For any inquiries, bugs, or suggestions, feel free to open an issue on the GitHub repository or contact the project maintainer.
```

---

### `requirements.txt`

Here is the `requirements.txt` file which lists the dependencies needed for the project:

```
pyautogui
PyQt5
```

### Directory Structure

Here is an example of how your project directory structure should look:

```
AutoTyper/
│
├── autotyper.py           # The main Python script for the application
├── requirements.txt       # The list of dependencies for the project
├── README.md              # Detailed instructions for installation, usage, and more
├── autotyper_data.json    # The file where the auto-typing tasks are saved (JSON format)
└── LICENSE                # Open-source license for the project (MIT License)
```

---

With these two files (`README.md` and `requirements.txt`), your project is ready for distribution.