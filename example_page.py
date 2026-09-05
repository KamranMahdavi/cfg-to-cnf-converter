from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from PyQt5.QtCore import Qt
from analysis_viewer import AnalysisViewer

class ExampleTab(QWidget):

    def __init__(self):
        super().__init__()
        self.subtitle1 = QLabel("Learn with an example:")
        self.grammar_example_label = QLabel(
            "S → ASB | aC\n"
            "A → ε | B\n"
            "B → b\n"
            "C → c\n"
        )
        self.subtitle2 = QLabel(
            "See how different steps like ε-removal\n"
            "or binarization transform this grammar."
        )
        self.subtitle2.setAlignment(Qt.AlignCenter)
        self.example_button = QPushButton("Explore Example")
        self.analysis_window = None

        self.setup_connections()
        self.setup_layout()
        self.setProperty("appContent", True)

    def setup_connections(self):
        self.example_button.clicked.connect(self.show_example)

    def setup_layout(self):
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.subtitle1, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.grammar_example_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.subtitle2, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.example_button)

        self.setLayout(main_layout)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def show_example(self):
        grammar = """
        S → A S B | a C
        A → ε | B
        B → b
        C → c
        """
        self.analysis_window = AnalysisViewer(grammar)
        self.analysis_window.setAttribute(Qt.WA_DeleteOnClose)
        self.analysis_window.destroyed.connect(self.clear_references)
        self.analysis_window.show()

    def clear_references(self):
        self.analysis_window = None