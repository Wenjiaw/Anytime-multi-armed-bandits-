# Karnin, Zohar Shay, Koren, Tomer, and Somekh, Oren. Almost optimal exploration in multi-armed bandits. In Proceedings of the International Conference on Machine Learning (ICML), pp. 1238–1246, 2013.
import numpy as np
class UCB:
    def __init__(self, bandit, m):
        self.bandit = bandit
        self.m = m
        self.reward_per_arm = [[] for i in range(len(self.bandit.arms))]
        self.mean_per_arm = np.full(len(self.bandit.arms), float(0))

    def upper(self, i,t):
        return (2*np.log(t - 1)/(len(self.reward_per_arm[i])))**0.5

    def biggest_upper(self, t):
        upper_array = [self.mean_per_arm[i] + self.upper(i,t) for i in range(len(self.bandit.arms))]
        index = np.where(upper_array == np.max(upper_array))[0]
        return int(index)

    def add_reward(self, arm_i, reward):
        self.reward_per_arm[arm_i].append(reward)
        self.mean_per_arm[arm_i] = np.mean(self.reward_per_arm[arm_i])

    def step(self, t):
        if t < len(self.bandit.arms) +1:
            reward = self.bandit.play(t-1)
            self.add_reward(t-1, reward)
        else:
            index = self.biggest_upper(t)
            reward = self.bandit.play(index)
            self.add_reward(index, reward)
        index = np.where(self.mean_per_arm == np.max(self.mean_per_arm))[0]
        self.Jt = [np.random.choice(index)]
        return self.Jt