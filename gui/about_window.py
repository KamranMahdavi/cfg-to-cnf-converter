from PyQt5.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget
)

from PyQt5.QtCore import Qt

class AboutWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = QLabel(
            "<span style= 'font-weight: bold;'>CFG to CNF Converter</span>"
        )
        self.description = QLabel(
            "An educational app that converts context-free\n"
            "grammars to Chomsky Normal Form. Features an\n" 
            "Analysis Mode that allows the user to see each\n"  
            "step of conversion and the changes made at that step."
        )
        self.creator = QLabel("Made by Kamran Mahdavi")
        self.language_and_package = QLabel("Created with Python and PyQt5")
        self.github = QLabel(
            "Github: "
            '<a href="https://github.com/KamranMahdavi/cfg-to-cnf-converter" '
            'style= "color: rgb(40, 140, 200);">'
            'Link'
            '</a>'
        )

        self.setup_layout()
        self.setWindowTitle("About")

    def setup_layout(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.description)
        self.description.setWordWrap(True)
        main_layout.addWidget(self.creator)
        main_layout.addWidget(self.language_and_package)
        main_layout.addWidget(self.github)
        self.github.setOpenExternalLinks(True)

        central_widget = QWidget()
        central_widget.setProperty("appContent", True)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)