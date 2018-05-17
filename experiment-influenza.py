#!/usr/bin/env python3
import numpy as np
from select_algorithm import select_algorithm
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
parser.add_argument("-R", "--R_0", dest="R_0",type=str, required=True)
args = parser.parse_args()

class EXPERIMENT_JUN():
    def __init__(self, arm_n, m, variance, steps, seed_num, algo, bandit, *R_0):
        self.arm_n = arm_n
        self.m = m
        self.variance = variance
        self.steps =steps
        self.seed_num = seed_num
        self.algo = algo
        self.bandit = bandit
        self.R_0 = R_0[0]
    def experiment(self):
        np.random.seed(self.seed_num)
        algo = select_algorithm(self.arm_n, self.m, self.variance, self.bandit, self.algo, self.R_0)
        J_t = algo.step(1)
        J_t = [str(i) for i in J_t]
        header = ['m %i' % i for i in range(1,(len(J_t)+1))]
        print(",".join(header))
        print(",".join(J_t))
        for t in range(2,self.steps +1):
            J_t = algo.step(t)
            J_t = [str(i) for i in J_t]
            print(",".join(J_t))

poly_10 = EXPERIMENT_JUN(args.arm_n, args.m, args.variance, args.steps, args.seed_num, args.algo, args.bandits, args.R_0).experiment()
