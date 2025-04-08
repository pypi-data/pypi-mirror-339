import numpy as np

def newton_method(func, grad, hess, x0, max_iter=50, tol=1e-6):
    x = np.array(x0, dtype=float)
    for _ in range(max_iter):
        g = grad(x)
        H = hess(x)
        if np.linalg.norm(g) < tol:
            break
        dx = np.linalg.solve(H, g)
        x -= dx
    return x
