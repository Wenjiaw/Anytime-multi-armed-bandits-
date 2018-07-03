
import numpy as np
from scipy import stats

class truncated_normal():
    def __init__(self, a, b, var):
        self.a = a
        self.b = b
        self.know_var = var
    def sample_arm_i(self,reward):
        n = len(reward)
        if n == 0:
            return stats.uniform.rvs(loc=self.a, scale=self.b)
        else:
            mu0 = np.mean(reward)
            sigma0 = np.sqrt(self.know_var/n)
            a_norm = (self.a - mu0) / sigma0
            b_norm = (self.b - mu0) / sigma0
            return stats.truncnorm.rvs(a_norm, b_norm, loc=mu0, scale=sigma0)

    def mean(self, rewards):
        n = len(rewards)
        if n == 0:
            return (self.b - self.a) / 2.0
        else:
            mu0 = np.mean(rewards)
            sigma0 = np.sqrt(self.know_var / n)
            a_norm = (self.a - mu0) / sigma0
            b_norm = (self.b - mu0) / sigma0
            return stats.truncnorm.mean(a_norm, b_norm, loc=mu0, scale=sigma0)