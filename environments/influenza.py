import numpy as np
import csv
from bandit import Bandit

def thresholds(data):
    with open(data, encoding="utf8", errors='ignore', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dict = {}
        for row in reader:
            dict[row['R_0']] = row['T_0 (cutoff=10^10)']
    return dict

def read_data(data,R_0):
    thre = thresholds("thresholds.csv")
    arms_n = 32
    population = 560000
    preventive_data = [[] for i in range(arms_n)]
    for i in range(arms_n):
        real_distribution = open(data+"/%i.txt" %i,'r')
        for line in real_distribution:
            if float(line) > float(thre[str(R_0)])/population:
                preventive_data[i].append(1-float(line))
    return preventive_data

def preventive_means(R_0):
    data = read_data("real-distributions/seattle-"+str(R_0),R_0)
    mean_fn = lambda i: np.mean(data[i])
    means = list(map(mean_fn, range(len(data))))
    return means

def preventive_bandit(variance, R_0):
    preventive_data = read_data("real-distributions/seattle-" + str(R_0), R_0)
    # means = preventive_means(R_0)
    # stddev = np.sqrt(variance)
    # def reward_fn(mu):
    #     return lambda: np.random.normal(mu, stddev)
    def reward_fn(mu):
        return lambda: np.random.choice(mu, size=1)
    arms = list(map(reward_fn, preventive_data))
    return Bandit(arms)
#
# R_0 =2
# a = preventive_means(R_0)
# b = (np.argsort(a)[:32])
# c = (np.sort(a)[:32])
# print(b)
# print(c)
# print(sum(b[29:32]))

# data = read_data("real-distributions/seattle-"+str(R_0),R_0)
# print(data[24])
# print(data[24].index(0.000262672))
# pos=[i for i in range(32)]
# plt.figure(2)
# plt.title("uniform", fontweight='bold')
# plt.xlabel('t')
# plt.ylabel('sum')
# plt.violinplot(data,pos,points=40,showmeans=True,showmedians=True)
# plt.legend()
# plt.xlim(0, 32)
# plt.ylim(0.0, 0.3)
# plt.show()