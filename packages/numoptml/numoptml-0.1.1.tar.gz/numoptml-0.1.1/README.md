# numoptml

**numoptml** — это лёгкая и понятная Python-библиотека численных методов оптимизации, разработанная с нуля для образовательных, исследовательских и экспериментальных целей в области машинного обучения и автоматизации ИИ.

Она идеально подходит для студентов, инженеров и исследователей, которым важна прозрачность алгоритмов и контроль над процессом оптимизации.

## 🚀 Основные возможности

- Градиентный спуск (Gradient Descent)
- Метод Ньютона (Newton's Method)
- Поддержка подбора длины шага (Backtracking Line Search)
- Подходит для интеграции в AutoML, обучение моделей, RL-агентов

## 🔧 Установка

```bash
pip install numoptml
```

## 📌 Примеры использования

### Gradient Descent

```python
from numoptml.optimizers.gradient_descent import gradient_descent
import numpy as np

f = lambda x: (x[0] - 3)**2
grad = lambda x: np.array([2 * (x[0] - 3)])
x0 = [0.0]

res = gradient_descent(f, grad, x0, lr=0.1)
print(res)  # -> [3.]
```

### Newton's Method

```python
from numoptml.optimizers.newton_method import newton_method
import numpy as np

f = lambda x: (x[0] - 3)**2
grad = lambda x: np.array([2 * (x[0] - 3)])
hess = lambda x: np.array([[2]])
x0 = [0.0]

res = newton_method(f, grad, hess, x0)
print(res)  # -> [3.]
```

### Backtracking Line Search

```python
from numoptml.utils.line_search import backtracking_line_search
import numpy as np

f = lambda x: (x[0] - 3)**2
grad = lambda x: np.array([2 * (x[0] - 3)])
x = np.array([0.0])
direction = grad(x)

alpha = backtracking_line_search(f, grad, x, direction)
print(alpha)
```

## 🧠 Использование в ИИ

- Минимизация функции ошибки при обучении моделей
- AutoML: подбор гиперпараметров
- Оптимизация политик RL-агентов
- Edge AI: сжатие и оптимизация моделей
- Использование в MLOps пайплайнах

## 🗂 Структура проекта

- `optimizers/`: алгоритмы градиентного спуска и Ньютона
- `utils/`: утилиты (линейный поиск и т.д.)
- `examples/`: примеры
- `tests/`: автоматические тесты

## 📄 Лицензия

MIT — свободно используйте и модифицируйте.
