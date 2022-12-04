import sys
from jacko import LittleHouse
from window_littlehouse import MainWindow
from PySide6.QtWidgets import QApplication

casinha = LittleHouse()
app = QApplication(sys.argv)
window = MainWindow(casinha)
window.show()
sys.exit(app.exec())