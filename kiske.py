import numpy as np
from numba import njit

# Desenha uma reta de cor 'color' entre os pontos (x1, y1) e (x2, y2)
@njit
def draw_line(img, c1, c2, color):
    print(c1, c2, color)