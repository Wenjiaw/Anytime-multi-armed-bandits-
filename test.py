import numpy as np
def zipf(s, arm_n):
        N = arm_n
        p_list = np.zeros(N)
        sum = 0
        for n in range(1,N+1):
            sum = sum + 1/n**s
        for k in range(1,N+1):
            p_list[k-1] = (1/k**s) / sum

        return lambda order: np.random.choice(order, p=p_list)

def uniform_and_zipf(s,m,arm_n):
        N = arm_n
        p_list = np.zeros(N)
        sum = 0
        for n in range(1,N-m+1):
            sum = sum + 1/(n)**s
        p_uniform = ((1/1**s) / sum)
        Area = m * p_uniform + 1
        for k in range(1,N+1):
            if k < m + 1:
                p_list[k-1] = p_uniform/Area
            else:
                p_list[k-1] = ((1/(k-m)**s) / sum)/Area
        return p_list

def mth_and_mplus1s(m):
    return lambda order: np.random.choice([order[m-1],order[m]],p=[0.5,0.5])

a = uniform_and_zipf(10,10,1000)
print(a)
a = 1.4

