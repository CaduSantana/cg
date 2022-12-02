# Qt draw line when drag and release

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from kiske import draw_line, draw_line_bresenham, draw_circle_parametric, draw_circle_bresenham
from PIL import Image, ImageQt
from numpy import array

defaultSize = (300, 300)
opMap = [draw_line, draw_line_bresenham, draw_circle_parametric, draw_circle_bresenham]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Retas e circunferências")
        # Building menuBar
        menubar = self.menuBar()
        arquivoMenu = menubar.addMenu("Arquivo")
        abrirAction = QAction("Abrir", self)
        abrirAction.triggered.connect(self.open)
        arquivoMenu.addAction(abrirAction)
        arquivoMenu.addAction("Salvar")
        arquivoMenu.addAction("Sair")
        layout = QVBoxLayout()
        self.canvas = Canvas()
        # Adicionando as operações
        self.opbox = QComboBox()
        self.opbox.addItems(["Reta pela equação", "Reta por Bresenham", "Circunferência pela eq. paramétrica", "Circunferência por Bresenham"])
        self.opbox.currentIndexChanged.connect(self.canvas.setOp)
        layout.addWidget(self.opbox)
        layout.addWidget(self.canvas)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    def open(self):
        print("oi")
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Imagens (*.png *.jpg *.bmp)")
        if not filename:
            return
        image = Image.open(filename).resize(defaultSize)
        self.canvas.loadImage(image)

class Canvas(QLabel):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setFixedSize(*defaultSize)
        self.setMouseTracking(True)
        self.setScaledContents(True)
        self.image = Image.new("RGB", defaultSize, "black")
        self.color = (255, 0, 0)
        self.op = draw_line
        p = QPixmap(self.size())
        p.fill(Qt.black)
        self.setPixmap(p)
        self.start = QPoint()
        self.end = QPoint()
        self.isDrawing = False

    def setOp(self, index):
        self.op = opMap[index]
    
    def loadImage(self, image):
        self.image = image
        self.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.image)))

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
            y1, x1, y2, x2 = self.start.x(), self.start.y(), self.end.x(), self.end.y()
            if(self.op.__name__ == 'draw_line' or self.op.__name__ == 'draw_line_bresenham'):
                self.op(a, x1, y1, x2, y2, self.color)
            else:
                print("imrpime circulo")
                r = int(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
                self.op(a, x1, y1, r, self.color)
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
            if(self.op.__name__ == 'draw_line' or self.op.__name__ == 'draw_line_bresenham'):
                # Atenção: este drawLine é apenas um preview! O objeto de verdade é desenhado
                # no evento mouseReleaseEvent, pelo algoritmo selecionado
                painter.drawLine(self.start, self.end)
                return
            # Comprimento da reta = raio da circunferência
            r = int(((self.start.x() - self.end.x()) ** 2 + (self.start.y() - self.end.y()) ** 2) ** 0.5)
            painter.drawEllipse(self.start, r, r)

import sys
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())