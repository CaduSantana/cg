import numpy as np
from PIL import Image, ImageQt, ImageDraw

class LittleHouse:
    def __init__(self):
        # Definindo os dados iniciais da casinha
        # Dados da casinha, exatamente como dados no enunciado
        points = [
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
        # Nas coordenadas cartesianas, o eixo x está na parte inferior, mas nas coordenadas da imagem, o eixo x está na parte superior.
        # Portanto, precisamos inverter a coordenada y.
        points = [[p[0], 150 - p[1], p[2]] for p in points]
        self.og_points = np.array(points)
        # Transformando os pontos em coordenadas homogêneas
        self.og_points = np.hstack((self.og_points, np.ones((len(self.og_points), 1))))
        self.points = np.copy(self.og_points)
        self.lines = [
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

    def reset(self):
        self.points = np.copy(self.og_points)

    def local_scale(self, sx, sy, sz):
        # Matriz de escala local
        S = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
        self.points = self.points @ S

    def global_scale(self, s):
        S = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, s]
        ])
        self.points = (self.points @ S) / s

    def translate(self, tx, ty, tz):
        T = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [tx, ty, tz, 1]
        ])
        self.points = self.points @ T

    # Rotaciona em torno da origem, eixo x, y ou z
    def rotate(self, angle, axis):
        a = np.deg2rad(angle)
        if(axis == 'x'):
            R = np.array([
                [1, 0, 0, 0],
                [0, np.cos(a), -np.sin(a), 0],
                [0, np.sin(a), np.cos(a), 0],
                [0, 0, 0, 1]
            ])
        elif(axis == 'y'):
            R = np.array([
                [np.cos(a), 0, np.sin(a), 0],
                [0, 1, 0, 0],
                [-np.sin(a), 0, np.cos(a), 0],
                [0, 0, 0, 1]
            ])
        elif(axis == 'z'):
            R = np.array([
                [np.cos(a), -np.sin(a), 0, 0],
                [np.sin(a), np.cos(a), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
        self.points = self.points @ R
    
    # Rotaciona em torno do centro do objeto
    def rotate_center(self, angle, axis):
        center = np.mean(self.points, axis=0)
        self.translate(-center[0], -center[1], -center[2])
        self.rotate(angle, axis)
        self.translate(center[0], center[1], center[2])

    def shearing(self, S):
        self.points = self.points @ S

    def project(self):
        # Matriz de projeção cavaleira
        P = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0.5, 0.5, 0, 0],
            [0, 0, 0, 1]
        ])
        return self.points @ P

    def to_QImage(self):
        # Criando uma imagem em branco
        # TODO: 'adivinhar' tamanho, padding
        img = Image.new('RGB', (500, 500), (0, 0, 0))
        # Desenhando as linhas
        draw = ImageDraw.Draw(img)
        for line in self.lines:
            p = self.project()
            p = p / p[:, 3].reshape(-1, 1)
            p = p[:, :2]
            p = np.round(p).astype(int)
            draw.line((p[line[0]][0], p[line[0]][1], p[line[1]][0], p[line[1]][1]), fill=(0, 255, 0), width=1)
        return ImageQt.ImageQt(img)