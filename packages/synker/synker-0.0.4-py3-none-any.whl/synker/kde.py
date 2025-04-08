import numpy as np

def kde(x, y, xi=None, yi=None, hx=None, hy=None, res=100):
    
    n = len(x)
    
    if xi is None:
        xi = np.linspace(min(x), max(x), res)
    if yi is None:
        yi = np.linspace(min(y), max(y), res)

    p = np.zeros((len(xi), len(yi)))

    for i in range(n):
        p1 = np.exp(-((x[i] - xi) ** 2) / (2 * hx ** 2))
        p2 = np.exp(-((y[i] - yi) ** 2) / (2 * hy ** 2))
        p += (1 / (n * hx * hy)) * p1[:, np.newaxis] * p2[np.newaxis, :]

    return p