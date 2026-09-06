from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

app = QApplication([])
app.setWindowIcon(QIcon("assets/icon.ico"))
window = MainWindow()
window.show()
app.exec_()