import numpy as np

class MultinomialPosterior():
    def __init__(self, alpha, c):
        self.alpha = alpha
        self.c = c

    def get_alpha_p(self, c, reward):
        count = np.zeros_like(c)
        for i in reward:
            count[c.index(i)] = count[c.index(i)] + 1
        alpha_p = count + self.alpha
        return alpha_p

    def sample_arm_i(self, reward):
        p_list = np.random.dirichlet(self.get_alpha_p(self.c, reward))
        return np.dot(p_list, self.c)

    def mean(self,rewards):
        if len(rewards) == 0:
            return np.random.choice(self.c)
        else:
            alpha_p = self.get_alpha_p(self.c, rewards)
            return np.dot(self.c, alpha_p) / sum(alpha_p)
