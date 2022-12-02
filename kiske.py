import numpy as np
from numba import njit
from PIL import Image

# Desenha uma reta de cor 'color' entre os pontos (x1, y1) e (x2, y2)
# Para linhas mais horizontais
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

a = np.zeros((200, 200), dtype=int)
draw_line(a, 0, 0, 20, 150, 255)
im = Image.fromarray(a)
#im.show()

# Para linhas mais verticais
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
draw_line2(a, 0, 0, 20, 150, 255)
im = Image.fromarray(a)
#im.show()

@njit
def draw_line_bresenham(img, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    inc_x = 1 if x1 < x2 else -1
    inc_y = 1 if y1 < y2 else -1
    d = dx - dy
    x = x1
    y = y1
    img[x, y] = color
    # Usando != porque pode crescer positiva ou negativamente
    while x != x2 or y != y2:
        aux = d << 1
        if aux > -dy:
            d = d - dy
            x += inc_x
        if aux < dx:
            d = d + dx
            y += inc_y
        img[x, y] = color

a = np.zeros((200, 200), dtype=int)
draw_line_bresenham(a, 0, 0, 20, 150, 255)
im = Image.fromarray(a)
im.show()
