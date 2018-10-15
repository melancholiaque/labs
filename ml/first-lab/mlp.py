import numpy as np


X = np.array(([0, 0], [0, 1], [1, 0], [1, 1]), dtype=float)
y = np.array(([0], [0], [0], [1]), dtype=int)


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
        for _ in range(self.epoch):
            self.train(X, y)
            if self.loss_(X, y) < self.loss:
                break

    def forward(self, X):
        vec, ln = X, len(self.zs)
        for i, w in enumerate(reversed(self.ws)):
            self.zs[ln - i - 1] = vec = self.f(np.dot(vec, w))
        return vec

    def backward(self, X, y, o):
        error = y - o
        delta = error * self.df(o)
        self.ws[0] += self.rate * self.zs[1].T.dot(delta)
        for i, w in enumerate(self.ws[1:-1]):
            error = delta.dot(self.ws[i].T)
            delta = error * self.df(self.zs[i+1])
            self.ws[i+1] += self.rate * self.zs[i+2].T.dot(delta)
        error = delta.dot(self.ws[-2].T)
        delta = error * self.df(self.zs[-1])
        self.ws[-1] += self.rate * X.T.dot(delta)

    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    def loss_(self, X, y):
        return np.mean(np.square(y - self.forward(X)))


class mlp(MLP):

    rate = 0.1
    epoch = 100_000
    loss = 0.001

    f = lambda x: 1 / (1 + np.exp(-x))
    df = lambda x: x * (1 - x)

    input = 2
    hidden = [3]
    output = 1


my_little_pony = mlp(X, y)
print(my_little_pony.forward(X))
