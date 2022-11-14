import sys
import time
import numpy as np
import pandas as pd
import seaborn as sns
sys.path.append('../laba_04')
from matplotlib import pyplot as plt
from Element import Element
from Create import Create
from Process import Process
from Despose import Despose
from Model import Model


v = 2
N = 10
time_modeling_list = range(100, 5000, 200)

times_list = []
events_list = []
events_theory_list = []

def calc_error(x, y):
    return 100 * (np.abs(np.array(x) - np.array(y))) / np.max([np.max(x), np.max(y)])

for time_modeling in time_modeling_list:
    curr_events_list = []
    curr_times_list = []
    for i in range(N):
        Element.id = 0
        c = Create(delay_mean = v, name = 'CREATOR', distribution = 'exp')
        p1 = Process(maxqueue = 100, delay_mean = .6, name = 'PROCESSOR1', distribution = 'exp')
        p2 = Process(maxqueue = 100, delay_mean = .3, name = 'PROCESSOR2', distribution = 'exp')
        p3 = Process(maxqueue = 100, delay_mean = .4, name = 'PROCESSOR3', distribution = 'exp')
        p4 = Process(maxqueue = 100, delay_mean = .1, name = 'PROCESSOR4', distribution = 'exp', n_channel = 2)
        d = Despose(name = 'DESPOSE')

        c.next_elements = [p1]
        p1.next_elements = [d, p2, p3, p4]
        p2.next_elements = [p1]
        p3.next_elements = [p1]
        p4.next_elements = [p1]

        p1.p = [0.42, 0.15, 0.13, 0.3]
        elements = [c, p1, p2, p3, p4, d]

        model = Model(elements, display_logs = False)
        start = time.time()
        quantity = model.simulate(time_modeling)
        curr_times_list.append(time.time() - start)
        curr_events_list.append(quantity)
        
    times_list.append(np.sum(curr_times_list) / N)
    events_list.append(np.sum(curr_events_list) / N)
    events_theory_list.append((np.sum(curr_times_list) / N) * v * 8000)

print(f'Error: {np.round(np.mean(calc_error(events_list, events_theory_list)), 5)}')


fig, ax = plt.subplots(1, 1, figsize = (15, 6))
sns.lineplot(x = 'count of events', y = 'time',
             data = pd.DataFrame(list(zip(events_list, times_list)), columns = ['count of events', 'time']),
             label = 'practical', ax = ax, color = 'orange')

sns.lineplot(x = 'count of events', y = 'time',
             data = pd.DataFrame(list(zip(events_theory_list, times_list)), columns = ['count of events', 'time']),
             label = 'theory', ax = ax, color = 'darkviolet')
ax.set_title(u'Experimental Assessment of Complexity');
plt.show()
