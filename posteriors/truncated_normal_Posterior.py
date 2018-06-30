import numpy as np
from scipy import stats

class truncated_normal():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def sample_arm_i(self,reward):
        n = len(reward)
        mu = np.mean(reward)
        var = np.var(reward)/n
        sigma = np.sqrt(var)
        if n == 1:
            a = self.a
            b = self.b
        else:
            a = (self.a - mu) / sigma
            b = (self.b - mu) / sigma
        result = stats.truncnorm.rvs(a, b, loc=mu, scale=sigma)
        return result


