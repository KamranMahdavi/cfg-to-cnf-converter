from PyQt5.QtWidgets import (
    QApplication,
    QTabWidget,
    QWidget,
    QFrame,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QGraphicsOpacityEffect
)

from PyQt5.QtCore import Qt, QPropertyAnimation, QAbstractAnimation
from .convert_analyze_page import ConvertAnalyzeTab
from .example_page import ExampleTab
from .about_window import AboutWindow
from .help_window import HelpWindow

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
        self.opacity_effect = QGraphicsOpacityEffect()
        self.themes_frame.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.themes_frame_open = False
        self.about_button = QPushButton("About")
        self.about_window_ = None
        self.help_button = QPushButton("Help")
        self.help_window_ = None

        self.setup_connections()
        self.setup_layout()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

    def setup_connections(self):
        self.themes_button.clicked.connect(self.show_theme_options)
        self.animation.finished.connect(self.hide_after_finish)
        self.light_button.clicked.connect(lambda: self.set_theme(False))
        self.dark_button.clicked.connect(lambda: self.set_theme())

        self.about_button.clicked.connect(self.show_about_window)
        self.help_button.clicked.connect(self.show_help_window)

    def setup_layout(self):
        themes_layout = QVBoxLayout()
        themes_layout.addWidget(self.light_button)
        themes_layout.addWidget(self.dark_button)
        self.themes_frame.setLayout(themes_layout)

        self.animation.setDuration(350)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.themes_button)
        main_layout.addWidget(self.themes_frame)
        self.themes_frame.hide()
        main_layout.addWidget(self.about_button)
        main_layout.addWidget(self.help_button)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def show_theme_options(self):
        if self.themes_frame_open == False:
            self.animation.setDirection(QAbstractAnimation.Forward)
            self.themes_frame.show()
            self.animation.start()
            self.themes_frame_open = True
        else:
            self.animation.setDirection(QAbstractAnimation.Backward)
            self.animation.start()
            self.themes_frame_open = False

    def hide_after_finish(self):
        if not self.themes_frame_open:
            self.themes_frame.hide()

    def set_theme(self, is_dark=True):
        app = QApplication.instance()
        if is_dark:
            with open("styles/dark.css", "r", encoding="utf-8") as file:
                style_sheet = file.read()
            app.setStyleSheet(style_sheet)
        else:
            app.setStyleSheet("")

    def show_about_window(self):
        if self.about_window_:
            self.about_window_.raise_()
            self.about_window_.activateWindow()
        else:
            self.about_window_ = AboutWindow()
            self.about_window_.setAttribute(Qt.WA_DeleteOnClose)
            self.about_window_.destroyed.connect(self.clear_references_about)
            self.about_window_.show()

    def clear_references_about(self):
        self.about_window_ = None

    def show_help_window(self):
        if self.help_window_:
            self.help_window_.raise_()
            self.help_window_.activateWindow()
        else:
            self.help_window_ = HelpWindow()
            self.help_window_.setAttribute(Qt.WA_DeleteOnClose)
            self.help_window_.destroyed.connect(self.clear_references_help)
            self.help_window_.show()

    def clear_references_help(self):
        self.help_window_ = None
