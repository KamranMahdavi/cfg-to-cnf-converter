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

class AnalyzeWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.input_textbox = QPlainTextEdit()
        self.import_button = QPushButton("Import")
        self.analyze_button = QPushButton("Analyze")
        self.clear_button = QPushButton("Clear")

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
        self.setCentralWidget(central_widget)

    def clear_textbox(self):
        pass

    def analyze_grammar(self):
        pass

    def import_grammar_file(self):
        pass