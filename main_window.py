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

from PyQt5.QtCore import Qt, QPropertyAnimation
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
        self.setWindowTitle("CFG to CNF Converter")

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
        central_widget.setProperty("appContent", True)
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
        self.light_button = QPushButton("Light")
        self.dark_button = QPushButton("Dark")
        self.themes_frame = QWidget()
        self.about_button = QPushButton("About")
        self.help_button = QPushButton("Help")

        self.setup_connections()
        self.setup_layout()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

    def setup_connections(self):
        self.themes_button.clicked.connect(self.show_theme_options)

    def setup_layout(self):
        themes_layout = QVBoxLayout()
        themes_layout.addWidget(self.light_button)
        themes_layout.addWidget(self.dark_button)
        self.themes_frame.setLayout(themes_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.themes_button)
        main_layout.addWidget(self.themes_frame)
        self.themes_frame.hide()
        main_layout.addWidget(self.about_button)
        main_layout.addWidget(self.help_button)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def show_theme_options(self):
        if self.themes_frame.isVisible():
            self.themes_frame.hide()
        else:
            self.themes_frame.show()