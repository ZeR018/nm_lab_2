import pandas as pd
import numpy as np
import sys

class main:
    def __init__(self, num_part):
        """
        Определение параметров и компонент стационарного уравнения теплоемкости
        """

        if num_part == 0:
             sys.exit()

        self.n = num_part
        self.node = self.n + 1
        self.start, self.end = 0, 1

        # точка разрыва
        self.ksi = 0.3
        self.mu = np.array([1, 0])
        self.kappa = np.array([0, 0])

        # для a
        self.k1 = lambda x: x**2 + 2
        self.k2 = lambda x: x**2

        # для d
        self.q1 = lambda x: x
        self.q2 = lambda x: x**2

        # для phi
        self.f1 = lambda x: 1
        self.f2 = lambda x: np.sin(np.pi*x)

    def numerical(self, k):
        """
        Построение численного решения v(xi)
        """

        # введем новые переменные
        self.phi = np.empty(k * self.n - 1, np.double)
        self.d = np.empty(k * self.n - 1, np.double)
        self.a = np.empty(k * self.n, np.double)

        # подсчет phi, d
        j = 1
        for i in range(k * self.n - 1):
            if self.ksi >= self.x2[i + 1]:
                self.phi[i] = self.f1(self.x[j])

                self.d[i] = self.q1(self.x[j])

            elif self.ksi <= self.x2[i]:
                self.phi[i] = self.f2(self.x[j])

                self.d[i] = self.q2(self.x[j])

            elif self.x2[i] < self.ksi < self.x2[i + 1]:
                self.phi[i] = (1 / self.h) * (
                        self.f1((self.x2[i] + self.ksi) / 2) * (self.ksi - self.x2[i]) + \
                        self.f2((self.ksi + self.x2[i + 1]) / 2) * (self.x2[i + 1] - self.ksi)
                )

                self.d[i] = (1 / self.h) * (
                        self.q1((self.x2[i] + self.ksi) / 2) * (self.ksi - self.x2[i]) + \
                        self.q2((self.ksi + self.x2[i + 1]) / 2) * (self.x2[i + 1] - self.ksi)
                )

            j += 1

        # подсчет a
        j = 1
        for i in range(k * self.n):
            if self.ksi >= self.x[j]:
                self.a[i] = self.k1(self.x2[i])

            elif self.ksi <= self.x[j - 1]:
                self.a[i] = self.k2(self.x2[i])

            elif self.x[j - 1] < self.ksi < self.x[j]:
                self.a[i] = 1 / ((1 / self.h) * (
                        ((self.ksi - self.x[i]) / (self.k1((self.x[i] + self.ksi) / 2))) + \
                        ((self.x[i + 1] - self.ksi) / (self.k2((self.ksi + self.x[i + 1]) / 2)))
                ))

            j += 1

        # нижняя диаг
        self.A = np.array([self.a[i] / (self.h ** 2) for i in range(k * self.n - 1)])
        # верхняя диаг
        self.B = np.array([self.a[i] / (self.h ** 2) for i in range(1, k * self.n)])
        # главная диаг
        self.C = np.array(
            [self.a[i] / (self.h ** 2) + self.a[i + 1] / (self.h ** 2) + self.d[i] for i in range(k * self.n - 1)])

        # найдем v
        return self.run_through(k)

    def calcdiag(self, k, k1):
        if k == 0:
            # главная диаг = 1 a1 ... an-1 1
            return np.concatenate(
                ([1], (-1) * np.array([self.a[i] / (self.h ** 2) + self.a[i + 1] / (self.h ** 2) + self.d[i] for i in
                                       range(k1 * self.n - 1)]), [1])
            )

        elif k == -1:
            # нижняя диаг = a1 ... an-1 -kappa2
            return np.concatenate(
                (np.array([self.a[i] / (self.h ** 2) for i in range(k1 * self.n - 1)]), [-self.kappa[1]])
            )
        else:
            # верхняя диаг = -kappa1 a2 ... an
            return np.concatenate(
                ([-self.kappa[0]], np.array([self.a[i] / (self.h ** 2) for i in range(1, k1 * self.n)]))
            )

    def direct(self, k):
        """
        Прямой ход прогонки
        """

        # находим параметры
        alpha = np.empty(k * self.n, np.double)
        beta = np.empty(k * self.n, np.double)

        # нач условие (3)
        alpha[0] = self.kappa[0]
        beta[0] = self.mu[0]

        # i = 1, n
        for i in range(k * self.n - 1):
            alpha[i + 1] = self.B[i] / (self.C[i] - self.A[i] * alpha[i])
            beta[i + 1] = (self.phi[i] + self.A[i] * beta[i]) / (self.C[i] - self.A[i] * alpha[i])

        return alpha, beta

    def reverse(self, k):
        """
        Обратный ход прогонки
        """

        # находим численное решение
        y = np.empty(k * self.n, np.double)

        # нач условие (6)
        y[-1] = (-self.kappa[1] * self.beta[-1] - self.mu[1]) / (self.kappa[1] * self.alpha[-1] - 1)

        # i = 0, n - 1
        for i in range(k * self.n - 2, -1, -1):
            y[i] = self.alpha[i + 1] * y[i + 1] + self.beta[i + 1]

        return y

    def run_through(self, k):
        """
        Метод прогонки
        """

        self.alpha, self.beta = self.direct(k)
        return self.reverse(k)

    def Solution(self):
        """
        Составление таблицы
        """

        # численные решения
        k = 1

        self.h = (self.end - self.start) / self.n
        self.x = [self.start + i * self.h for i in range(self.node)]
        self.x2 = [self.start + (i + 0.5) * self.h for i in range(self.node - 1)]
        self.v = np.concatenate(([self.mu[0]], self.numerical(k)))

        # численное решение с половинным шагом
        k = 2
        self.h /= 2
        self.x = [self.start + i * self.h for i in range(self.node * k)]
        self.x2 = [self.start + (i + 0.5) * self.h for i in range(self.node * k - 1)]
        self.v2 = np.concatenate(([self.mu[0]], self.numerical(k)))[::2]

        # разница численных решений
        self.dif = np.absolute(self.v - self.v2)
        self.x = self.x[::2]

        # таблица
        ndata = pd.DataFrame({
            '№ узла': np.arange(self.node), 'x': np.round(self.x, len(str(self.h))), 'v(x)': np.round(self.v, 14), \
            'v2(x2i)': np.round(self.v2, 14), '|v(x) - v2(x2i)|': np.round(self.dif, 14)
        })

        return ndata