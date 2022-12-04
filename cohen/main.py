from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from johnny import Cohen_Sutherland

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cohen-Sutherland")
        self.setWindowIcon(QIcon("icons/johnny.ico"))

        mainLayout = QVBoxLayout()
        self.label = QLabel("Para começar, desenhe uma janela.")
        self.canvas = Canvas(self)
        self.clearButton = QPushButton("Limpar")
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.canvas)
        mainLayout.addWidget(self.clearButton)
        self.clearButton.clicked.connect(self.clear)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def clear(self):
        self.label.setText("Para começar, desenhe uma janela.")
        self.canvas.clear()

class Canvas(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.cs = Cohen_Sutherland()
        self.setFixedSize(500, 500)
        self.setMouseTracking(True)
        self.setPixmap(QPixmap.fromImage(self.cs.to_QImage()))
        # Variáveis pra desenho
        self.start = QPoint()
        self.end = QPoint()
        self.isDrawing = False
        self.windowColor = (255, 255, 255)
        self.lineColor = (255, 0, 0)
        self.isDrawingWindow = True

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
            self.end = QPoint(event.position().x(),event.position().y())
            self.isDrawing = False
            # Desenhou a janela de corte
            if self.isDrawingWindow:
                self.cs.set_window(self.start.x(), self.start.y(), self.end.x(), self.end.y())
                self.isDrawingWindow = False
                self.parent.label.setText("Agora, desenhe as retas.")
            else:
                self.cs.draw_line(self.start.x(), self.start.y(), self.end.x(), self.end.y())
            self.setPixmap(QPixmap.fromImage(self.cs.to_QImage()))
            self.update()

    def paintEvent(self, event):
        super(Canvas, self).paintEvent(event)
        if self.isDrawing:
            painter = QPainter(self)
            if self.isDrawingWindow:
                painter.setPen(QPen(QColor(*self.windowColor), 1, Qt.SolidLine))
                painter.setBrush(QBrush(QColor(*self.windowColor), Qt.SolidPattern))
                painter.drawPoint(self.start.x(), self.start.y())
                painter.drawPoint(self.start.x(), self.end.y())
                painter.drawPoint(self.end.x(), self.start.y())
                painter.drawPoint(self.end.x(), self.end.y())
                painter.drawRect(self.start.x(), self.start.y(), self.end.x() - self.start.x(), self.end.y() - self.start.y())
                return
            painter.setPen(QPen(QColor(*self.lineColor), 1, Qt.SolidLine))
            painter.drawLine(self.start, self.end)

    def clear(self):
        self.cs.clear()
        self.isDrawingWindow = True
        self.setPixmap(QPixmap.fromImage(self.cs.to_QImage()))
        self.update()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()