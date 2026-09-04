from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QFrame,
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
        self.options_sidebar = OptionsSideBar()

        self.setup_connections()
        self.setup_layout()
        self.options_sidebar.hide()
        self.setMinimumWidth(490)

    def setup_connections(self):
        self.options_button.pressed.connect(self.toggle_sidebar)

    def setup_layout(self):
        title = QLabel("CFG → CNF")
        title.setObjectName("titleLabel")
        self.header.addWidget(title, alignment=Qt.AlignCenter)
        self.header.addStretch()
        self.header.addWidget(self.options_button)

        example_tab = ExampleTab()
        example_tab.setObjectName("exampleTab")
        convert_analyze_tab = ConvertAnalyzeTab()
        convert_analyze_tab.setObjectName("convertAnalyzeTab")

        self.tabs.addTab(convert_analyze_tab, "Convert/Analyze")
        self.tabs.addTab(example_tab, "Explore Example")

        contents_layout = QHBoxLayout()
        contents_layout.addWidget(self.tabs)
        contents_layout.addWidget(self.options_sidebar)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.header)
        main_layout.addLayout(contents_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def toggle_sidebar(self):
        if self.options_sidebar.isVisible():
            self.options_sidebar.hide()
        else:
            self.options_sidebar.show()


class OptionsSideBar(QFrame):

    def __init__(self):
        super().__init__()
        self.themes_button = QPushButton("Themes")
        self.about_button = QPushButton("About")
        self.help_button = QPushButton("Help")

        self.setup_layout()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

    def setup_layout(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.themes_button)
        main_layout.addWidget(self.about_button)
        main_layout.addWidget(self.help_button)
        main_layout.addStretch()

        self.setLayout(main_layout)