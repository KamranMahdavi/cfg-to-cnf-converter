from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from PyQt5.QtCore import Qt

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
        self.analyze = QPushButton("Analyze Grammar")

        self.setup_layout()

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