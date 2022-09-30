import sys
import numpy as np
from numba import njit
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow, QGridLayout, QSpinBox

# Converte RGB para HSL
# Baseado nas equações: https://www.rapidtables.com/convert/color/rgb-to-hsl.html
@njit
def rgb_para_hsl(r, g, b):
    rr = r / 255.0
    gg = g / 255.0
    bb = b / 255.0
    cmax = max([ rr, gg, bb ])
    cmin = min([ rr, gg, bb ])
    ll = (cmax + cmin) / 2.0
    if (cmax == cmin):
        h = s = 0
    # Calcula H e S
    else:
        delta = cmax - cmin;
        # S está na escala de 0...1, converter p/ 240
        s = (delta / (1.0 - np.abs((2 * ll) - 1.0))) * 240
        if (cmax == rr):
            hh = ((gg - bb) / delta) + (6.0 if gg < bb else 0.0) # (gg < bb ? 6.0 : 0.0)
        elif (cmax == gg):
            hh = ((bb - rr) / delta) + 2.0
        elif (cmax == bb):
            hh = ((rr - gg) / delta) + 4.0

        if (hh < 0.0):
            hh += 360.0
        hh *= 60.0
        # 0 <= h < 360 => 0 <= h < 240
        hh = (hh * 2.0) / 3.0
        h = hh
    # Calcula L
    l = ll * 240.0

    return h, s, l

# Converte HSL para RGB.
# Baseado nesta abordagem: https://en.wikipedia.org/wiki/HSL_and_HSV ("HSL to RGB alternative")
@njit
def hsl_para_rgb(h, s, l):
    ll = l / 240.0
    # Imagem sem saturação (cinza)
    if (s == 0):
        r = g = b = np.round(ll * 255.0)
        return r, g, b

    hh = (h / 2.0) * 3.0
    ss = s / 240.0

    r = hsl_f(0, hh, ss, ll)
    g = hsl_f(8, hh, ss, ll)
    b = hsl_f(4, hh, ss, ll)

    return r, g, b

@njit
def hsl_f(n, h, s, l):
    k = np.fmod((n + (h / 30.0)), 12.0)
    return np.round((l - (s * min(l, 1.0 - l)) * max(-1.0, min([ k - 3.0, 9.0 - k, 1.0 ]))) * 255.0)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CG - Conversor RGB-HSL")
        centralWidget = QWidget()
        centralLayout = QVBoxLayout()
        valoresLayout = QGridLayout()
        # Criando as spinboxes
        self.__rs = QSpinBox()
        self.__rs.setRange(0, 255)
        self.__gs = QSpinBox()
        self.__gs.setRange(0, 255)
        self.__bs = QSpinBox()
        self.__bs.setRange(0, 255)
        self.__hs = QSpinBox()
        self.__hs.setRange(0, 239)
        self.__ss = QSpinBox()
        self.__ss.setRange(0, 240)
        self.__ls = QSpinBox()
        self.__ls.setRange(0, 240)
        self.__mostraCor = QWidget()
        self.__mostraCor.setAutoFillBackground(True)
        self.__mostraCor.setFixedSize(230, 20)
        self.__mostraCor.setPalette(QPalette(QColor(0, 0, 0)))
        valoresLayout.addWidget(QLabel('R'), 0, 0)
        valoresLayout.addWidget(self.__rs, 0, 1)
        valoresLayout.addWidget(QLabel('G'), 1, 0)
        valoresLayout.addWidget(self.__gs, 1, 1)
        valoresLayout.addWidget(QLabel('B'), 2, 0)
        valoresLayout.addWidget(self.__bs, 2, 1)
        valoresLayout.addWidget(QLabel('H'), 0, 2)
        valoresLayout.addWidget(self.__hs, 0, 3)
        valoresLayout.addWidget(QLabel('S'), 1, 2)
        valoresLayout.addWidget(self.__ss, 1, 3)
        valoresLayout.addWidget(QLabel('L'), 2, 2)
        valoresLayout.addWidget(self.__ls, 2, 3)
        botoesLayout = QHBoxLayout()
        self.__btn_rgb_para_hsl = QPushButton("Converter\nRGB para HSL")
        self.__btn_hsl_para_rgb = QPushButton("Converter\nHSL para RGB")
        botoesLayout.addWidget(self.__btn_rgb_para_hsl)
        botoesLayout.addWidget(self.__btn_hsl_para_rgb)
        centralLayout.addLayout(valoresLayout)
        centralLayout.addLayout(botoesLayout)
        centralLayout.addWidget(self.__mostraCor)
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()