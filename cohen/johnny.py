import numpy as np
from PIL import Image, ImageDraw

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
    
    # Define uma nova janela de corte
    def set_window(self, x1, y1, x2, y2):
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
        print("Drawing line from ({}, {}) to ({}, {})".format(x1, y1, x2, y2))
        draw = ImageDraw.Draw(self.image)
        draw.line((x1, y1, x2, y2), fill=(255, 0, 0))
        print(self.cohen_sutherland((x1, y1), (x2, y2)))
        '''draw = ImageDraw.Draw(self.image)
        res = self.cohen_sutherland((x1, y1), (x2, y2))
        draw.line((x1, y1, x2, y2), fill=(255, 0, 0))
        xa, ya, xb, yb = res
        draw.line((xa, ya, xb,yb), fill=(255, 255, 255))'''

    def point_classify(self, x, y):
        print(x, y)
        c = 0b0000

        if x < self.xl:
            c |= 1
        elif x > self.xr:
            c |= 2

        if y < self.yb:
            c |= 4
        elif y > self.yt:
            c |= 8

        return c

    # O algoritmo de Cohen-Sutherland, propriamente dito.
    # Retorna o (x1, y1, x2, y2) da reta cortada com a janela de corte estabelecida,
    # ou False caso a reta esteja inteiramente fora da janela de corte.
    def cohen_sutherland(self, p1, p2):
        #print('xl {} yb {} xr {} yt {}'.format(self.xl, self.yb, self.xr, self.yt))
        # Classificando os pontos
        cod = [self.point_classify(*p1), self.point_classify(*p2)]
        if cod[0] == 0 and cod[1] == 0:
            return p1 + p2
        elif cod[0] & cod[1] != 0:
            return False
        codeA, codeB = cod
        # line needs clipping because at least
        # one of the points is outside the rectangle
        x = 1.0
        y = 1.0
        # we find which of the points is outside
        if codeA != 0:
            codeOut = codeA
        else:
            codeOut = codeB
            
        # now we find the intersection point using
        # some formulas
        if codeOut & TOP:
            # point is above the clip rectangle
            x = x1 + (x2 - x1) * (self.ymax - y1) / (y2 - y1)
            y = self.ymax
            
        elif codeOut & BOTTOM:
            # point is below the clip rectangle
            x = x1 + (x2 - x1) * (self.ymin - y1) / (y2 - y1)
            y = self.ymin
                
        elif codeOut & RIGHT:
            # point is to the right of the clip rectangle
            y = y1 + (y2 - y1) * (self.xmax - x1) / (x2 - x1)
            x = self.xmax
                
        elif codeOut & LEFT:
            # point is to the left of the clip rectangle
            y = y1 + (y2 - y1) * (self.xmin - x1) / (x2 - x1)
            x = self.xmin
                
        # now we replace point outside rectangle by
        # intersection point
        if codeOut == codeA:
            x1 = x
            y1 = y
            codeA = self.point_classify(x1, y1)
        else:
            x2 = x
            y2 = y
            codeB = self.point_classify(x2, y2)
        
    def show(self):
        self.image.show()

c = Cohen_Sutherland()
c.set_window(100, 100, 400, 400)
#c.draw_line(300, 450, 400, 20)
c.draw_line(110, 30, 50, 400)
c.show()