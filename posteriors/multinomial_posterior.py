import numpy as np

class MultinomialPosterior():
    def __init__(self, alpha):
        self.alpha = alpha

    def get_alpha_p(self, c, reward):
        count = [0, 0, 0]
        for i in reward:
            count[c.index(i)] = count[c.index(i)] + 1
        f = [count[i] / len(reward) for i in range(len(count))]
        alpha_p = [(f[i] + self.alpha[i]) for i in range(len(count))]
        return alpha_p

    def sample_arm_i(self, reward):
        c = [0, 0.5, 1]
        p_list = np.random.dirichlet(self.get_alpha_p(c, reward))
        return np.dot(p_list, c)

    def mean(self, rewards):
        c = [0, 0.5, 1]
        if len(rewards) == 0:
            return np.random.choice(c)
        else:
            alpha_p = self.get_alpha_p(c, rewards)
            return np.dot(c, alpha_p) / sum(alpha_p)
