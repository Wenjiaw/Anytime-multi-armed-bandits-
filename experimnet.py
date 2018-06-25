#!/usr/bin/env python3
import numpy as np
from select_algorithm import select_algorithm,select_bandit

from argparse import ArgumentParser

parser = ArgumentParser(description="""
Calculate the m_best bandits
""")

parser.add_argument("-a", "--armn", dest="arm_n", type=int, required=True)
parser.add_argument("-v", "--variance", dest="variance", type=float, required=True)
parser.add_argument("-s", "--seed", dest="seed_num", type=int, required=True)
parser.add_argument("-st", "--steps", dest="steps", type=int, required=True)
parser.add_argument("-m", "--m", dest="m",type=int, required=True)
parser.add_argument("-algo", "--algo", dest="algo", type=str, required=True)
parser.add_argument("-b", "--bandits", dest="bandits",type=str, required=True)
parser.add_argument("-R", "--R_0", dest="R_0",type=str, required=False)
parser.add_argument("-D", "--distribution_method", dest="distribution_method",type=str, required=False)
args = parser.parse_args()

class EXPERIMENT_JUN():
    def __init__(self, arm_n, m, variance, steps, seed_num, algo, bandit, distribution_method, *R_0):
        self.arm_n = arm_n
        self.m = m
        self.variance = variance
        self.steps =steps
        self.seed_num = seed_num
        self.algo = algo
        self.bandit = bandit
        self.distribution_method = distribution_method
        self.R_0 = R_0[0]
    def experiment(self):
        np.random.seed(self.seed_num)
        bandit = select_bandit(self.arm_n, self.variance, self.bandit,self.R_0)
        algo = select_algorithm(self.arm_n,self.variance, self.m,bandit,self.algo, self.distribution_method)
        header = ['m %i' % i for i in range(1,self.m+1)]
        print(",".join(header))
        for t in range(1,self.steps +1):
            #reward = algo.step(t)
            J_t = algo.step(t)
            J_t = [str(i) for i in J_t]
            print(",".join(J_t))
            # if t == 150000:
            #     return reward[1]
poly_10 = EXPERIMENT_JUN(args.arm_n, args.m, args.variance, args.steps, args.seed_num, args.algo, args.bandits,args.distribution_method,args.R_0).experiment()
#a = EXPERIMENT_JUN(1000, 10, 0.25, 100000, 6, "Thompson", "linear","uniform_and_zipf",2).experiment()


#
# pos=[i for i in range(32)]
# plt.figure(2)
# plt.title("uniform", fontweight='bold')
# plt.xlabel('t')
# plt.ylabel('sum')
# plt.violinplot(a,pos,points=40,showmeans=True,showmedians=True)
# plt.legend()
# plt.xlim(0, 32)
# plt.ylim(0.0, 2.0)
# plt.show()

