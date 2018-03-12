import numpy as np


class Value():
    def __init__(self, n):
        self.n = n


    def linearValue(self):
        reward = np.arange(self.n - 1, -1, -1)
        return reward * 0.9 / 999

    def polynomialValue(self):

        reward=np.arange([0.9*(1-((i+1)/self.n)**0.5) for i in range(self.n)])
        reward[0]=0.9
        return reward

    def sparseValue(self):
        reward=np.zeros(self.n)
        reward[1]=0.5
        return reward