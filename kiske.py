import numpy as np
from numba import njit
from PIL import Image

# Desenha uma reta de cor 'color' entre os pontos (x1, y1) e (x2, y2)
@njit
def draw_line(img, x1, y1, x2, y2, color):
    m = (y2 - y1) / (x2 - x1)
    inc = -1
    if(x1 < x2):
        inc = 1
    x = x1
    y = y1
    while (x <= x2):
        img[x, y] = color
        x += inc
        y = int((m *(x - x1)) + y1)
    return img

a = np.zeros((200, 200), dtype=int)
draw_line(a, 0, 0, 199, 199, 255)
im = Image.fromarray(a)
im.show()