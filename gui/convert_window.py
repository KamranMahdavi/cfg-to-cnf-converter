from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QPlainTextEdit,
    QFrame,
    QMessageBox,
    QFileDialog
)

from PyQt5.QtCore import Qt
from backend.backend import convert

class ConvertWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.input_textbox = QPlainTextEdit()
        self.output_textbox = QPlainTextEdit()
        self.import_button = QPushButton("Import")
        self.convert_button = QPushButton("Convert")
        self.clear_button = QPushButton("Clear")

        self.input_textbox.setPlaceholderText(
            "Enter your context-free grammar here...\n\n"
            "OR\n\n"
            "Click the Import button below to upload a file."
        )
        self.output_textbox.setPlaceholderText(
            "Converted grammar will appear here..."
        )
        self.output_textbox.setReadOnly(True)

        self.setup_connections()
        self.setup_layout()
        self.setWindowTitle("CFG to CNF Converter - Convert")

    def setup_connections(self):
        self.clear_button.clicked.connect(self.clear_all)
        self.convert_button.clicked.connect(self.convert_grammar)
        self.import_button.clicked.connect(self.import_grammar_file)

    def setup_layout(self):
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        central_widget = QWidget()

        right_label = QLabel("CNF Output")

        left_label = QLabel("CFG Input")
        left_layout.addWidget(left_label, alignment=Qt.AlignCenter)
        left_layout.addWidget(self.input_textbox)

        divider_line = QFrame()
        divider_line.setFrameShape(QFrame.VLine)
        divider_line.setFrameShadow(QFrame.Sunken)

        right_label = QLabel("CNF Output")
        right_layout.addWidget(right_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.output_textbox)

        top_layout.addLayout(left_layout)
        top_layout.addWidget(divider_line)
        top_layout.addLayout(right_layout)

        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.convert_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)
        central_widget.setProperty("appContent", True)
        self.setCentralWidget(central_widget)

    def clear_all(self):
        self.input_textbox.clear()
        self.output_textbox.clear()

    def convert_grammar(self):
        input_grammar_string = self.input_textbox.toPlainText()
        if input_grammar_string == "":
            self.throw_error(2)
            return

        try:
            cnf_result = convert(input_grammar_string)
        except ValueError as error:
            self.throw_error(1, str(error))
            return
        else:
            self.output_textbox.setPlainText(cnf_result)

    def throw_error(self, type, message=""):
        error_window = QMessageBox(self)
        if type == 1:
            error_window.setWindowTitle("Error occurred")
            error_window.setText("Invalid Grammar Format")
            error_window.setInformativeText(message)
            error_window.setIcon(QMessageBox.Critical)
            error_window.exec_()
        elif type == 2:
            error_window = QMessageBox.warning(
                self,
                "Empty Input",
                "Enter or import a context-free grammar before converting."
            )
        elif type == 3:
            error_window = QMessageBox.critical(self, "Error Occurred", "Failed to open selected file.")
        elif type == 4:
            error_window = QMessageBox.critical(self, "Error Occurred", "Could not decode selected file.")

    def import_grammar_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Grammar File", "", "Text Files (*.txt)")
        if path == "":
            return
        try:
            with open(path, "r", encoding="utf-8") as file:
                contents = file.read()
            self.input_textbox.setPlainText(contents)
        except OSError:
            self.throw_error(3)
        except UnicodeDecodeError:
            self.throw_error(4)