import csv
from bandit import Bandit
import numpy as np

def read_data(data):
    captions_data = np.zeros((499, 3))
    with open(data,encoding="utf8", errors='ignore', newline='') as csvfile:
             reader = csv.DictReader(csvfile)
             for row in reader:
                 caption_id = int(row['target_id']) - 1
                 reward_id = int(row['target_reward']) - 1
                 captions_data[caption_id][reward_id] = captions_data[caption_id][reward_id] + 1
    for row in captions_data:
        sum_row = np.sum(row)
        for i in range(len(row)):
            row[i] = row[i]/sum_row
    return captions_data

captions_data = read_data('499-responses.csv')

def captions_means():
    mean_fn = lambda i: i[0]*0 +i[1]*0.5 +i[2]
    means = list(map(mean_fn, captions_data))
    return means

def captions_bandit():
    data = captions_data
    def reward_fn(percentage):
        return lambda: np.random.choice((0,0.5,1),1,p=percentage)[0]
    arms = list(map(reward_fn, data))
    return Bandit(arms)