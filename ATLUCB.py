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
from master.value import *
def LinearValue(n):
    reward = np.arange(n - 1, -1, -1)
    return reward * 0.9 / 999


class AT_LUCB(object):
    def __init__(self,n,interation,sigma,alpha,zeta,m,value):
        self.n=n
        self.interation=interation
        self.sigma=sigma
        self.alpha=alpha
        self.zeta = zeta
        self.m=m
        self.value=value

    def belta(self,u,t,sigma1):
        k1=1.25
        belta=(np.log((self.n)*k1*(t**4)/sigma1)/(2*u))**0.5
        return belta

    def temi(self,empircal,Jsamles,t,sigma1):
        if (0 in empircal[1] or 0 in Jsamles[1]):
            return False
        else:
            for i in range(self.n):
                if i in Jsamles[0]:
                    #empircal[2][i]=empircal[0][i]-self.belta(empircal[1][i],t,sigma1)
                    index = np.where(Jsamles[0] == i)[0]
                    Jsamles[3][index]=empircal[0][i]-self.belta(empircal[1][i],t,sigma1)
                    empircal[2][i]=0
                else:
                    empircal[2][i] = empircal[0][i] +self.belta(empircal[1][i], t, sigma1)
            if np.max(empircal[2])-np.min(Jsamles[3])<0:
                return True
            else:
                return False

    def getEmpirical(self,empirical,Jsmaples):
        #heapq.nlargest(self.m, empirical[0])
        index= bottleneck.argpartition(-empirical[0], self.m)[:self.m]
        random.shuffle(index)
        for i in range(self.m):
            empirical[2][int(Jsmaples[0][i])]=Jsmaples[3][i]
        for j in range(self.m):
            Jsmaples[0]=index
            Jsmaples[1][j]=empirical[1][index[j]]
            Jsmaples[2][j]=empirical[0][index[j]]
            Jsmaples[3][j] = empirical[2][index[j]]
            empirical[2][index[j]]=0

    def pull(self,empircal,jsample):
        if (0 in jsample[1]):
            mzerolist=np.where(jsample[1]==0)[0]
            high=np.random.choice(mzerolist)
            highindex=int(jsample[0][high])
            emzerolist=np.where(empircal[1]==0)[0]
            emzerolistfilter=[i for i in emzerolist if i not in jsample[0]]
            lowindex=np.random.choice(emzerolistfilter)

        elif (0 in empircal[1]):
            high=np.where(jsample[3]==np.min(jsample[3]))[0]
            high=np.random.choice(high)
            highindex=int(jsample[0][high])
            emzerolist = np.where(empircal[1] == 0)[0]
            lowindex= np.random.choice(emzerolist)

        else:
            high = np.where(jsample[3] == np.min(jsample[3]))[0]
            high = np.random.choice(high)
            highindex = int(jsample[0][high])
            lowindex = np.where(empircal[2] == np.max(empircal[2]))[0]
            lowindex=np.random.choice(lowindex)
        lowvalue=np.random.normal(self.value[lowindex],0.4)
        highvalue=np.random.normal(self.value[highindex],0.4)
        jsample[1][high]=jsample[1][high]+1
        jsample[2][high]=jsample[2][high]+(highvalue-jsample[2][high])/(jsample[1][high])
        empircal[1][int(lowindex)]=empircal[1][int(lowvalue)]+1
        empircal[0][int(lowindex)]=empircal[0][int(lowindex)]+(lowvalue-empircal[0][int(lowindex)])/(empircal[1][int(lowindex)])
        empircal[1][int(highindex)]=empircal[1][int(highindex)]+1
        empircal[0][int(highindex)]=jsample[2][high]

    def recommand(self,jsample):
        return np.min(jsample[2]),np.sum(jsample[2])

    def undate(self):
        t=1
        Jsmaples=np.zeros((4,self.m))
        s=1
        sigma1=self.sigma*(self.alpha**(s-1))
        empirical=np.zeros((3,self.n))
        minresult=[]
        sumresult=[]

        for i in range(self.n):
            empirical[0][i]=np.random.normal(self.value[i],0.4)
            empirical[1][i]= empirical[1][i]+1
        self.getEmpirical(empirical,Jsmaples)
        print(self.value)
        print(empirical)
        print(Jsmaples)
        while t<self.interation+1:
            if (self.temi(empirical,Jsmaples,t,sigma1)):
                s = s + 1
                while self.temi(empirical,Jsmaples,t,sigma1):
                    s = s + 1
                    sigma1 = self.sigma * (self.alpha ** (s - 1))
                self.getEmpirical(empirical,Jsmaples)

            else:
                if s==1:
                    self.getEmpirical(empirical, Jsmaples)
                else:
                    pass

            self.pull(empirical,Jsmaples)
            minresult.append(np.min(Jsmaples[2]))

            sumresult.append(np.sum(Jsmaples[2]))
            t=t+1

        return minresult,sumresult,s

value=LinearValue(1000)
interation=150000
Lineam10=AT_LUCB(1000,interation,0.5,0.99,1,10,value)
print(Lineam10.undate()[0])
print(Lineam10.undate()[2])

# for i in range(200):
#     Lineam10 = AT_LUCB(1000, interation, 0.5, 0.99, 1, 10, value)
#     result=np.zeros_like(Lineam10.undate()[0])
#     result=result+Lineam10.undate()[0]
# result=result/200




plt.figure(1)

plt.title('Linear m=10', fontweight='bold')
plt.xlabel('t')
plt.ylabel('min')
plt.plot(Lineam10.undate()[0],'b-',color='r',label='AT-LUCB')


plt.legend()
plt.xlim(0,interation)
plt.ylim(0,1)
plt.show()
















