'''
    kiske - biblioteca para desenho de retas e círculos em matrizes quaisquer.
    Nomes das funções e variáveis em inglês para condizer com a linguagem Python.
    Autores:
        Carlos Eduardo Fernances de Santana
        Daniel Henrique Serezane Pereira
'''

import numpy as np
from numba import njit

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

# Desenha linhas com Breseham
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

# Checa se um determinado par calculado (x, y) está dentro da imagem img
# Útil par impedir círculos de "darem a volta" na imagem
@njit
def check_pair(img, x, y):
    return (x >= 0 and x < img.shape[0] and y >= 0 and y < img.shape[1])

# Desenha um círculo de centro (xc, yc) e raio r, com cor color, usando a equação paramétrica
@njit
def draw_circle_parametric(img, xc, yc, r, color):
    for a in range(0, 360):
        x = int(xc + r * np.cos(a))
        y = int(yc + r * np.sin(a))
        if check_pair(img, x, y):
            img[x, y] = color

# Desenha um círculo usando o algoritmo de Bresenham
@njit
def draw_circle_bresenham(img, xc, yc, r, color):
    x = 0
    y = r
    d = 3 - (r << 2)
    while x <= y:
        if check_pair(img, xc + x, yc + y):
            img[xc + x, yc + y] = color
        if check_pair(img, xc + y, yc + x):
            img[xc + y, yc + x] = color
        if check_pair(img, xc - x, yc + y):
            img[xc - x, yc + y] = color
        if check_pair(img, xc - y, yc + x):
            img[xc - y, yc + x] = color
        if check_pair(img, xc + x, yc - y):
            img[xc + x, yc - y] = color
        if check_pair(img, xc + y, yc - x):
            img[xc + y, yc - x] = color
        if check_pair(img, xc - x, yc - y):
            img[xc - x, yc - y] = color
        if check_pair(img, xc - y, yc - x):
            img[xc - y, yc - x] = color
        if d < 0:
            d += (x << 2) + 6
        else:
            d += ((x - y) << 2) + 10
            y -= 1
        x += 1