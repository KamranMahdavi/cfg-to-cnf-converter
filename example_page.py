from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from PyQt5.QtCore import Qt

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

        self.setup_layout()
        self.setProperty("appContent", True)

    def setup_layout(self):
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.subtitle1, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.grammar_example_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.subtitle2, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.example_button)

        self.setLayout(main_layout)
        self.setAttribute(Qt.WA_StyledBackground, True)