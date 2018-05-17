import numpy as np
import bottleneck
import math

#PL: just have one DSAR file, that you can configure with a Boolean?

class DSAR:
    def __init__(self, bandit, m):
        self.bandit = bandit
        self.m = m
        #same comments as for at-lucb
        self.reward_perarm = [[] for i in range(len(self.bandit.arms))]
        self.mean_estimates = np.full(len(self.bandit.arms), float(0))

        self.active = np.arange(1 ,len(self.bandit.arms)+1 , 1)
        #self.Jt = np.random.choice(len(self.bandit.arms),self.m)

        #PL: again, no history here
        self.J = []  # history of top m
        self.J.append(self.Jt)
        
        self.s = 1
        self.k = 1

        self.phase_counter = 0
        #self.m_lack = self.m
        #self.n = [0 if k == 0 else 1 for k in range(len(self.bandit.arms))]
        #self.count = self.n[self.k] - self.n[self.k - 1]
        #self.i = 0

    #def initial_stage(self):
    #    self.m_lack = self.m
    #    self.s = self.s + 1
    #    budget = 2 ** (self.s - 1) * len(self.bandit.arms)
    #    self.n = [math.ceil(self.n_k(k, budget)) for k in range(len(self.bandit.arms))]
    #    self.active = np.arange(1, len(self.bandit.arms) + 1, 1)
    #    self.k = 1
    #    self.count = self.n[self.k] - self.n[self.k-1]

    def n_k(self, k, budget):
        if k == 0:
            return 0
        else:
            K = len(self.bandit.arms)
            n = budget
            return 1/self.log_(K) * (n-k)/(K+1-k)

    #use fractions here, only convert to float when returing,
    #to avoid rounding errors
    def log_(self, n):
        a = 1 / 2
        for i in range(2, n + 1):
            a = a + 1 / i
        return a

    def add_reward(self, arm_i, reward):
        self.reward_perarm[arm_i].append(reward)
        self.mean_estimates[arm_i] = np.mean(self.reward_perarm[arm_i])

    #TODO: define a gap function n terms of the sigma bijection
    
    #def empirical_gaps(self):
    #    if self.m_lack == 0:
    #        pass
    #    else:
    #        mean_active = self.mean_estimates[self.active-1]
    #        index = np.argsort(-mean_active)
    #        if mean_active[index[0]] - mean_active[index[self.m_lack]] >= (
    #            mean_active[index[self.m_lack - 1]] - mean_active[index[-1]]):
    #            self.Jt[self.m - self.m_lack] = self.active[index[0]] - 1
    #            self.m_lack = self.m_lack - 1
    #            self.active = np.delete(self.active, index[0])
    #        else:
    #            self.active = np.delete(self.active, index[-1])
    #    return self.active

    def get_top_m(self):
        if self.m_lack == 0:
            pass
        else:
            mean_active = self.mean_estimates[self.active - 1]
            index = np.argsort(-mean_active)
        for i in range(self.m_lack):
            self.Jt[self.m - self.m_lack + i] = self.active[index[i]] - 1
        return self.Jt

    def step(self, t):
        reward = self.bandit.play(self.active[self.i] - 1)
        self.add_reward(self.active[self.i] - 1, reward)

        self.phase_counter = self.phase_counter + 1

        #if we are at the end of the phase
        if phase_counter > (n_k(k) - n_k(k-1)):
            #1. decide which arm to reject
            max_ = sys.float_info.min
            for a in active:
                g = gap(a, n_k(k))
                if g > max_:
                    max_ = g
                #TODO: remove max_ from active
                #    -> as you remove stuff from it,
                #       active is maybe better a list than an array?
            #2. go to the next phase
            self.k = self.k + 1

        #TODO: if all phases are done, go to the next stage
            
        
        
    #return depending on your DSAR variant that is defined by the Boolean ...
