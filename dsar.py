import numpy as np
import math
from fractions import Fraction
#PL: just have one DSAR file, that you can configure with a Boolean?

class DSAR:
    def __init__(self, bandit, m, boolean):
        self.bandit = bandit
        self.m = m
        self.boolean = boolean
        self.reward_per_arm = [[] for i in range(len(self.bandit.arms))]
        self.mean_per_arm = np.full(len(bandit.arms), float(0))
        self.active = [i for i in range(len(self.bandit.arms))]
        self.Jt = np.random.choice(len(self.bandit.arms),self.m)
        self.Jt_naive = np.copy(self.Jt)#return Jt_naive if DSAR_naive
        self.s = 1
        self.i = 0
        self.phase_counter = 1
        self.k = 1
        self.m_lack = self.m

    def next_stage(self):
       self.m_lack = self.m
       self.s = self.s + 1
       self.active = [i for i in range(len(self.bandit.arms))]
       self.k = 1
       self.phase_counter = self.n_k(self.k) - self.n_k(self.k - 1)

    def n_k(self, k):
        budget = 2 ** (self.s - 1) * len(self.bandit.arms)
        if k == 0:
            return 0
        else:
            K = len(self.bandit.arms)
            n = budget
            return math.ceil((1/self.log_(K)) * (n-k)/(K+1-k))

    def log_(self, n):
        a = Fraction(1,2)
        for i in range(2, n + 1):
            a = a + Fraction(1,i)
        return float(a)

    def add_reward(self, arm_i, reward):
        self.reward_per_arm[arm_i].append(reward)
        self.mean_per_arm[arm_i] = np.mean(self.reward_per_arm[arm_i])
    
    def max_gap(self,mean_active,r):
        up_gap = mean_active[r[0]] - mean_active[r[self.m_lack]]
        down_gap = mean_active[r[self.m_lack - 1]] - mean_active[r[-1]]
        if up_gap >= down_gap:
            return self.active[r[0]]
        else:
            return self.active[r[-1]]

    def get_top_m(self):
        if self.m_lack == 0:
            pass
        else:
            mean_active = self.mean_per_arm[self.active]
            index = np.argsort(-mean_active)
        for i in range(self.m_lack):
            self.Jt[self.m - self.m_lack + i] = self.active[index[i]]
        return self.Jt
    #return depending on your DSAR variant that is defined by the Boolean ...
    def step(self, t):
        reward = self.bandit.play(self.active[self.i])
        self.add_reward(self.active[self.i], reward)
        self.Jt = self.get_top_m()
        if self.i < len(self.active) - 1:
            self.i = self.i + 1
        else:
            self.phase_counter = self.phase_counter - 1
            self.i = 0
            while self.phase_counter == 0:
                if self.m_lack > 0:
                    mean_active = self.mean_per_arm[self.active]
                    r = np.argsort(-mean_active)
                    i_k = self.max_gap(mean_active,r)
                    if self.active[r[0]] == i_k:
                        self.Jt[self.m - self.m_lack] = i_k
                        self.m_lack = self.m_lack - 1
                    self.active.remove(i_k)
                if self.k < len(self.bandit.arms) - 1:
                    self.k = self.k + 1
                    self.phase_counter = self.n_k(self.k) - self.n_k(self.k - 1)
                else:
                    self.Jt_naive = np.copy(self.Jt)
                    self.next_stage()
        if self.boolean == True:
            return self.Jt
        else:
            return self.Jt_naive