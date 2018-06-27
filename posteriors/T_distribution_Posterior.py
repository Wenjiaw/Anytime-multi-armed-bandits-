import numpy as np
class T_Posterior():

    def sample_arm_i(reward):
        n = len(reward)
        if n == 1:
            T = reward[0]
        else:
            sigma = np.std(reward)
            mu = np.mean(reward)
            T = mu + np.random.standard_t(n-1)*sigma
        return T
