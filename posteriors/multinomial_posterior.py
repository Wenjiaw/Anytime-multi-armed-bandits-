import numpy as np
class MultinomialPosterior():
    def __init__(self, alpha):
        self.alpha = alpha

    def sample_arm_i(self, reward):

        unique, counts = np.unique(reward, return_counts=True)
        p_list = np.random.dirichlet(self.alpha)
        return np.dot(counts, p_list)


    def mean(self, rewards):

        unique, counts = np.unique(rewards, return_counts=True)
        return np.dot(count,self.alpha)/sum(self.alpha)
