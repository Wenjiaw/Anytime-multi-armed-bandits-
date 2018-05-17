import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from environments.gaussian_jun import linear_means,polynomial_means
from environments.captions_jun import captions_means
from environments.influenza import preventive_means

class Plot():
    def __init__(self, arm_n, m, steps, bandit, n):
        self.arm_n = arm_n
        self.m = m
        self.n = n
        self.steps =steps
        self.bandit = bandit


    def read_data(self,data,R_0):
        if self.bandit == "linear":
            means_value = linear_means(self.arm_n)
        elif self.bandit == "capition":
            means_value = captions_means()
        elif self.bandit == "influenza":
            means_value = preventive_means(R_0)
        else:
            means_value = polynomial_means(self.arm_n)
        result = np.zeros((2, self.steps))
        with open(data,"r") as csvfile:
                 reader = csv.reader(csvfile)
                 count = 0
                 for row in reader:
                     try:
                        top_m = [means_value[int(i)] for i in row]
                        result[0][count] = np.min(top_m)
                        result[1][count] = np.sum(top_m)
                        count = count + 1

                     except:
                        pass
        return result

    def get_means(self,data):
        result = np.zeros((2, self.steps))
        for i in range(1,self.n+1):
            J_t_value = self.read_data('%s/outfile_%i.csv'%(data,i))
            result = result + J_t_value
        result = result / self.n
        return result

    def plot(self):
        dsar_data = "output_%s_DSAR_%i" % (self.bandit, self.m)
        naivedsar_data = "output_%s_naive_DSAR_%i" % (self.bandit, self.m)
        uniform_data = "output_%s_Uniform_%i" % (self.bandit, self.m)
        ATLUCB_data = "output_%s_AT_LUCB_%i" % (self.bandit, self.m)
        naivedsar = self.get_means(naivedsar_data)
        uniform = self.get_means(uniform_data)
        dsar = self.get_means(dsar_data)
        ATLUCB = self.get_means(ATLUCB_data)
        plt.figure(1)
        plt.title('%s m = %i min' % (self.bandit, self.m), fontweight='bold')
        plt.xlabel('t')
        plt.ylabel('min')
        plt.plot(ATLUCB[0], 'b-', color='g', label='AT_LUCB')
        plt.plot(naivedsar[0], 'b-', color='y', label="naive_DSAR")
        plt.plot(uniform[0], 'b-', color='b', label='uniform')
        plt.plot(dsar[0], 'b-', color='r', label='DSAR')
        plt.legend()
        plt.xlim(0, steps)
        plt.ylim(0.3, 0.9)
        plt.savefig('%s m = %i_min.png' % (self.bandit, self.m))
        plt.figure(2)
        plt.title('%s m = %i sum' % (self.bandit, self.m), fontweight='bold')
        plt.xlabel('t')
        plt.ylabel('sum')
        plt.plot(ATLUCB[1], 'b-', color='g', label='AT_LUCB')
        plt.plot(naivedsar[1], 'b-', color='y', label="naive_DSAR")
        plt.plot(uniform[1], 'b-', color='b', label='Uniform')
        plt.plot(dsar[1], 'b-', color='r', label='DSAR')
        plt.legend()
        plt.xlim(0, self.steps)
        plt.ylim(36.0, 44.0)
        plt.savefig('%s m = %i_sum.png' % (self.bandit, self.m),format='png')




arms = 1000
m=50
steps = 150000
bandit = "linear"
n = 200

plot = Plot(arms,m,steps,bandit,n).plot()







