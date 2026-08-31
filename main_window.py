from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)

from PyQt5.QtCore import Qt
from convert_analyze_page import ConvertAnalyzeTab
from example_page import ExampleTab

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.header = QHBoxLayout()
        self.tabs = QTabWidget()
        self.options_button = QPushButton("☰ Options")

        self.setup_layout()

    def setup_layout(self):
        title = QLabel("CFG → CNF")
        self.header.addWidget(title, alignment=Qt.AlignCenter)
        self.header.addStretch()
        self.header.addWidget(self.options_button)

        example_tab = ExampleTab()
        convert_analyze_tab = ConvertAnalyzeTab()

        self.tabs.addTab(convert_analyze_tab, "Convert/Analyze")
        self.tabs.addTab(example_tab, "Explore Example")

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.header)
        main_layout.addWidget(self.tabs)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)