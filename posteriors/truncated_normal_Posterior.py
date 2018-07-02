import numpy as np
from scipy import stats

class truncated_normal():
    def __init__(self, a, b, known_var):
        self.a = a
        self.b = b
        self.known_var = known_var

    def sample_arm_i(self,rewards):
        n = len(rewards)
        if n == 0:
            return stats.uniform.rvs(loc=self.a, scale=self.b)
        else:
            mu0 = np.mean(rewards)
            sigma0 = np.sqrt(known_var/n)
            return stats.truncnorm.rvs(self.a, self.b, loc=mu0, scale=sigma0)
