import numpy as np

def gradient_descent(func, grad, x0, lr=0.01, max_iter=100, tol=1e-6):
    x = np.array(x0, dtype=float)
    for _ in range(max_iter):
        g = grad(x)
        if np.linalg.norm(g) < tol:
            break
        x -= lr * g
    return x
