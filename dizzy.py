import numpy as np
from numba import njit
from PIL import Image

@njit
def draw_circle(img, x1, y1, x2, y2, color):
    a = 100
    limite = 728

    while(a < limite):
        aReal = (a - 100) / 100
        x = round(50 * np.cos(aReal))
        y = round(50 * np.sin(aReal))
        img[x1 + x, y1 + y] = color
        a += 1

a = np.zeros((200, 200), dtype=int)
draw_circle(a, 50, 50, 50, 50, 255)
im = Image.fromarray(a)
im.show()

@njit
def draw_circle_bresenham(img, x1, y1, x2, y2, color):
    r = round(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    d = 1 - r
    x = 0
    y = r

    img[x1 + x, y1 + y] = color
    img[x1 + y, y1 + x] = color
    img[x1 - x, y1 + y] = color
    img[x1 - y, y1 + x] = color
    img[x1 + x, y1 - y] = color
    img[x1 + y, y1 - x] = color
    img[x1 - x, y1 - y] = color
    img[x1 - y, y1 - x] = color

    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

        img[x1 + x, y1 + y] = color
        img[x1 + y, y1 + x] = color
        img[x1 - x, y1 + y] = color
        img[x1 - y, y1 + x] = color
        img[x1 + x, y1 - y] = color
        img[x1 + y, y1 - x] = color
        img[x1 - x, y1 - y] = color
        img[x1 - y, y1 - x] = color

a = np.zeros((200, 200), dtype=int)
draw_circle_bresenham(a, 50, 50, 100, 100, 255)
im = Image.fromarray(a)
im.show()
