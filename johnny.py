import numpy as np
from numba import njit
from PIL import Image

# Cohen-Sutherland clipping algorithm

# define region codes as constants
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

# define diagonals points to define rectangle area
# of interest
xMax = 10.0
yMax = 8.0
xMin = 4.0
yMin = 4.0

# define function to compute region code to get
# a point(x,y)
def getPoint(x,y):
    code = INSIDE
    if x < xMin:
        code |= LEFT
    elif x > xMax:
        code |= RIGHT
    if y < yMin:
        code |= BOTTOM
    elif y > yMax:
        code |= TOP
    
    return code

def check_clip(x1, x2, y1, y2, flag):
    print('test')
    if flag:
        print('Line accepted from %.2f, %.2f to %.2f, %.2f' % (x1, y1, x2, y2))
    else:
        print('Line rejected - Completely outside the rectangle')

def clipping(x1, x2, y1, y2):
    # compute region codes for P1, P2
    codeA = getPoint(x1, y1)
    codeB = getPoint(x2, y2)
    isInside = False
    
    while True:
        # if both endpoints lie within rectangle
        if codeA == 0 and codeB == 0:
            isInside = True
            break
        
        # if both endpoints are outside rectangle
        elif (codeA & codeB) != 0:
            break
        
        # Some segment lies within the rectangle
        else:
            # line needs clipping because at least
            # one of the points is outside the rectangle
            x = 1.0
            y = 1.0
            # we find which of the points is outside
            if codeA != 0:
                codeOut = codeA
            else:
                codeOut = codeB
            
            # now we find the intersection point using
            # some formulas
            if codeOut & TOP:
                # point is above the clip rectangle
                x = x1 + (x2 - x1) * (yMax - y1) / (y2 - y1)
                y = yMax
            
            elif codeOut & BOTTOM:
                # point is below the clip rectangle
                x = x1 + (x2 - x1) * (yMin - y1) / (y2 - y1)
                y = yMin
                
            elif codeOut & RIGHT:
                # point is to the right of the clip rectangle
                y = y1 + (y2 - y1) * (xMax - x1) / (x2 - x1)
                x = xMax
                
            elif codeOut & LEFT:
                # point is to the left of the clip rectangle
                y = y1 + (y2 - y1) * (xMin - x1) / (x2 - x1)
                x = xMin
                
            # now we replace point outside rectangle by
            # intersection point
            if codeOut == codeA:
                x1 = x
                y1 = y
                codeA = getPoint(x1, y1)
            else:
                x2 = x
                y2 = y
                codeB = getPoint(x2, y2)
                
    if isInside:
        check_clip(x1, y1, x2, y2, True)
    else:
        check_clip(x1, y1, x2, y2, False)

def run():
    # define line points
    x1 = 5
    y1 = 7
    x2 = 5
    y2 = 7
    
    clipping(x1, x2, y1, y2)


run()