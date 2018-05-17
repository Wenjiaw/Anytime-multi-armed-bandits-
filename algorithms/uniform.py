import numpy as np
import bottleneck
class Uniform:
    def __init__(self, bandit, m):
        self.bandit = bandit
        self.m = m
        #same remarks as for the at-lucb
        self.reward_perarm = [[] for i in range(len(self.bandit.arms))]
        self.mean_estimates = np.full(len(bandit.arms), float(0))

    def add_reward(self, arm_i, reward):
        self.reward_perarm[arm_i].append(reward)
        self.mean_estimates[arm_i] = np.mean(self.reward_perarm[arm_i])

    #refactor least_sampled_index
    def leastsample_index(self):
        counts_per_arm = #just take the lenghts of rewards_per_arm ?
        least_sampled = np.where(counts_per_arm == np.min(counts_per_arm))[0]
        
        return leastsampled

    def step(self, t):
        least_sampled = self.leastsample_index()
        arm_i = np.random.choice(least_sampled)
        
        reward = self.bandit.play(arm_i)
        self.add_reward(arm_i, reward)
        
        J_t = bottleneck.argpartition(-self.mean_estimates, self.m)[:self.m]
        return J_t













