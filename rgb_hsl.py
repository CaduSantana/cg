import numpy as np
from numba import njit

# Converte RGB para HSL
# Baseado nas equações: https://www.rapidtables.com/convert/color/rgb-to-hsl.html
@njit
def rgb_para_hsl(r, g, b):
    rr = r / 255.0
    gg = g / 255.0
    bb = b / 255.0
    cmax = max([ rr, gg, bb ])
    cmin = min([ rr, gg, bb ])
    ll = (cmax + cmin) / 2.0
    if (cmax == cmin):
        h = s = 0
    # Calcula H e S
    else:
        delta = cmax - cmin;
        # S está na escala de 0...1, converter p/ 240
        s = (delta / (1.0 - np.abs((2 * ll) - 1.0))) * 240
        if (cmax == rr):
            hh = ((gg - bb) / delta) + (6.0 if gg < bb else 0.0) # (gg < bb ? 6.0 : 0.0)
        elif (cmax == gg):
            hh = ((bb - rr) / delta) + 2.0
        elif (cmax == bb):
            hh = ((rr - gg) / delta) + 4.0

        if (hh < 0.0):
            hh += 360.0
        hh *= 60.0
        # 0 <= h < 360 => 0 <= h < 240
        hh = (hh * 2.0) / 3.0
        h = hh
    # Calcula L
    l = ll * 240.0

    return h, s, l

# Converte HSL para RGB.
# Baseado nesta abordagem: https://en.wikipedia.org/wiki/HSL_and_HSV ("HSL to RGB alternative")
@njit
def hsl_para_rgb(h, s, l):
    ll = l / 240.0
    # Imagem sem saturação (cinza)
    if (s == 0):
        r = g = b = np.round(ll * 255.0)
        return r, g, b

    hh = (h / 2.0) * 3.0
    ss = s / 240.0

    r = hsl_f(0, hh, ss, ll)
    g = hsl_f(8, hh, ss, ll)
    b = hsl_f(4, hh, ss, ll)

    return r, g, b

@njit
def hsl_f(n, h, s, l):
    k = np.fmod((n + (h / 30.0)), 12.0)
    return np.round((l - (s * min(l, 1.0 - l)) * max(-1.0, min([ k - 3.0, 9.0 - k, 1.0 ]))) * 255.0)