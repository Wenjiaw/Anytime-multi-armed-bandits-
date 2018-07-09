import numpy as np
class MultinomialPosterior():
    def __init__(self, alpha):
        self.alpha = alpha
    
    def sample_arm_i(self, reward):
        p_list = np.random.dirichlet(self.alpha)
        unique, counts = np.unique(reward, return_counts=True)
        a = 2 * unique
        index = [int(i) for i in a]
        if len(unique) == 0:
            return 0
        else:
            return np.dot(counts, p_list[index])



    def mean(self, rewards):
    
        unique, counts = np.unique(rewards, return_counts=True)
        return np.dot(counts,self.alpha[0:len(unique)])/sum(self.alpha)
