from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QMainWindow    
)

from PyQt5.QtCore import Qt
from convert_analyze_page import ConvertAnalyzeTab
from example_page import ExampleTab

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()

        self.setup_layout()

    def setup_layout(self):

        example_tab = ExampleTab()
        convert_analyze_tab = ConvertAnalyzeTab()

        self.tabs.addTab(convert_analyze_tab, "Convert/Analyze")
        self.tabs.addTab(example_tab, "Explore Example")

        self.setCentralWidget(self.tabs)