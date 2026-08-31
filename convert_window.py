from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QPlainTextEdit,
    QFrame
)

from PyQt5.QtCore import Qt

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
        self.setCentralWidget(central_widget)

    def clear_all(self):
        self.input_textbox.clear()
        self.output_textbox.clear()