from algorithms import AT_LUCB
from algorithms import Uniform
from algorithms import DSAR
from algorithms import UCB
from algorithms import DSH
from algorithms import TS
from environments.gaussian_jun import linear_means,linear_bandit,polynomial_means,polynomial_bandit,sparse_means,sparse_bandit
from environments.captions_jun import captions_means,captions_bandit
from environments.influenza import preventive_means,preventive_bandit
from posteriors.Gaussion_Posterior import GaussianPosterior
from posteriors.T_distribution_Posterior import T_Posterior
from ranking import uniform_and_zipf,mth_and_mplus1s,zipf,poisson

def select_means(arm_n,bandit,R_0):
    if bandit == "linear":
        means_value = linear_means(arm_n)
    elif bandit =="sparse":
        means_value = sparse_means(arm_n)
    elif bandit == "capition":
        means_value = captions_means()
    elif bandit == "influenza":
        means_value = preventive_means(R_0)
    else:
        means_value = polynomial_means(arm_n)
    return means_value

def select_bandit(arm_n,variance, bandit,R_0):
    if bandit == "linear":
        bandits = linear_bandit(arm_n, variance)
    elif bandit =="sparse":
        bandits = sparse_bandit(arm_n, variance)
    elif bandit == "capition":
        bandits =captions_bandit()
    elif bandit == "influenza":
        bandits = preventive_bandit(variance,R_0)
    else:
        bandits = polynomial_bandit(arm_n, variance)
    return bandits

def select_algorithm(bandit, arm_n,variance,m,bandits,algorithm,distribution_method):

    if algorithm == "AT_LUCB":
        algo = AT_LUCB(0.5, 0.99, 0, bandits, m)
    elif algorithm == "DSAR":
        algo = DSAR(bandits, m, True)
    elif algorithm == "naive_DSAR":
        algo = DSAR(bandits, m, False)
    elif algorithm == "UCB":
        algo = UCB(bandits, m)
    elif algorithm == "DSH":
        algo = DSH(bandits, m)
    elif algorithm == "Uniform":
        algo = Uniform(bandits, m)
    elif algorithm == "Thompson":
        if distribution_method == "uniform_and_zipf":
            rank = uniform_and_zipf(6,m,arm_n)
        elif distribution_method == "zipf":
            rank = zipf(3,arm_n)
        elif distribution_method =="mth_and_mplus1s":
            rank = mth_and_mplus1s(m)
        elif distribution_method =="poisson":
            rank = poisson(arm_n, m)
        if bandit == "influenza":
            posterior = T_Posterior
        elif bandit == "capition":
            pass
        else:
            posterior = GaussianPosterior(variance, 1, 0.45)
        algo = TS(bandits, m, rank, posterior)
    return algo