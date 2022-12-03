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

# In cartesian coordinates the x axis is on the bottom, but in image coordinates, the x axis is on the top
# So we need to flip the y coordinate
pontos = [[p[0], 150 - p[1], p[2]] for p in pontos]

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
    [0.5, 0.5, 0, 0],
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
    draw.line((pontos[line[0], 0], pontos[line[0], 1], pontos[line[1], 0], pontos[line[1], 1]), fill=(0, 0, 0))

img.save('t_casinha.png')

# Local scale matrix 10x 3y 4z
'''S = np.array([
    [10, 0, 0, 0],
    [0, 3, 0, 0],
    [0, 0, 4, 0],
    [0, 0, 0, 1]
])

# Applying scale
pontos = pontos @ S

# Reseting image
img = Image.new('RGB', (2000, 2000), (255, 255, 255))
draw = ImageDraw.Draw(img)

for line in lines:
    draw.line((pontos[line[0], 0], pontos[line[0], 1], pontos[line[1], 0], pontos[line[1], 1]), fill=(0, 0, 0))

img.save('t_casinha_scale.png')'''

# Global scale matrix 4 times
S = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 4]
])

# Applying scale
pontos = pontos @ S
pontos = np.round(pontos / S[3, 3])
print()
print(pontos)

# Reseting image
img = Image.new('RGB', (250, 250), (255, 255, 255))
draw = ImageDraw.Draw(img)

for line in lines:
    draw.line((pontos[line[0], 0], pontos[line[0], 1], pontos[line[1], 0], pontos[line[1], 1]), fill=(0, 0, 0))

draw.line((0, 0, 1000, 100), fill=(255, 0, 0))

img.save('t_casinha_scale.png')