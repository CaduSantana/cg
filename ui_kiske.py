# Qt draw line when drag and release

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from kiske import draw_line_bresenham
from PIL import Image, ImageQt
from numpy import array

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Retas e circunferências")
        # Building menuBar
        menubar = self.menuBar()
        arquivoMenu = menubar.addMenu("Arquivo")
        layout = QVBoxLayout()
        buttons = QHBoxLayout()
        canvas = Canvas()
        self.lineFormulaButton = QPushButton()
        self.lineBresenhamButton = QPushButton()
        self.circleParametricButton = QPushButton()
        self.circleBresenhamButton = QPushButton()
        buttons.addWidget(self.lineFormulaButton)
        buttons.addWidget(self.lineBresenhamButton)
        buttons.addWidget(self.circleParametricButton)
        buttons.addWidget(self.circleBresenhamButton)
        layout.addLayout(buttons)
        layout.addWidget(canvas)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

class Canvas(QLabel):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setFixedSize(300, 300)
        self.setMouseTracking(True)
        self.setScaledContents(True)
        self.image = Image.new("RGB", (300, 300), "black")
        self.color = (226, 135, 67)
        p = QPixmap(self.size())
        p.fill(Qt.black)
        self.setPixmap(p)
        self.start = QPoint()
        self.end = QPoint()
        self.isDrawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = QPoint(event.position().x(),event.position().y())
            self.isDrawing = True

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.isDrawing:
            self.end = QPoint(event.position().x(),event.position().y())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            a = array(self.image)
            draw_line_bresenham(a, self.start.y(), self.start.x(), self.end.y(), self.end.x(), self.color)
            self.image = Image.fromarray(a)
            self.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.image)))
            self.end = QPoint(event.position().x(),event.position().y())
            self.isDrawing = False
            self.update()


    def paintEvent(self, event):
        super(Canvas, self).paintEvent(event)
        if self.isDrawing:
            painter = QPainter(self)
            # * = unpacking de tuplas
            painter.setPen(QPen(QColor(*self.color), 1, Qt.SolidLine))
            painter.drawLine(self.start, self.end)

import sys
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())