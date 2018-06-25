import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from select_algorithm import select_means
from argparse import ArgumentParser

parser = ArgumentParser(description="""
Calculate the m_best bandits
""")

parser.add_argument("-a", "--armn", dest="arm_n", type=int, required=True)
parser.add_argument("-st", "--steps", dest="steps", type=int, required=True)
parser.add_argument("-m", "--m", dest="m",type=int, required=True)
parser.add_argument("-b", "--bandits", dest="bandits",type=str, required=True)
parser.add_argument("-R", "--R_0", dest="R_0",type=str, required=False)
parser.add_argument("-n", "--n", dest="n",type=int, required=False)

parser.add_argument("-min_U", "--min_U", dest="min_U", type=float, required=True)
parser.add_argument("-min_L", "--min_L", dest="min_L", type=float, required=True)
parser.add_argument("-sum_U", "--sum_U", dest="sum_U", type=float, required=True)
parser.add_argument("-sum_L", "--sum_L", dest="sum_L", type=float, required=True)
parser.add_argument("-Success_U", "--Success_U", dest="Success_U",type=float, required=True)
parser.add_argument("-Success_L", "--Success_L", dest="Success_L",type=float, required=True)
args = parser.parse_args()


class Plot():
    def __init__(self,arm_n,m,bandits,steps,n,R_0,min_U,min_L,sum_U,sum_L,Success_U,Success_L):
        self.m = m
        self.n = n
        self.bandit = bandits
        self.steps = steps
        self.means = select_means(arm_n,bandits,R_0)
        self.R_0 = R_0
        self.min_U = min_U
        self.min_L = min_L
        self.sum_U = sum_U
        self.sum_L = sum_L
        self.Success_U = Success_U
        self.Success_L = Success_L

    def read_data(self,data):
        min_sum_success_rate = np.zeros((3,self.steps))
        m_best_means = np.argpartition(self.means, -self.m)[-self.m:]

        with open(data,"r") as csvfile:
                 reader = csv.reader(csvfile)
                 for index, row in enumerate(reader):
                     if index == 0:
                         pass
                     else:
                         in_list = [i for i in row if int(i) in m_best_means]
                         min_sum_success_rate[2][index-1] = len(in_list)/self.m
                         top_m = [self.means[int(i)] for i in row]
                         min_sum_success_rate[0][index-1] = np.min(top_m)
                         min_sum_success_rate[1][index-1] = np.sum(top_m)
                         if index == self.steps:
                             return min_sum_success_rate

    def get_means(self,data):
        min_sum_success_rate = np.zeros((3, self.steps))
        for i in range(1,self.n+1):
            J_t_value = self.read_data('%s/outfile_%i.csv'%(data,i))
            min_sum_success_rate = min_sum_success_rate + J_t_value
        min_sum_success_rate = min_sum_success_rate / self.n
        return min_sum_success_rate

    def plot(self):
        if self.bandit == "influenza":
            dsar_data = "output_%s_DSAR_%i" % (self.R_0,self.m)
            naivedsar_data = "output_%s_naive_DSAR_%i" % (self.R_0,self.m)
            uniform_data = "output_%s_Uniform_%i" % (self.R_0,self.m)
            ATLUCB_data = "output_%s_AT_LUCB_%i" % (self.R_0,self.m)
            Thompson_data = "output_%s_Thompson_%i" % (self.R_0,self.m)
        else:
            dsar_data = "output_%s_DSAR_%i" % (self.bandit, self.m)
            naivedsar_data = "output_%s_naive_DSAR_%i" % (self.bandit, self.m)
            uniform_data = "output_%s_Uniform_%i" % (self.bandit, self.m)
            ATLUCB_data = "output_%s_AT_LUCB_%i" % (self.bandit, self.m)
            Thompson_data = "output_%s_Thompson_%i" % (self.bandit, self.m)
        naivedsar = self.get_means(naivedsar_data)
        uniform = self.get_means(uniform_data)
        dsar = self.get_means(dsar_data)
        ATLUCB = self.get_means(ATLUCB_data)
        Thompson = self.get_means(Thompson_data)
        plt.figure(1)
        if self.bandit == "influenza":
            plt.title('R_0 = %s m = %i min' % (self.R_0, self.m), fontweight='bold')
        else:
            plt.title('%s m = %i min' % (self.bandit, self.m), fontweight='bold')
        plt.xlabel('t')
        plt.ylabel('min')
        plt.plot(ATLUCB[0], 'b-', color='g', label='AT_LUCB')
        plt.plot(naivedsar[0], 'b-', color='y', label="naive_DSAR")
        plt.plot(uniform[0], 'b-', color='b', label='uniform')
        plt.plot(dsar[0], 'b-', color='r', label='DSAR')
        plt.plot(Thompson[0], 'b-', color='black', label='Thompson_Sample')
        plt.legend()
        plt.xlim(0, self.steps)
        plt.ylim(self.min_L, self.min_U)
        if self.bandit == "influenza":
            plt.savefig('R_0 = %s m = %i_min.png' % (self.R_0, self.m))
        else:
            plt.savefig('%s m = %i_min.png' % (self.bandit, self.m))

        plt.figure(2)
        if self.bandit == "influenza":
            plt.title('R_0 = %s m = %i sum' % (self.R_0, self.m), fontweight='bold')
        else:
            plt.title('%s m = %i sum' % (self.bandit, self.m), fontweight='bold')
        plt.xlabel('t')
        plt.ylabel('sum')
        plt.plot(ATLUCB[1], 'b-', color='g', label='AT_LUCB')
        plt.plot(naivedsar[1], 'b-', color='y', label="naive_DSAR")
        plt.plot(uniform[1], 'b-', color='b', label='Uniform')
        plt.plot(dsar[1], 'b-', color='r', label='DSAR')
        plt.plot(Thompson[1], 'b-', color='black', label='Thompson_Sample')
        plt.legend()
        plt.xlim(0, self.steps)
        plt.ylim(self.sum_L, self.sum_U)
        if self.bandit == "influenza":
            plt.savefig('R_0 = %s m = %i_sum.png' % (self.R_0, self.m), format='png')
        else:
            plt.savefig('%s m = %i_sum.png' % (self.bandit, self.m), format='png')

        plt.figure(3)
        if self.bandit == "influenza":
            plt.title('R_0 = %s m = %i success_rate' % (self.R_0, self.m), fontweight='bold')
        else:
            plt.title('%s m = %i success_rate' % (self.bandit, self.m), fontweight='bold')
        plt.xlabel('t')
        plt.ylabel('success_rate')
        plt.plot(ATLUCB[2], 'b-', color='g', label='AT_LUCB')
        plt.plot(naivedsar[2], 'b-', color='y', label="naive_DSAR")
        plt.plot(uniform[2], 'b-', color='b', label='uniform')
        plt.plot(dsar[2], 'b-', color='r', label='DSAR')
        plt.plot(Thompson[2], 'b-', color='black', label='Thompson_Sample')
        plt.legend()
        plt.xlim(0, self.steps)
        plt.ylim(self.Success_L, self.Success_U)
        if self.bandit == "influenza":
            plt.savefig('R_0 = %s m = %i_success_rate.png' % (self.R_0, self.m))
        else:
            plt.savefig('%s m = %i_success_rate.png' % (self.bandit, self.m))


# arm_n = 1000
# bandits = "linear"
# m=10
# steps = 150000
# R_0 = 1.4
# n = 200

# plot = Plot(arm_n,m,bandits,steps,n,R_0).plot()
plot = Plot(args.arm_n,args.m,args.bandits,args.steps,args.n,args.R_0,args.min_U,args.min_L,args.sum_U,args.sum_L,args.Success_U,args.Success_L).plot()