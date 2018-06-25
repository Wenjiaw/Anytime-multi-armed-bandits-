import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from select_algorithm import select_means

class Plot():
    def __init__(self,arm_n,m,bandits,steps,n,R_0):
        self.m = m
        self.n = n
        self.bandit = bandits
        self.steps = steps
        self.means = select_means(arm_n,bandits,R_0)
        self.R_0 = R_0

    def read_data(self,data):
        min_sum_success_rate = np.zeros((2,self.steps))
        m_best_means = np.argpartition(self.means, -self.m)[-self.m:]

        with open(data,"r") as csvfile:
                 reader = csv.reader(csvfile)
                 for index, row in enumerate(reader):
                     if index == 0:
                         pass
                     else:
                         in_list = [i for i in row if int(i) in m_best_means]
                         min_sum_success_rate[1][index - 1] = 1 - len(in_list) / self.m
                         top_m = [self.means[int(i)] for i in row]
                         min_sum_success_rate[0][index - 1] = np.min(top_m)
                         if index == self.steps:
                             return min_sum_success_rate
        return min_sum_success_rate

    def get_means(self,data):
        min_sum_success_rate = np.zeros((2, self.steps))
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
            Thompson_data = "output_%s_Thompson_%i" % (self.R_0, self.m)
        else:
            dsar_data = "output_%s_DSAR_%i" % (self.bandit, self.m)
            naivedsar_data = "output_%s_naive_DSAR_%i" % (self.bandit, self.m)
            uniform_data = "output_%s_Uniform_%i" % (self.bandit, self.m)
            ATLUCB_data = "output_%s_AT_LUCB_%i" % (self.bandit, self.m)
            UCB_data = "output_%s_UCB_%i" % (self.bandit, self.m)
            DSH_data = "output_%s_DSH_%i" % (self.bandit, self.m)
            Thompson_data = "output_%s_Thompson_%i" % (self.bandit, self.m)
        uniform = self.get_means(uniform_data)
        dsar = self.get_means(dsar_data)
        ucb = self.get_means(UCB_data)
        dsh = self.get_means(DSH_data)
        ATLUCB = self.get_means(ATLUCB_data)
        Thompson = self.get_means(Thompson_data)
        plt.figure(1)
        if self.bandit == "influenza":
            plt.title('R_0 = %s m = %i min' % (self.R_0, self.m), fontweight='bold')
        else:
            plt.title('%s m = %i min' % (self.bandit, self.m), fontweight='bold')
        plt.xlabel('The # of samples')
        plt.ylabel('sum of J(t)')
        plt.plot(ATLUCB[0], 'b-', color='g', label='AT_LUCB')
        plt.plot(ucb[0], 'b-', color='y', label='UCB')
        plt.plot(dsh[0], 'b-', color='brown', label='DSH')
        plt.plot(uniform[0], 'b-', color='b', label='uniform')
        plt.plot(dsar[0], 'b-', color='r', label='DSAR')
        plt.plot(Thompson[0], 'b-', color='m', label='Thompson_Sample')
        plt.legend()
        plt.xlim(0, steps)
        plt.ylim(0.735, 0.765)
        if self.bandit == "influenza":
            plt.savefig('R_0 = %s m = %i_min.png' % (self.R_0, self.m))
        else:
            plt.savefig('%s m = %i_min.png' % (self.bandit, self.m))

        plt.figure(2)
        if self.bandit == "influenza":
            plt.title('R_0 = %s m = %i success_rate' % (self.R_0, self.m), fontweight='bold')
        else:
            plt.title('%s m = %i success_rate' % (self.bandit, self.m), fontweight='bold')
        plt.xlabel('The # of samples')
        plt.ylabel('unsuccess_rate')
        plt.plot(ATLUCB[1], 'b-', color='g', label='AT_LUCB')
        plt.plot(ucb[1], 'b-', color='y', label='UCB')
        plt.plot(dsh[1], 'b-', color='brown', label='DSH')
        plt.plot(uniform[1], 'b-', color='b', label='uniform')
        plt.plot(dsar[1], 'b-', color='r', label='DSAR')
        plt.plot(Thompson[1], 'b-', color='m', label='Thompson_Sample')
        plt.legend()
        plt.xlim(0, steps)
        plt.ylim(0.0, 1.0)
        if self.bandit == "influenza":
            plt.savefig('R_0 = %s m = %i_success_rate.png' % (self.R_0, self.m))
        else:
            plt.savefig('%s m = %i_success_rate.png' % (self.bandit, self.m))


arm_n = 1000
bandits = "influenza"
m=1
steps = 150000
R_0 = 1.4
n = 200

plot = Plot(arm_n,m,bandits,steps,n,R_0).plot()