import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# Grupo 'global' para que os RadioButtons possam se comunicar
class RadioButtons(QButtonGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setExclusive(True)
        self.buttonClicked.connect(self._on_button_clicked)

    def _on_button_clicked(self, button):
        for b in self.buttons():
            if b != button:
                b.setChecked(False)

# Class for a QDoubleSpinBox with a range from -1000.0 to 1000.0
class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(-1000.0, 1000.0)

class MainWindow(QMainWindow):
    def __init__(self, imgCasinha, parent=None):
        super().__init__()
        self.setWindowTitle("Transformações e Projeções")
        self.buttonGroup = RadioButtons()
        mainLayout = QHBoxLayout()
        self.casinhaLabel = QLabel()
        self.casinhaLabel.setPixmap(QPixmap(imgCasinha))
        menuLayout = QVBoxLayout()
        # Construindo escala
        menuLayout.addWidget(self.createScale())
        # Translação
        menuLayout.addWidget(self.createTranslate())
        # Rotação
        menuLayout.addWidget(self.createRotate())
        # Shearing
        menuLayout.addWidget(self.createShearing())
        buttonLayout = QHBoxLayout()
        # Botão de reset
        button = QPushButton('Reiniciar')
        button.clicked.connect(self.reset)
        buttonLayout.addWidget(button)
        # Botão de execução
        button = QPushButton('Executar')
        button.clicked.connect(self.execute)
        buttonLayout.addWidget(button)
        menuLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.casinhaLabel)
        mainLayout.addLayout(menuLayout)
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def createScale(self):
        scaleGroup = QGroupBox('Escala')
        scaleGrid = QGridLayout()
        scaleGlobal = QRadioButton('Global')
        scaleLocal = QRadioButton('Local')
        scaleLocal.setChecked(True)
        self.buttonGroup.addButton(scaleGlobal)
        self.buttonGroup.addButton(scaleLocal)
        scaleGrid.addWidget(scaleLocal, 1, 0)
        scaleGrid.addWidget(scaleGlobal, 2, 0)
        label = QLabel('X')
        label.setAlignment(Qt.AlignCenter)
        scaleGrid.addWidget(label, 0, 1)
        label = QLabel('Y')
        label.setAlignment(Qt.AlignCenter)
        scaleGrid.addWidget(label, 0, 2)
        label = QLabel('Z')
        label.setAlignment(Qt.AlignCenter)
        scaleGrid.addWidget(label, 0, 3)
        self.scaleG = DoubleSpinBox()
        self.scaleX = DoubleSpinBox()
        self.scaleY = DoubleSpinBox()
        self.scaleZ = DoubleSpinBox()
        self.scaleX.setValue(1)
        self.scaleY.setValue(1)
        self.scaleZ.setValue(1)
        scaleGrid.addWidget(self.scaleX, 1, 1)
        scaleGrid.addWidget(self.scaleY, 1, 2)
        scaleGrid.addWidget(self.scaleZ, 1, 3)
        scaleGrid.addWidget(self.scaleG, 2, 1)
        scaleGroup.setLayout(scaleGrid)
        return scaleGroup

    def createTranslate(self):
        translateGroup = QGroupBox('Translação')
        translateGrid = QGridLayout()
        translateRadio = QRadioButton()
        self.buttonGroup.addButton(translateRadio)
        translateGrid.addWidget(translateRadio, 1, 0)
        label = QLabel('X')
        label.setAlignment(Qt.AlignCenter)
        translateGrid.addWidget(label, 0, 1)
        label = QLabel('Y')
        label.setAlignment(Qt.AlignCenter)
        translateGrid.addWidget(label, 0, 2)
        label = QLabel('Z')
        label.setAlignment(Qt.AlignCenter)
        translateGrid.addWidget(label, 0, 3)
        self.translateX = DoubleSpinBox()
        self.translateY = DoubleSpinBox()
        self.translateZ = DoubleSpinBox()
        translateGrid.addWidget(self.translateX, 1, 1)
        translateGrid.addWidget(self.translateY, 1, 2)
        translateGrid.addWidget(self.translateZ, 1, 3)
        translateGroup.setLayout(translateGrid)
        return translateGroup

    def createRotate(self):
        rotateGroup = QGroupBox('Rotação')
        rotateGrid = QGridLayout()
        origemRadio = QRadioButton('Origem')
        self.buttonGroup.addButton(origemRadio)
        centroRadio = QRadioButton('Centro do objeto')
        self.buttonGroup.addButton(centroRadio)
        rotateGrid.addWidget(origemRadio, 0, 0)
        rotateGrid.addWidget(centroRadio, 1, 0)
        rotateGrid.addWidget(QLabel('Eixo'), 0, 1)
        rotateGrid.addWidget(QLabel('Graus'), 1, 1)
        self.origemEixo = QComboBox()
        self.origemEixo.addItems(['X', 'Y', 'Z'])
        self.centroGraus = DoubleSpinBox()
        rotateGrid.addWidget(self.origemEixo, 0, 2)
        rotateGrid.addWidget(self.centroGraus, 1, 2)
        rotateGroup.setLayout(rotateGrid)
        return rotateGroup

    def createShearing(self):
        shearingGroup = QGroupBox('Shearing')
        # Create input for a full 4x4 matrix
        shearingGrid = QGridLayout()
        shearingRadio = QRadioButton()
        self.buttonGroup.addButton(shearingRadio)
        shearingGrid.addWidget(shearingRadio, 0, 0)
        # Matriz para os inputs da matriz de transformação
        self.shearingInputs = [
            [DoubleSpinBox() for _ in range(4)] for _ in range(4)
        ]
        for i in range(4):
            self.shearingInputs[i][i].setValue(1)
            for j in range(4):
                shearingGrid.addWidget(self.shearingInputs[i][j], i, j+1)
        shearingGroup.setLayout(shearingGrid)
        return shearingGroup

    def execute(self):
        print('exe')

    def reset(self):
        print('res')