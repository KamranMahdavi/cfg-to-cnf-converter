from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QGridLayout
)
from PyQt5.QtCore import Qt
from backend import analyze
from grammar_parser import flatten_productions

class AnalysisViewer(QMainWindow):

    def __init__(self, grammar):
        super().__init__()
        self.steps = analyze(grammar)
        self.current_index = 0

        self.message_label = QLabel(f"Step {self.current_index + 1} of {len(self.steps) + 1}")
        self.title_label = QLabel(self.steps[0].title)
        self.description_label = QLabel(self.steps[0].description)
        self.description_scroll_area = QScrollArea()
        self.slider = QSlider(Qt.Horizontal)
        self.before_label = QLabel("Before")
        self.after_label = QLabel("After")
        self.previous_panel = GrammarPanel()
        self.previous_scroll_area = QScrollArea()
        self.current_panel = GrammarPanel()
        self.current_scroll_area = QScrollArea()
        self.before_after_grid_layout = QGridLayout()

        self.setup_connections()
        self.setup_layout()
        self.setWindowTitle("CFG to CNF Converter - Analysis")
        self.resize(600, 405)

    def setup_connections(self):
        self.slider.valueChanged.connect(self.navigate)

    def setup_layout(self):
        self.description_label.setAlignment(Qt.AlignCenter)
        self.slider.setRange(0, len(self.steps))
        self.slider.setSingleStep(1)
        self.previous_scroll_area.hide()
        self.current_panel.display_productions(self.steps[self.current_index].snapshot)
        self.before_label.hide()
        self.after_label.hide()
        self.previous_scroll_area.setWidget(self.previous_panel)
        self.current_scroll_area.setWidget(self.current_panel)
        self.description_scroll_area.setWidget(self.description_label)
        self.current_scroll_area.setWidgetResizable(True)
        self.previous_scroll_area.setWidgetResizable(True)
        self.description_scroll_area.setWidgetResizable(True)
        self.description_label.setWordWrap(True)

        self.before_after_grid_layout.addWidget(self.before_label, 0, 0, alignment=Qt.AlignCenter)
        self.before_after_grid_layout.addWidget(self.after_label, 0, 1, alignment=Qt.AlignCenter)
        self.before_after_grid_layout.addWidget(self.previous_scroll_area, 1, 0)
        self.before_after_grid_layout.addWidget(self.current_scroll_area, 1, 1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(self.before_after_grid_layout)
        main_layout.addWidget(self.description_scroll_area)
        main_layout.addWidget(self.slider)
        main_layout.addWidget(self.message_label, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _get_change_types(self):
        previous_step = self.steps[self.current_index - 1].snapshot
        previous_step = flatten_productions(previous_step)
        current_step = self.steps[self.current_index].snapshot
        current_step = flatten_productions(current_step)
        removed = previous_step - current_step
        added = current_step - previous_step
        return removed, added

    def navigate(self):
        self.current_index = self.slider.value()
        self.message_label.setText(f"Step {self.current_index + 1} of {len(self.steps) + 1}")
        self.display_step(self.current_index)

    def display_step(self, index):
        if index == 0:
            self.before_label.hide()
            self.after_label.hide()
            self.previous_scroll_area.hide()
            self.current_panel.display_productions(self.steps[self.current_index].snapshot)
            self.title_label.setText(self.steps[self.current_index].title)
            self.description_label.setText(self.steps[self.current_index].description)

        elif index == len(self.steps):
            self.before_label.hide()
            self.after_label.hide()
            self.previous_scroll_area.hide()
            self.current_panel.display_productions(self.steps[-1].snapshot)
            self.title_label.setText("CNF Result")
            self.description_label.setText(
                "With this, the conversion is complete.\n"
                "The grammar is now in Chomsky Normal Form."
            )

        else:
            self.before_label.show()
            self.after_label.show()
            self.previous_scroll_area.show()
            removed, added = self._get_change_types()
            self.previous_panel.display_productions(
                self.steps[self.current_index - 1].snapshot,
                removed, 
                "removed"
            )
            self.current_panel.display_productions(
                self.steps[self.current_index].snapshot,
                added,
                "added"
            )
            self.title_label.setText(self.steps[self.current_index].title)
            self.description_label.setText(self.steps[self.current_index].description)

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