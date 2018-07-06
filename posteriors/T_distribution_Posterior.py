import numpy as np
class T_Posterior():
    def __init__(self,alpha):
        self.alpha = alpha

    def freedom(n):
        n+(2*self.alpha)-1

    def sample_arm_i(self,reward):
        n = len(reward)
        freedom = self.freedom(n)
        sigma = np.sqrt(np.var(reward)/freedom)
        mu = np.mean(reward)
        sample = np.random.standard_t(freedom)
        return mu + sample*sigma

    def mean(self, rewards):
        return np.mean(rewards)
