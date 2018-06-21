import numpy as np
class GaussianPosterior():
    def __init__(self, variance):
        self.known_var = variance

    def sample_arm_i(self,reward):
        n = len(reward)
        if n == 1:
            stddev =  np.sqrt(self.known_var)
            return np.random.normal(reward[0],stddev)
        else:
            var0 = np.var(reward)
            u0 = np.mean(reward)
            denom = (1.0 / var0 + n / self.known_var)
            u = (u0 / var0 + sum(reward) / self.known_var) / denom
            var = 1.0 / denom
            stddev = np.sqrt(var)
            return np.random.normal(u,stddev)

    # def mean(self, posterior_per_arm):
    #     mean = np.zeros(len(posterior_per_arm))
    #     for i in range(len(posterior_per_arm)):
    #         if len(posterior_per_arm[i]) == 0:
    #             pass
    #         else:
    #             mean[i] = np.mean(posterior_per_arm[i])
    #     return mean
