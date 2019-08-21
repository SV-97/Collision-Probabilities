

def binom(n, k):
    c = 1.0
    for i in range(1, k+1):
        c *= float((n+1-i))/float(i)
    return c


def p(v, n):
    return sum((-1)**(k) * binom(n, k) / v**(n-(k)) for k in range(0, n))


def f(v): return 1/v**5 - 5/v**4 + 10/v**3 - 10/v**2 + 5/v


print(p(5, 5))
print(f(5))

""" neat plot styles

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.sin(x) + np.sin(np.sin(x))

def g(x):
    return np.sin(x+np.sin(x))

x = np.linspace(0, 2*np.pi, 500000)
x2 = np.linspace(0, 30, 500000)
f_1 = f(x)
f_2 = f(x2)
g_1 = g(x)
g_2 = g(x2)

for style in ["seaborn-darkgrid", "seaborn"]:
    plt.style.use(style)
    # plt.suptitle(r"$f(x) = \sin(x + sin(x))$")
    plt.subplot(1, 2, 1)
    plt.plot(x, f_1)
    plt.plot(x, g_1)

    plt.subplot(1, 2, 2)
    plt.plot(x2, f_2)
    plt.plot(x2, g_2)

    plt.show()
"""
"""
x1 = np.arange(-5, 300, 1)
x2 = np.linspace(x1[0], x1[-1], 50_000)
y1 = f(x1)
y2 = f(x2)

plt.subplot(1, 2, 1)
plt.plot(x1, y1, "x")
plt.subplot(1, 2, 2)
plt.plot(x2, y2)
plt.show()
"""
