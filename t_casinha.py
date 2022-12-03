import numpy as np
from PIL import Image, ImageDraw

# Pontos da casinha, exatamente como dados no enunciado
pontos = [
    [50, 150, 0],
    [50, 150, 100],
    [0, 100, 0],
    [0, 0, 0],
    [100, 0, 0],
    [100, 0, 100],
    [0, 0, 100],
    [100, 100, 0],
    [0, 100, 100],
    [100, 100, 100]
]

# Points if it was a image, not cartesian
'''pontos = [
    [50, 0, 0],
    [50, 0, 100],
    [0, 100, 0],
    [0, 200, 0],
    [100, 200, 0],
    [100, 200, 100],
    [0, 200, 100],
    [100, 100, 0],
    [0, 100, 100],
    [100, 100, 100]
]'''

# Flip the x axis
#pontos = [[-p[0], 150 - p[1], 100 - p[2]] for p in pontos]

# Flip the points in pontos vertically
#pontos = np.array(pontos)
#pontos[:, 1] = 150 - pontos[:, 1]

lines = [
    [0, 1],
    [0, 2],
    [0, 7],
    [1, 8],
    [1, 9],
    [2, 3],
    [2, 8],
    [3, 4],
    [3, 6],
    [4, 5],
    [4, 7],
    [5, 6],
    [5, 9],
    [6, 8],
    [7, 9]
]

# Parallel projection matrix, z = 0
'''P = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 1]
])'''

# Matriz de projeção cavaleira
P = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0.7, 0.7, 0, 0],
    [0, 0, 0, 1]
])

# Transformig points to homogeneous coordinates
pontos = np.array(pontos)
pontos = np.hstack((pontos, np.ones((len(pontos), 1))))
print(pontos)

# Applying projection
pontos = pontos @ P

# Normalizing points
#pontos = pontos[:, :2] / pontos[:, 2:]

# Drawing
img = Image.new('RGB', (250, 250), (255, 255, 255))
draw = ImageDraw.Draw(img)

for line in lines:
    x1, y1 = pontos[line[0], :2]
    x2, y2 = pontos[line[1], :2]
    draw.line((y1, x1, y2, x2), fill=(0, 0, 0), width=1)

img.save('t_casinha.png')