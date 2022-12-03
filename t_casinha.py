import numpy as np

pontos = [
    [50, 150, 0, 1],
    [50, 150, 100, 1],
    [0, 100, 100, 1],
    [100, 100, 100, 1],
    [0, 100, 0, 1],
    [100, 100, 0, 1],
    [0, 0, 100, 1],
    [100, 0, 100, 1],
    [0, 0, 0, 1],
    [100, 0, 0, 1]
]

# Matriz de projeção paralela ortogonal (z = 0)
proj = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 1]
]

pontos = np.array(pontos)
proj = np.array(proj)

pontos_proj = pontos @ proj
print(pontos_proj)