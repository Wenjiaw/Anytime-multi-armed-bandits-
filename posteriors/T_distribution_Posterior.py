import numpy as np
class T_Posterior():

    def __init__(self,alpha):
        self.alpha = alpha

    def sample_arm_i(self,reward):
        n = len(reward)
        if n == 1:
            T = reward[0]
        else:
            sigma = np.std(reward)
            mu = np.mean(reward)
            T = mu + np.random.standard_t(n+(2*self.alpha)-1)*sigma
        return T

    def mean(self, rewards):
        return np.mean(rewards)
