import numpy as np
class Uniform:
    def __init__(self, bandit, m):
        self.bandit = bandit
        self.m = m
        self.reward_per_arm = [[] for i in range(len(self.bandit.arms))]
        self.mean_per_arm = np.full(len(bandit.arms), float(0))

    def add_reward(self, arm_i, reward):
        self.reward_per_arm[arm_i].append(reward)
        self.mean_per_arm[arm_i] = np.mean(self.reward_per_arm[arm_i])

    def least_sample_index(self):
        counts_per_arm = [len(self.reward_per_arm[i]) for i in range(len(self.bandit.arms))]#just take the lenghts of rewards_per_arm ?
        least_sampled_index = np.where(counts_per_arm == np.min(counts_per_arm))[0]

        return least_sampled_index

    def step(self, t):
        least_sampled = self.least_sample_index()
        arm_i = np.random.choice(least_sampled)
        reward = self.bandit.play(arm_i)
        self.add_reward(arm_i, reward)
        J_t = np.argsort(-self.mean_per_arm)[0:self.m]
        return J_t













