import numpy as np
class MultinomialPosterior():
    def __init__(self, alpha):
        self.alpha = alpha
    
    def get_alpha_p(self,c,reward):
        count = [0, 0, 0]
        for i in range(len(reward)):
            count[c.index(i)] = count[c.index(i)] + 1
        f = count / len(reward) 
        alpha_p = f + self.alpha
        return alpha_p
    
    def sample_arm_i(self, reward):
        c= [0,0.5,1]
        p_list = np.random.dirichlet(self.get_alpha_p(c,reward))
        return np.dot(p_list, c)

    def mean(self, rewards):
        c= [0,0.5,1]
        alpha_p = self.get_alpha_p(c,rewards)
        return np.dot(c,alpha_p)/sum(alpha_p)
