# from master.environments.gaussian_jun import sample
class Bandit:
    #ctor: accepts list of functions,
    #each function represents an arm's reward distribution
    def __init__(self, arms):
        self.arms = arms

    def play(self,  arm_i):
        reward = self.arms[arm_i]()
        return reward



