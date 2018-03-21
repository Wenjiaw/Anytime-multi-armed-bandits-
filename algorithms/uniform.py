import numpy as np
import bottleneck
class Uniform:
    def __init__(self, bandit, m):
        self.bandit = bandit
        self.m = m
        self.counts_per_arm = np.full(len(bandit.arms), 0)
        self.mean_estimates = np.full(len(bandit.arms), float(0))


    def add_reward(self, arm_i, reward):
        self.counts_per_arm[arm_i] = self.counts_per_arm[arm_i]+1
        self.mean_estimates[arm_i] = self.mean_estimates[arm_i] +(reward-self.mean_estimates[arm_i])/(self.counts_per_arm[arm_i])

    def step(self, t):
        leastsampled = np.where(self.counts_per_arm == np.min(self.counts_per_arm))[0]
        arm_i = np.random.choice(leastsampled)
        reward = self.bandit.play(arm_i)
        self.add_reward(arm_i, reward)
        J_t = bottleneck.argpartition(-self.mean_estimates, self.m)[:self.m]
        return J_t













