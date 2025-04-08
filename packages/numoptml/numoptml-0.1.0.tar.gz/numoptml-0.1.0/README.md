# numoptml

Мини-библиотека численных методов оптимизации для машинного обучения.

## Установка

```bash
pip install .
```

## Пример использования

```python
from numoptml.optimizers.gradient_descent import gradient_descent

f = lambda x: (x[0] - 3)**2
grad = lambda x: np.array([2 * (x[0] - 3)])
x0 = [0.0]
result = gradient_descent(f, grad, x0)
print(result)
```
