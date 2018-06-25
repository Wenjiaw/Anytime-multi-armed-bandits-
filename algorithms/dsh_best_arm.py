import numpy as np
import math

class DSH:
    def __init__(self, bandit, m):
        self.bandit = bandit
        self.m = m
        self.reward_per_arm = [[] for i in range(len(self.bandit.arms))]
        self.mean_per_arm = np.full(len(self.bandit.arms), float(0))
        self.S = np.arange(0,len(self.bandit.arms),1)
        self.Jt = -1
        self.s = 1
        self.phase_counter = self.get_phase_counter()
        self.i = 0
        self.r = 0

    def initial_stage(self):
        self.S = np.arange(0, len(self.bandit.arms), 1)
        self.s = self.s + 1
        self.phase_counter = self.get_phase_counter()
        self.r = 0

    def initial_rank(self):
        self.r = self.r + 1
        self.S = self.elimite_S()
        self.phase_counter = self.get_phase_counter()

    def get_phase_counter(self):
        budget = 2 ** (self.s - 1) * len(self.bandit.arms)
        return int(budget/(len(self.S)*np.ceil(math.log2(len(self.bandit.arms)))))

    def add_reward(self, arm_i, reward):
        self.reward_per_arm[arm_i].append(reward)
        self.mean_per_arm[arm_i] = np.mean(self.reward_per_arm[arm_i])

    def elimite_S(self):
        n = math.ceil(len(self.S)/2)
        mean_S = self.mean_per_arm[self.S]
        nonzero = np.nonzero(mean_S)
        if len(nonzero[0]) == 0:
             S = np.random.choice(self.S, n, replace = False)
        elif len(nonzero[0]) < n:
            zero_index = np.where(mean_S == 0)[0]
            zero_index_choice = np.random.choice(self.S[zero_index], n-len(nonzero[0]),replace=False)
            nonzero_index = self.S[nonzero[0]]
            S = np.hstack((nonzero_index, zero_index_choice))
        else:
            sorted = np.argsort(-mean_S)
            S = self.S[sorted[:n]]
        return S

    def step(self, t):
        while self.phase_counter == 0:
            self.initial_rank()
        reward = self.bandit.play(self.S[self.i])
        self.add_reward(self.S[self.i], reward)
        index = np.where(self.mean_per_arm == np.max(self.mean_per_arm[self.S]))[0]
        self.Jt = np.random.choice(index)
        if self.i == len(self.S) - 1:
            self.i = 0
            self.phase_counter = self.phase_counter - 1
            if self.phase_counter == 0:
                if self.r < math.ceil(math.log2(len(self.bandit.arms))) - 1:
                    self.initial_rank()
                else:
                    self.S = self.elimite_S()
                    self.Jt = self.S[0]
                    self.initial_stage()
        else:
            self.i = self.i + 1
        return [self.Jt]