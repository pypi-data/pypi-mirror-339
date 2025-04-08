def backtracking_line_search(f, grad, x, direction, alpha=1.0, rho=0.5, c=1e-4):
    while f(x - alpha * direction) > f(x) - c * alpha * grad(x).dot(direction):
        alpha *= rho
    return alpha
