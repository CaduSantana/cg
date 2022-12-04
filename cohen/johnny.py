import numpy as np
from PIL import Image, ImageDraw

INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

def getPoint(x,y, xMax, yMax, xMin, yMin):
    code = INSIDE
    if x < xMin:
        code |= LEFT
    elif x > xMax:
        code |= RIGHT
    if y < yMin:
        code |= BOTTOM
    elif y > yMax:
        code |= TOP
    
    return code

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
        res = self.cohen_sutherland(x1, y1, x2, y2)
        print(res)
        if res:
            draw.line(res[:4], fill=(0, 255, 0))
        '''draw = ImageDraw.Draw(self.image)
        res = self.cohen_sutherland((x1, y1), (x2, y2))
        draw.line((x1, y1, x2, y2), fill=(255, 0, 0))
        xa, ya, xb, yb = res
        draw.line((xa, ya, xb,yb), fill=(255, 255, 255))'''

    # O algoritmo de Cohen-Sutherland, propriamente dito.
    # Retorna o (x1, y1, x2, y2) da reta cortada com a janela de corte estabelecida,
    # ou False caso a reta esteja inteiramente fora da janela de corte.
    def cohen_sutherland(self, x1, y1, x2, y2):
        # compute region codes for P1, P2
        xMax, yMax, xMin, yMin = self.xl, self.yb, self.xr, self.yt
        codeA = getPoint(x1, y1, xMax, yMax, xMin, yMin)
        codeB = getPoint(x2, y2, xMax, yMax, xMin, yMin)
        isInside = False
        
        while True:
            # if both endpoints lie within rectangle
            if codeA == 0 and codeB == 0:
                isInside = True
                break
            
            # if both endpoints are outside rectangle
            elif (codeA & codeB) != 0:
                break
            
            # Some segment lies within the rectangle
            else:
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
                    codeA = getPoint(x1, y1, xMax, yMax, xMin, yMin)
                else:
                    x2 = x
                    y2 = y
                    codeB = getPoint(x2, y2, xMax, yMax, xMin, yMin)

        if isInside:
            return (x1, y1, x2, y2, True)
        else:
            return False
        
    def show(self):
        self.image.show()

c = Cohen_Sutherland()
c.set_window(100, 100, 400, 400)
c.draw_line(300, 450, 400, 20)
c.draw_line(110, 30, 50, 400)
c.draw_line(200, 450, 250, 60)
c.draw_line(240, 440, 110, 80)
c.draw_line(60, 320, 440, 240)
c.draw_line(440, 380, 90, 340)
c.show()