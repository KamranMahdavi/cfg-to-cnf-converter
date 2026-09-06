from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from PyQt5.QtCore import Qt
from .analyze_window import AnalyzeWindow
from .convert_window import ConvertWindow

class ConvertAnalyzeTab(QWidget):

    def __init__(self):
        super().__init__()
        self.subtitle1 = QLabel(
            "Understand Chomsky Normal Form\nstep by step."
        )
        self.subtitle1.setAlignment(Qt.AlignCenter)
        self.subtitle2 = QLabel(
            "Convert a context-free grammar "
            "directly to CNF, or see\nhow each "
            "conversion step changes it."
        )
        self.subtitle2.setAlignment(Qt.AlignCenter)
        self.convert = QPushButton("Convert Grammar")
        self.convert_window_ = None
        self.analyze = QPushButton("Analyze Grammar")
        self.analyze_window_ = None

        self.setup_connections()
        self.setup_layout()
        self.setProperty("appContent", True)

    def setup_connections(self):
        self.convert.clicked.connect(self.show_convert_window)
        self.analyze.clicked.connect(self.show_analyze_window)

    def setup_layout(self):
        main_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(self.convert)
        buttons_layout.addWidget(self.analyze)

        main_layout.addWidget(self.subtitle1, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.subtitle2, alignment=Qt.AlignCenter)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def show_convert_window(self):
        if self.convert_window_:
            self.convert_window_.raise_()
            self.convert_window_.activateWindow()
        else:
            self.convert_window_ = ConvertWindow()
            self.convert_window_.setAttribute(Qt.WA_DeleteOnClose)
            self.convert_window_.destroyed.connect(self.clear_references_convert)
            self.convert_window_.show()

    def clear_references_convert(self):
        self.convert_window_ = None

    def show_analyze_window(self):
        if self.analyze_window_:
            self.analyze_window_.raise_()
            self.analyze_window_.activateWindow()
        else:
            self.analyze_window_ = AnalyzeWindow()
            self.analyze_window_.setAttribute(Qt.WA_DeleteOnClose)
            self.analyze_window_.destroyed.connect(self.clear_references_analyze)
            self.analyze_window_.show()

    def clear_references_analyze(self):
        self.analyze_window_ = None
