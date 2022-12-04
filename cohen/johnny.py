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
            draw.line(res[:4], fill=(0, 255, 0))
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
        # compute region codes for P1, P2
        xMax, yMax, xMin, yMin = self.xl, self.yb, self.xr, self.yt
        codeA = self.point_classify(x1, y1)
        codeB = self.point_classify(x2, y2)
        
        while True:
            # if both endpoints lie within rectangle
            if codeA == 0 and codeB == 0:
                return (x1, y1, x2, y2, True)
            
            # if both endpoints are outside rectangle
            elif (codeA & codeB) != 0:
                return False

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
                x = x1 + (x2 - x1) * (yMax - y1) / (y2 - y1)
                y = yMax
                
            elif codeOut & BOTTOM:
                # point is below the clip rectangle
                x = x1 + (x2 - x1) * (yMin - y1) / (y2 - y1)
                y = yMin
                    
            elif codeOut & RIGHT:
                # point is to the right of the clip rectangle
                y = y1 + (y2 - y1) * (xMax - x1) / (x2 - x1)
                x = xMax
                    
            elif codeOut & LEFT:
                # point is to the left of the clip rectangle
                y = y1 + (y2 - y1) * (xMin - x1) / (x2 - x1)
                x = xMin
                    
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
    
    def clear(self):
        # Desativa o desenho de retas até que uma nova janela de corte seja definida
        self.active = False
        self.image.paste((13,117,172), [0, 0, self.image.size[0], self.image.size[1]])
        
    def to_QImage(self):
        return ImageQt.ImageQt(self.image)

