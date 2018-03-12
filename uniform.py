import matplotlib.pyplot as plt
import numpy as np
import bottleneck
import heapq
import random
import math
import seaborn as sns
import scipy.stats as stats
import matplotlib.patches as mpatches
plt.rcParams['figure.figsize'] = (10, 8)

def LinearValue(n):
    reward = np.arange(n - 1, -1, -1)
    return reward * 0.9 / 999


class uniform(object):
    def __init__(self,n,interation,m,value):
        self.n=n
        self.interation=interation
        self.m=m
        self.value=value



    def getEmpirical(self,empirical,Jsmaples,t):
        #heapq.nlargest(self.m, empirical[0]
        # term=empirical.copy()
        # a=np.transpose(term)
        # np.random.shuffle(a)
        # b=np.transpose(a)
        index = bottleneck.argpartition(-empirical[1], self.m)[:self.m]




        # if t < self.m:
        #     leastsampled = np.where(empirical[0] == 0)[0]
        #     maxvalueindex=np.where(empirical[0] !=0)[0]
        #     index=np.random.choice(leastsampled,self.m-t)
        #     index=np.append(index,maxvalueindex)
        # else:
        #     index = bottleneck.argpartition(-empirical[1], self.m)[:self.m]
        # index = bottleneck.argpartition(-empirical[1], self.m)[:self.m]
        if 0 in empirical[0][index]:
            zeroindex=np.where(empirical[0]==0)[0]
            newindex=np.array([i for i in index if i not in zeroindex])
            a=np.random.choice(zeroindex,(len(index)-len(newindex)))
            index=np.append(a,newindex)
        else:
            pass



        for j in range(self.m):
            Jsmaples[0]=index
            Jsmaples[1][j]=empirical[0][int(index[j])]
            Jsmaples[2][j]=empirical[1][int(index[j])]
        return Jsmaples

    def pull(self,empircal,least):
        empircal[0][least]=empircal[0][least]+1
        highvalue = np.random.normal(self.value[least], 0.4)
        empircal[1][least]=(empircal[1][least]*(empircal[0][least]-1)+highvalue)/empircal[0][least]
        return empircal
    def undate(self):
        t=1
        empirical=np.zeros((2,self.n))
        Jsample=np.zeros((3,self.m))
        minresult=[]
        sumresult=[]
        while t < self.interation + 1:
            leastsampled=np.where(empirical[0]==np.min(empirical[0]))[0]
            leastsampledindex=np.random.choice(leastsampled)
            result=self.pull(empirical,leastsampledindex)

            result1=self.getEmpirical(result,Jsample,t)
            minresult.append(np.min(result1[2]))
            sumresult.append(np.sum(result1[2]))
            t = t + 1


        return minresult,sumresult,empirical,Jsample


interation=1000
m=10
n=1000
value=LinearValue(n)
a=uniform(n,interation,m,value)
print(a.undate()[0])
print(a.undate()[2])
result=np.zeros_like(a.undate()[0])
for i in range(200):
    Lineam10 = uniform(n, interation,m, value)

    result=result+Lineam10.undate()[0]
result=result/200




plt.figure(1)

plt.title('Linear m=10 Uniform', fontweight='bold')
plt.xlabel('t')
plt.ylabel('min')
plt.plot(result,'b-',color='r',label='Uniform')


plt.legend()
plt.xlim(0,interation)
plt.ylim(0,2)
plt.show()
















