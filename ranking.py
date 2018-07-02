import numpy as np
from scipy import stats


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
        return lambda order: np.random.choice(order, p=p_list)


def mth_and_mplus1s(m):
    return lambda order: np.random.choice((order[m-1],order[m]),p=[0.5,0.5])


def poisson(arm_n, m):

    result = arm_n
    while result > arm_n -1:
        result = np.random.poisson(m - 1)
    return lambda order: order[np.random.poisson(m-1)]

def create_zipf(s, n):
    x = np.arange(1, n+1)
    weights = 1/x**s
    weights /= weights.sum()
    return stats.rv_discrete(name='bounded_zipf', values=(x, weights))

def sample_mirrored_zipf(s, N, m):
    zipf = create_zipf(s, N-m)
    # try 10000 times, as sampling from the left may fail (i.e., be negative) 
    for i in range(10000):
        # select randomly 50/50 the left or right side of the distribution
        if np.random.randint(0, 2) == 0:
            r = zipf.rvs()
            sample = m + 1 - r
            if sample > 0:
                return sample
        else:
            r = zipf.rvs()
            return m + r 
     raise Exception('Unable to sample from mirrorred zipf')
