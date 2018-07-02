import numpy as np
from scipy import stats

class truncated_normal():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def sample_arm_i(self,reward):
        n = len(reward)
        if n == 0:
            return stats.uniform.rvs(loc=self.a, scale=self.b)
        else:
            mu0 = np.mean(reward)
            sigma0 = np.var(reward)/n
            return stats.truncnorm.rvs(self.a, self.b, loc=mu0, scale=sigma0)
