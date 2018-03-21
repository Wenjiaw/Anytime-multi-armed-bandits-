import numpy as np
import bottleneck
import random

class AT_LUCB:
    def __init__(self, sigma, alpha, epsilon ,bandit, m):
        self.sigma = sigma
        self.alpha = alpha
        self.bandit = bandit
        self.epsilon = epsilon
        self.m = m
        self.reward_perarm = [[] for i in range(len(bandit.arms))]
        self.mean_estimates = self.mean_estimates = np.full(len(bandit.arms), float(0))
        self.S =  []
        self.Jt = np.full(self.m , 0)
        self.J = []

    def beta(self, u, t, sigma1):
        k1 = 1.25
        beta = (np.log((len(self.bandit.arms[1]))*k1*(t**4)/sigma1)/(2*u))**0.5
        return beta


    def term(self, t, sigma1, epsilon):   #satifies the terminal candition or not
        if ():
            return False
        else:


    def high_arm(self, t):
        mini_list = [(self.mean_estimates[i]-self.beta(np.sum(self.reward_perarm[i])/self.mean_estimates[i], t-1, self.sigma)) for i in self.J[t-1]]
        mini = np.min(mini_list)
        index = mini_list.index(mini)
        return index, mini

    def low_arm(self,t):
        maxm_list=[(self.mean_estimates[i] + self.beta(np.sum(self.reward_perarm[i]) / self.mean_estimates[i], t-1, self.sigma)) for
          i in range(len(self.mean_estimates)) if i not in self.Jt[t-1]]
        maxm = np.max(maxm_list)
        index = maxm_list.index(maxm)
        return index, maxm


    def get_top_m(self):
        self.Jt = bottleneck.argpartition(-self.mean_estimates, self.m)[:self.m]

    def add_reward(self, arm_i, reward):
        self.reward_perarm[arm_i].append(reward)
        self.mean_estimates[arm_i] = np.mean(self.reward_perarm[arm_i])


    def step(self, t):

        if self.term(self.sigma, self.epsilon):
            s = self.S[t - 1]
            while self.term(self.sigma, self.epsilon):
                s = s + 1
                self.sigma = self.sigma*(self.alpha**(self.s-1))
            self.S.append(s)
            self.Jt = self.get_top_m()

        else:
            self.S.append(self.S[t-1])
            if self.S[t] == 1:
                self.Jt = self.get_top_m()
            self.J.append(self.Jt)

        high_index = self.high_arm(t-1)
        low_index =self.low_arm(t-1)
        highreward = self.bandit.play(high_index)
        self.add_reward(highreward)
        lowreward = self.bandit.play(low_index)
        self.add_reward(lowreward)
        self.J.append(self.Jt)
        return self.J_t




















