import numpy as np
from FunRand import FunRand


class Element:
    id = 0
    def __init__(self, name = None, delay_mean = 1., delay_dev = 0., distribution = '', p = None, n_channel = 1):
        self.p = p
        self.id = Element.id
        Element.id += 1
        self.name = f'element_{self.id}' if name is None else name
        self.delay_mean = delay_mean # Середнє значення часової затримки
        self.delay_dev = delay_dev # Середнє квадратичне відхилення часової затримки
        self.distribution = distribution
        self.quantity = 0
        self.tcurr = 0 # Поточний момент часу
        self.next_elements = None
        self.n_channel = n_channel
        self.tnexts = [0.0] * self.n_channel # Список моменту часу наступної події
        self.states = [0] * self.n_channel
    
    # Розрахунок часової затримки
    def get_delay(self):
        if self.distribution == 'exp':
            return FunRand.exp(self.delay_mean)
        elif self.distribution == 'unif':
            return FunRand.unif(self.delay_mean, self.delay_dev)
        elif self.distribution == 'norm':
            return FunRand.norm(self.delay_mean, self.delay_dev)
        else:
            return self.delay_mean
    
    # Вхід в елемент
    def in_act(self):
        pass
    
    # Вихід з елементу
    def out_act(self):
        self.quantity += 1

    def print_statistic(self):
        print(f'{self.name}: Quantity = {self.quantity}, State={self.states}')
        
    def print_info(self):
        print(f'{self.name}: Quantity = {self.quantity}, State = {self.states}, tnext = {np.round(self.tnexts, 5)}')
    
    def find_curr_channels(self):
        res = []
        for i in range(self.n_channel):
            if self.tnexts[i] == self.tcurr:
                res.append(i)
        return res

    def find_empty_channels(self):
        empty_channels = []
        for i in range(self.n_channel):
            if self.states[i] == 0:
                empty_channels.append(i)
        return empty_channels
        
    def do_statistics(self, delta):
        pass
