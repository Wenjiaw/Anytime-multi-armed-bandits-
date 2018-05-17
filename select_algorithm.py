from algorithms import AT_LUCB
from algorithms import Uniform
from algorithms import NAIVE_DSAR
from algorithms import DSAR
from environments.gaussian_jun import linear_bandit,polynomial_bandit
from environments.captions_jun import captions_bandit
from environments.influenza import preventive_bandit
def select_algorithm(arm_n, m, variance, bandit,algorithm,R_0):
    if bandit == "linear":
        bandits = linear_bandit(arm_n, variance)
    elif bandit == "capition":
        bandits =captions_bandit()
    elif bandit == "influenza":
        bandits = preventive_bandit(variance,R_0)
    else:
        bandits = polynomial_bandit(arm_n, variance)

    if algorithm == "AT_LUCB":
        algo = AT_LUCB(0.5, 0.99, 0, bandits, m)
    elif algorithm == "DSAR":
        algo = DSAR(bandits, m)
    elif algorithm == "naive_DSAR":
        algo = NAIVE_DSAR(bandits, m)
    elif algorithm == "Uniform":
        algo = Uniform(bandits, m)
    return algo