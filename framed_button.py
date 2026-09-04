from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget
)

class FramedButton(QWidget):

    def __init__(self, text):
        super().__init__()
        self.button = QPushButton(text)
        self.setup_layout()

    def setup_layout(self):

        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.button)
        frame_layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(frame_layout)
        self.setObjectName("buttonFrame")