import numpy as np
from PIL import Image, ImageDraw, ImageQt

INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

class Cohen_Sutherland:
    def __init__(self):
        self.image = Image.new('RGB', (500, 500), (13,117,172))
        # Inicializando as variáveis da janela
        self.xl = 0
        self.xr = 0
        self.yb = 0
        self.yt = 0
        self.active = False
    
    # Define uma nova janela de corte
    def set_window(self, x1, y1, x2, y2):
        self.active = True
        #print("Setting window to ({}, {}) to ({}, {})".format(x1, y1, x2, y2))
        # Lembrando que aqui, com y cresce para baixo, o yb é o maior y
        self.xl = max(x1, x2)
        self.xr = min(x1, x2)
        self.yb = max(y1, y2)
        self.yt = min(y1, y2)
        print("Window set to ({}, {}) to ({}, {})".format(self.xl, self.yb, self.xr, self.yt))
        # Desenha a janela na tela
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((x1, y1, x2, y2), fill=(0, 0, 0))

    # Desenha uma reta entre (x1, y1) e (x2, y2), cortando-a com a janela de corte
    def draw_line(self, x1, y1, x2, y2):
        if not self.active:
            return
        print("Drawing line from ({}, {}) to ({}, {})".format(x1, y1, x2, y2))
        draw = ImageDraw.Draw(self.image)
        #draw.line((x1, y1, x2, y2), fill=(255, 0, 0))
        res = self.cohen_sutherland(x1, y1, x2, y2)
        print(res)
        if res:
            draw.line(res, fill=(0, 255, 0))
        '''draw = ImageDraw.Draw(self.image)
        res = self.cohen_sutherland((x1, y1), (x2, y2))
        draw.line((x1, y1, x2, y2), fill=(255, 0, 0))
        xa, ya, xb, yb = res
        draw.line((xa, ya, xb,yb), fill=(255, 255, 255))'''

    def point_classify(self, x,y):
        code = INSIDE
        if x < self.xr:
            code |= LEFT
        elif x > self.xl:
            code |= RIGHT
        if y < self.yt:
            code |= BOTTOM
        elif y > self.yb:
            code |= TOP
        
        return code

    # O algoritmo de Cohen-Sutherland, propriamente dito.
    # Retorna o (x1, y1, x2, y2) da reta cortada com a janela de corte estabelecida,
    # ou False caso a reta esteja inteiramente fora da janela de corte.
    def cohen_sutherland(self, x1, y1, x2, y2):
        cod1, cod2 = self.point_classify(x1, y1), self.point_classify(x2, y2)
        # Uma abordagem para o algoritmo de Cohen-Sutherland
        # que usa um loop para ajustar os (x, y) de cada ponto até
        # que ambos estejam dentro da janela de corte.
        # O algoritmo vai, no máximo, precisar ajustar 4 pontos.
        while True:
            # Quando ambos estiverem na janela de corte após os ajustes,
            # ou se naturalmente já estiverem.
            if cod1 == 0 and cod2 == 0:
                return (x1, y1, x2, y2)
            # Se ambos estiverem fora da janela de corte
            elif (cod1 & cod2) != 0:
                return False
            # Se ainda precisarem de ajustes, usamos as fórmulas
            x, y = None, None
            # Tratamos apenas os pontos que precisam de ajuste
            # (conseguimos saber se precisa ou não pelo código)
            cod_tr = cod1 if cod1 != 0 else cod2
            # Fazendo direto ao invés de calcular m para evitar divisão por zero
            # Cima
            if cod_tr & TOP:
                x = x1 + (x2 - x1) * (self.yb - y1) / (y2 - y1)
                y = self.yb
            # Baixo
            elif cod_tr & BOTTOM:
                x = x1 + (x2 - x1) * (self.yt - y1) / (y2 - y1)
                y = self.yt
            # Direita
            elif cod_tr & RIGHT:
                x = self.xl
                y = y1 + (y2 - y1) * (self.xl - x1) / (x2 - x1)   
            # Esquerda 
            elif cod_tr & LEFT:
                x = self.xr
                y = y1 + (y2 - y1) * (self.xr - x1) / (x2 - x1)
            # Atualiza o código do ponto que precisava de ajuste
            if cod_tr == cod1:
                x1 = x
                y1 = y
                cod1 = self.point_classify(x1, y1)
                continue
            x2 = x
            y2 = y
            cod2 = self.point_classify(x2, y2)
    
    def clear(self):
        # Desativa o desenho de retas até que uma nova janela de corte seja definida
        self.active = False
        self.image.paste((13,117,172), [0, 0, self.image.size[0], self.image.size[1]])
        
    def to_QImage(self):
        return ImageQt.ImageQt(self.image)

