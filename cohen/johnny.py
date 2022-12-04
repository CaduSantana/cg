import numpy as np
from PIL import Image, ImageDraw

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
        # Desenha a janela na tela
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((x1, y1, x2, y2), fill=(0, 0, 0))

    # Desenha uma reta entre (x1, y1) e (x2, y2), cortando-a com a janela de corte
    def draw_line(self, x1, y1, x2, y2):
        draw = ImageDraw.Draw(self.image)
        draw.line((x1, y1, x2, y2), fill=(255, 0, 0))
        res = self.cohen_sutherland((x1, y1), (x2, y2))
        if res:
            draw.line(res[:4], fill=(0, 255, 0))

    def point_classify(self, x,y):
        c = 0

        if x < self.xr:
            c |= 1
        elif x > self.xl:
            c |= 2
        
        if y < self.yt:
            c |= 4
        elif y > self.yb:
            c |= 8
        
        return c

    # O algoritmo de Cohen-Sutherland, propriamente dito.
    # Retorna o (x1, y1, x2, y2) da reta cortada com a janela de corte estabelecida,
    # ou False caso a reta esteja inteiramente fora da janela de corte.
    def cohen_sutherland(self, p1, p2):
        p = [{'x': p1[0], 'y': p1[1]}, {'x': p2[0], 'y': p2[1]}]
        cod = [self.point_classify(p[i]['x'], p[i]['y']) for i in range(2)]
        # Uma abordagem para o algoritmo de Cohen-Sutherland
        # que usa um loop para ajustar os (x, y) de cada ponto até
        # que ambos estejam dentro da janela de corte.
        # O algoritmo vai, no máximo, precisar ajustar 4 pontos.
        for _ in range(4):
            # Quando ambos estiverem na janela de corte
            # (ou se naturalmente já estiverem)
            if cod[0] == 0 and cod[1] == 0:
                return (p[0]['x'], p[0]['y'], p[1]['x'], p[1]['y'], True)
            # Se ambos estiverem fora da janela de corte
            elif (cod[0] & cod[1]) != 0:
                return False
            # Se ainda precisarem de ajustes, usamos as fórmulas
            x, y = (None, None)
            # Tratamos apenas os pontos que precisam de ajuste
            # Salvamos o índice do código do ponto que precisa de ajuste
            i_adj = 0 if cod[0] != 0 else 1
            m = (p[1]['y'] - p[0]['y']) / (p[1]['x'] - p[0]['x'])
            # Cima
            if cod[i_adj] & 8:
                x = p[i_adj]['x'] + (self.yb - p[i_adj]['y']) / m
                y = self.yb
            # Baixo
            elif cod[i_adj] & 4:
                x = p[i_adj]['x'] + (self.yt - p[i_adj]['y']) / m
                y = self.yt
            # Direita
            elif cod[i_adj] & 2:
                y = p[i_adj]['y'] + m * (self.xl - p[i_adj]['x'])
                x = self.xl
            # Esquerda
            elif cod[i_adj] & 1:
                y = p[i_adj]['y'] + m * (self.xr - p[i_adj]['x'])
                x = self.xr   
            # Atualiza o código do ponto que precisava de ajuste
            p[i_adj]['x'] = x
            p[i_adj]['y'] = y
            cod[i_adj] = self.point_classify(p[0]['x'], p[0]['y'])

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