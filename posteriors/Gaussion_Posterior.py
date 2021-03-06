import numpy as np
class GaussianPosterior():
    def __init__(self, variance, var0, mu0):
        self.known_var = variance
        self.var0 = var0
        self.mu0 = mu0

    def sample_arm_i(self, reward):
        n = len(reward)
        denom = (1.0 / self.var0 + n / self.known_var)
        u = (self.mu0 / self.var0 + sum(reward) / self.known_var) / denom
        var = 1.0 / denom
        stddev = np.sqrt(var)
        return np.random.normal(u, stddev)

    def mean(self, rewards):
        return np.mean(rewards)

