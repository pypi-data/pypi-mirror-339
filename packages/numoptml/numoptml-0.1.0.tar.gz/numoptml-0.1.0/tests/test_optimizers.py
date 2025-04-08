from numoptml.optimizers.gradient_descent import gradient_descent
from numoptml.optimizers.newton_method import newton_method
import numpy as np

def test_gd_min():
    f = lambda x: (x[0] - 3)**2
    grad = lambda x: np.array([2 * (x[0] - 3)])
    x0 = [0.0]
    result = gradient_descent(f, grad, x0, lr=0.1)
    assert abs(result[0] - 3.0) < 1e-3

def test_newton_min():
    f = lambda x: (x[0] - 3)**2
    grad = lambda x: np.array([2 * (x[0] - 3)])
    hess = lambda x: np.array([[2]])
    x0 = [0.0]
    result = newton_method(f, grad, hess, x0)
    assert abs(result[0] - 3.0) < 1e-6
