from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QPlainTextEdit,
    QMessageBox,
    QFileDialog
)

from PyQt5.QtCore import Qt
from .analysis_viewer import AnalysisViewer

class AnalyzeWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.input_textbox = QPlainTextEdit()
        self.import_button = QPushButton("Import")
        self.analyze_button = QPushButton("Analyze")
        self.clear_button = QPushButton("Clear")
        self.analysis_window = None

        self.input_textbox.setPlaceholderText(
            "Enter your context-free grammar here...\n\n"
            "OR\n\n"
            "Click the Import button below to upload a file."
        )

        self.setup_connections()
        self.setup_layout()
        self.setWindowTitle("CFG to CNF Converter - Analyze")

    def setup_connections(self):
        self.clear_button.clicked.connect(self.clear_textbox)
        self.analyze_button.clicked.connect(self.analyze_grammar)
        self.import_button.clicked.connect(self.import_grammar_file)

    def setup_layout(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.analyze_button)

        top_label = QLabel("CFG Input")
        main_layout.addWidget(top_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.input_textbox)
        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)
        central_widget.setProperty("appContent", True)
        self.setCentralWidget(central_widget)

    def clear_textbox(self):
        self.input_textbox.clear()

    def clear_window_pointer(self):
        self.analysis_window = None

    def analyze_grammar(self):
        if self.analysis_window is not None:
            self.analysis_window.raise_()
            self.analysis_window.activateWindow()
        else:
            input_grammar = self.input_textbox.toPlainText()
            if input_grammar == "":
                self.throw_error(2)
                return
            try:
                self.analysis_window = AnalysisViewer(input_grammar)
            except ValueError as error:
                self.throw_error(1, str(error))
                return
            self.analysis_window.setAttribute(Qt.WA_DeleteOnClose)
            self.analysis_window.destroyed.connect(self.clear_window_pointer)
            self.analysis_window.show()

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
                "Enter or import a context-free grammar before analysis."
            )
        elif type == 3:
            error_window = QMessageBox.critical(self, "Error Occurred", "Failed to open selected file.")
        elif type == 4:
            error_window = QMessageBox.critical(self, "Error Occurred", "Could not decode selected file.")