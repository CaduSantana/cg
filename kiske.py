import numpy as np
from numba import njit
from PIL import Image

# Desenha uma reta de cor 'color' entre os pontos (x1, y1) e (x2, y2)
@njit
def draw_line(img, x1, y1, x2, y2, color): # Mais vertical
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

a = np.zeros((200, 200), dtype=int)
draw_line(a, 0, 0, 199, 199, 255)
im = Image.fromarray(a)
im.show()

# Forma alternativa (mais horizontal)
@njit
def draw_line2(img, x1, y1, x2, y2, color):
    m = (y2 - y1) / (x2 - x1)
    inc = -1
    if(x1 < x2):
        inc = 1
    x = x1
    y = y1
    while (x <= x2):
        img[x, y] = color
        x += inc
        y = int((x - x1) * (m + y1))

a = np.zeros((200, 200), dtype=int)
draw_line2(a, 0, 0, 199, 199, 255)
im = Image.fromarray(a)
im.show()

# Bresenham
@njit
def draw_line_bresenham(img, x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    inc = 1
    if(dy < 0):
        inc = -1
        dy = -dy
    d = 2 * dy - dx
    y = y1
    for x in range(x1, x2):
        img[x, y] = color
        if(d > 0):
            y += inc
            d -= 2 * dx
        d += 2 * dy

a = np.zeros((200, 200), dtype=int)
draw_line_bresenham(a, 0, 0, 199, 199, 255)
im = Image.fromarray(a)
im.show()
