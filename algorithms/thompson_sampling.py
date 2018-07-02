
import numpy as np
class TS:
    def __init__(self, bandit, m, rank, posterior):
        self.bandit = bandit
        self.m = m
        self.posterior = posterior
        self.rank = rank
        self.reward_per_arm = [[] for i in range(len(self.bandit.arms))]

    def add_reward(self, arm_i, reward):
        self.reward_per_arm[arm_i].append(reward)

    def get_top_m(self):
        mean_per_arm = [posterior.mean(r) for r in self.reward_per_arm] 
        return np.argsort(-mean_per_arm)[0:self.m]

    def step(self, t):
        if t < len(self.bandit.arms) +1:
            reward = self.bandit.play(t-1)
            self.add_reward(t-1, reward)
        else:
            sample_result = np.zeros(len(self.reward_per_arm))
            for i in range(len(self.reward_per_arm)):
                sample_result[i] = self.posterior.sample_arm_i(self.reward_per_arm[i])
            order = np.argsort(-np.array(sample_result))
            arm_i = self.rank(order)
            reward = self.bandit.play(arm_i)
            self.add_reward(arm_i, reward)

        self.Jt = self.get_top_m()
        return self.Jt