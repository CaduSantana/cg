# Qt draw line when drag and release

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from kiske import draw_line, draw_line_bresenham
from PIL import Image, ImageQt
from numpy import array

defaultSize = (300, 300)

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
        buttons = QHBoxLayout()
        self.canvas = Canvas()
        self.lineFormulaButton = QPushButton()
        self.lineBresenhamButton = QPushButton()
        self.circleParametricButton = QPushButton()
        self.circleBresenhamButton = QPushButton()
        buttons.addWidget(self.lineFormulaButton)
        buttons.addWidget(self.lineBresenhamButton)
        buttons.addWidget(self.circleParametricButton)
        buttons.addWidget(self.circleBresenhamButton)
        layout.addLayout(buttons)
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
        p = QPixmap(self.size())
        p.fill(Qt.black)
        self.setPixmap(p)
        self.start = QPoint()
        self.end = QPoint()
        self.isDrawing = False
    
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
            x1, y1, x2, y2 = self.start.x(), self.start.y(), self.end.x(), self.end.y()
            # Limita as linhas para a imagem
            # Lembrando que essa limitação é um corte simples. Para uma aproximação da reta,
            # seria necessário aplicar algum algoritmo de corte de retas.
            x1, y1, x2, y2 = min(299, max(0, x1)), min(299, max(0, y1)), min(299, max(0, x2)), min(299, max(0, y2))
            draw_line(a, y1, x1, y2, x2, self.color)
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
            # Atenção: este drawLine é apenas um preview! O objeto de verdade é desenhado
            # no evento mouseReleaseEvent, pelo algoritmo selecionado
            painter.drawLine(self.start, self.end)

import sys
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())