import numpy as np


class MLP:

    def __new__(cls, *args, **kwargs):

        inst = super().__new__(cls)
        for n in ['input', 'hidden', 'output', 'epoch', 'loss', 'rate']:
            setattr(inst, n, cls.__dict__[n])

        ws_szs = [inst.input] + inst.hidden + [inst.output]
        ws_pairs = list(zip(ws_szs[:-1], ws_szs[1:]))

        inst.f = cls.__dict__['f']
        inst.df = cls.__dict__['df']

        inst.ws = [np.random.randn(i, j) for i, j in reversed(ws_pairs)]
        inst.zs = [None] * len(inst.ws)

        return inst

    def __init__(self, X, y):
        self.fit(X, y)

    def fit(self, X, y):
        for _ in range(self.epoch):
            self.backward(X, y, self.predict(X))
            if np.mean(np.square(y - self.predict(X))) < self.loss:
                break
        return self

    def predict(self, X):
        vec, ln = X, len(self.zs)
        for i, w in enumerate(reversed(self.ws)):
            self.zs[ln - i - 1] = vec = self.f(vec @ w)
        return vec

    def backward(self, X, y, o):
        error = y - o
        delta = error * self.df(o)
        self.ws[0] += self.rate * self.zs[1].T @ delta
        for i, w in enumerate(self.ws[1:-1]):
            error = delta @ self.ws[i].T
            delta = error * self.df(self.zs[i+1])
            self.ws[i+1] += self.rate * self.zs[i+2].T @ delta
        error = delta @ self.ws[-2].T
        delta = error * self.df(self.zs[-1])
        self.ws[-1] += self.rate * X.T @ delta
