import numpy as np
class MultinomialPosterior():
    def __init__(self, variance, var0, mu0):
        self.known_var = variance
        self.var0 = var0
        self.mu0 = mu0

    def sample_arm_i(self, reward):
        if len(reward) == 0:
            return 0
        else:
            unique, counts = np.unique(reward, return_counts=True)
            p_list = np.random.dirichlet(counts)
            return np.dot(unique, p_list)

    def mean(self, rewards):
        if len(rewards) == 0:
            return 0
        else:
            unique, counts = np.unique(rewards, return_counts=True)
            return np.dot(unique,counts/len(rewards))