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
    while (y <= y2):
        img[x, y] = color
        y += inc
        x = int((y - y1) / (m + x1))

        # pixel wise
@njit
def draw_line_p(img, x1, y1, x2, y2, color):
    m = (y2 - y1) / (x2 - x1)
    inc = -1
    if(x1 == x2):
        if(y1 < y2):
            for y in range(y1, y2):
                img[x1, y] = color
        else:
            for y in range(y2, y1):
                img[x1, y] = color
    else:
        if(x1 < x2):
            for x in range(x1, x2):
                img[x, int((m *(x - x1)) + y1)] = color
        else:
            for x in range(x2, x1):
                img[x, int((m *(x - x1)) + y1)] = color
a = np.zeros((200, 200), dtype=int)
draw_line(a, 0, 0, 199, 199, 255)
im = Image.fromarray(a)
im.show()
