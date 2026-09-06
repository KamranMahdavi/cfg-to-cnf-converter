from PyQt5.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QLabel
)

from PyQt5.QtCore import Qt

class HelpWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.grammar_input_format = QLabel(
            '<span style= "font-weight: bold;">'
            'Grammar Input Format'
            '</span>'
        )
        self.input_format_explanation = QLabel(
            'Each variable and all its productions should be '
            'entered in one line. The start variable must be S. '
            'Whitespace is tolerated, and grammar symbols have '
            'multiple equivalents.' 
        )
        self.input_format_example = QLabel(
            'Below is an example of the prefered input format:\n'
            'S -> A B | a\n'
            'A -> a\n'
            'B -> b'
        )
        self.accepted_alternatives = QLabel(
            'As alternative symbols, for example, → may be used instead of '
            '->, and any of "λ", "eps" or "epsilon" may be used instead of ε. '
            'Many vertical bar variants like "¦" or "∣" are also accepted.\n'
        )

        self.analyze_mode_title = QLabel(
            '<span style= "font-weight: bold;">'
            'Analyze Mode'
            '</span>'
        )
        self.analyze_mode_explanation = QLabel(
            'Analyze Mode offers a more elaborate explanation of '
            'the conversion by walking you through the process. '
            'The first step always shows the original grammar, and '
            'the last step shows the completed CNF grammar. In '
            'intermediate steps, the grammar before and after each '
            'transformation is displayed side by side.'
        )

        self.highlighting_changes_title = QLabel(
            '<span style= "font-weight: bold;">'
            'Highlighting Changes'
            '</span>'
        )
        self.highlighting_changes_explanation = QLabel(
            'Added productions are highlighted in green, and the '
            'removed ones are highlighted in red. If a new variable '
            'gets added, the entire line becomes green. Changes are '
            'highlighted at the production level. This means when a '
            'production gets replaced, the entire right-hand side gets '
            'coloured even if some symbols appear unchanged between the '
            'old and the new productions.'
        )

        self.setup_layout()
        self.setWindowTitle("Help")

    def setup_layout(self):
        scroll_area = QScrollArea()
        main_layout = QVBoxLayout()
        central_layout = QVBoxLayout()
        content_widget = QWidget()
        central_widget = QWidget()

        main_layout.addWidget(self.grammar_input_format, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.input_format_explanation)
        self.input_format_explanation.setWordWrap(True)
        main_layout.addWidget(self.input_format_example)
        main_layout.addWidget(self.accepted_alternatives)
        self.accepted_alternatives.setWordWrap(True)

        main_layout.addWidget(self.analyze_mode_title, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.analyze_mode_explanation)
        self.analyze_mode_explanation.setWordWrap(True)

        main_layout.addWidget(self.highlighting_changes_title, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.highlighting_changes_explanation)
        self.highlighting_changes_explanation.setWordWrap(True)

        content_widget.setLayout(main_layout)
        content_widget.setObjectName("helpContent")
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        central_layout.addWidget(scroll_area)
        central_widget.setLayout(central_layout)
        central_widget.setProperty("appContent", True)
        self.setCentralWidget(central_widget)