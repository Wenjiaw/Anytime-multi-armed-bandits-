import numpy as np
class MultinomialPosterior():
    def __init__(self, alpha):
        self.alpha = alpha
    
    def sample_arm_i(self, reward):
        p_list = np.random.dirichlet(self.alpha)
        unique, counts = np.unique(reward, return_counts=True)
        if len(unique) == 0:#keep it because if the unique empty, p_list[index] will return error
            return 0
        else:
            a = 2 * unique # a can be the index of counts, avoidding the lengh of unique smaller than 3
            index = [int(i) for i in a]
            return np.dot(counts, p_list[index])



    def mean(self, rewards):
    
        unique, counts = np.unique(rewards, return_counts=True)
        return np.dot(counts,self.alpha[0:len(unique)])/sum(self.alpha)
