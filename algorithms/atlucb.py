import numpy as np
import bottleneck
import random
class AT_LUCB:
    #PL: the d symbol is not a sigma but a delta?
    
    def __init__(self, sigma1, alpha, epsilon ,bandit, m):
        self.sigma1 = sigma1
        self.alpha = alpha
        self.bandit = bandit
        self.epsilon = epsilon
        self.m = m
        #PL: refactor rewards_per_arm
        self.reward_perarm = [[] for i in range(len(bandit.arms))]
        #PL: refactor mean_per_arm
        self.mean_estimates = np.full(len(bandit.arms), float(0))

        #PL: why intialize Jt to a random number?
        #why not to -1, it is never used until it is set in the algo right?
        self.Jt = np.random.randint(len(bandit.arms), size=self.m)

        #PL:
        #no need to keep this history here,
        #it is not part of the algo, if you want to keep it,
        #keep it where you call the algorithm !
        # -> decouple: only have the algo stuff here!
        self.J = [] # history of top m
        self.J.append(self.Jt)

        #you don't need a list? just S_t?
        self.S = [1] #list of stages, initially 1

    #use this function
    def sigma(self, s):
        return sigma1 * alpha**(s-1)

    def beta(self, u, t, sigma1):
        k1 = 1.25
        n = len(self.bandit.arms)
        return (np.log(n)*k1*((t)**4)/sigma1)/(2*u))**0.5

    #PL:
    #determines whether the terminal condition for this stage is satisfied
    #  -> correct?
    def term(self, J_t, t, sigma, epsilon):
        h = h(t, sigma, J_t)
        l = l(t, sigma, J_t)
        U = U(t, l, sigma)
        T = T(t, h, sigma)
        return U - T < epsilon
        
    def L(self, t, a, sigma):
        mu = self.mean_estimates[a]
        if mu == 0.0:
            return float("-inf")
        else:
            return mu - self.beta(len(self.reward_perarm[a]), t, sigma)

    def U(self, t, a, sigma):
        mu = self.mean_estimates[a]
        if mu == 0.0:
            return float("inf")
        else:
            return mu + self.beta(len(self.reward_perarm[a]), t, sigma)

    def h(self, t, sigma, J_t):
        min_ = sys.float_info.max
        for j in J_t:
            L = L(t, j, sigma)
            if L < min_:
                min_ = L
        return min_

    def l(self, t, sigma, J_t):
        max_ = sys.float_info.min
        for j in J_t:
            U = U(t, j, sigma)
            if U > max_:
                max_ = U
        return max_
                
                
        

    def high_arm(self, t): #return the mini  mean -beta  of top m and its index
        mini_list = [True if self.mean_estimates[i] == 0 else (self.mean_estimates[i] - self.beta(np.sum(self.reward_perarm[i])/self.mean_estimates[i], t-1, self.sigma)) for i in self.J[t-1]]
        # mini_list store the mean_estimates - Beta of the top m arms.
        # store the ones nerve been pulled as True (beta is infinite)
        if True in mini_list:
            mini = True
        else:
            mini = np.min(mini_list)
        index = self.J[t-1][mini_list.index(mini)]
        return index, mini


    def low_arm(self,t):#return the max  mean + beta  of top m and its index
        maxm_list = [True if self.mean_estimates[i]==0 else (self.mean_estimates[i] + self.beta(np.sum(self.reward_perarm[i]) / self.mean_estimates[i], t-1, self.sigma)) for i in range(len(self.mean_estimates))]
        # maxm_list store the mean_estimates + Beta of the all the arms.
        # store the ones nerve been pulled as True (beta is infinite)
        for i in range(self.m):
            maxm_list[(self.J[t-1])[i]] = 0
        #keep the mean_estimates + beta of top m as 0 to make sure it will not been pulled
        if True in maxm_list:
            maxm = True
        else:
            maxm = np.max(maxm_list)
        index = maxm_list.index(maxm)
        return index, maxm

    def get_top_m(self):
        return bottleneck.argpartition(-self.mean_estimates, self.m)[:self.m]

    def add_reward(self, arm_i, reward):
        self.reward_perarm[arm_i].append(reward)
        self.mean_estimates[arm_i] = np.mean(self.reward_perarm[arm_i])

    def step(self, t):
        if self.term(t, self.epsilon):
            s = self.S[t - 1]
            while self.term(t, self.epsilon):
                s = s + 1
                self.sigma = self.sigma*(self.alpha**(self.s-1))
            self.S.append(s)
            self.Jt = self.get_top_m()
        else:
            self.S.append(self.S[t-1])
            if self.S[t] == 1:
                self.Jt = self.get_top_m()
        high_index = self.high_arm(t)[0]
        low_index = self.low_arm(t)[0]
        highreward = self.bandit.play(high_index)
        self.add_reward(high_index, highreward)
        #pull H
        lowreward = self.bandit.play(low_index)
        self.add_reward(low_index, lowreward)
        #pull L
        self.J.append(self.Jt)
        return self.Jt,self.S[t]




















