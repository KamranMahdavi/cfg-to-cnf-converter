from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)
from PyQt5.QtCore import Qt
from backend import analyze

class AnalysisViewer(QMainWindow):

    def __init__(self, grammar):
        super().__init__()
        self.steps = analyze(grammar)
        self.current_index = 0

        self.message_label = QLabel(f"Step {self.current_index} of {len(self.steps)}")
        self.title_label = QLabel(self.steps[0].title)
        self.description_label = QLabel(self.steps[0].description)
        self.slider = QSlider(Qt.Horizontal)
        self.previous_panel = GrammarPanel()
        self.current_panel = GrammarPanel()

        self.setup_connections()
        self.setup_layout()
        self.setWindowTitle("CFG to CNF Converter - Analysis")

    def setup_connections(self):
        self.slider.valueChanged.connect(self.navigate)

    def setup_layout(self):
        self.description_label.setAlignment(Qt.AlignCenter)
        self.slider.setRange(0, len(self.steps))
        self.slider.setSingleStep(1)
        self.previous_panel.hide()
        self.current_panel.display_productions(self.steps[self.current_index].snapshot)

        grammar_panel_layout = QHBoxLayout()
        grammar_panel_layout.addWidget(self.previous_panel, alignment=Qt.AlignCenter)
        grammar_panel_layout.addWidget(self.current_panel, alignment=Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(grammar_panel_layout)
        main_layout.addWidget(self.description_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.slider)
        main_layout.addWidget(self.message_label, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _get_change_types(self):
        previous_step = self.steps[self.current_index - 1].snapshot
        current_step = self.steps[self.current_index].snapshot
        removed = previous_step - current_step
        added = current_step - previous_step
        return removed, added

    def navigate(self):
        pass

class GrammarPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.QLabel_list = []
        self.grammar_layout = QVBoxLayout()

        self.setLayout(self.grammar_layout)

    def clear_productions(self):
        for label in self.QLabel_list:
            label.deleteLater()
        self.QLabel_list.clear()

    def display_productions(self, productions, highlighted_productions=set(), change_type=""):
        self.clear_productions()
        for production in productions:
            to_add = QLabel(self._to_string(production, productions[production]))
            if production in highlighted_productions:
                to_add.setProperty("changeType", change_type)
            self.QLabel_list.append(to_add)
            self.grammar_layout.addWidget(to_add)

    def _to_string(self, lhs, rhs):
        rhs_list = []
        for element in rhs:
            rhs_list.append(" ".join(element))
        string_rhs = " | ".join(rhs_list)
        return lhs + " → " + string_rhs