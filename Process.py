import numpy as np
from Element import Element


class Process(Element):
    def __init__(self, maxqueue = np.inf, n_channel = 1, **kwargs):
        super().__init__(**kwargs)
        self.failure = 0
        self.queue = 0
        self.max_queue = maxqueue
        self.mean_queue = 0
        self.max_queue_length = self.queue
        self.n_channel = n_channel
        self.tnexts = [np.inf] * n_channel
        self.states = [0] * n_channel
        
    def in_act(self):
        free_channels = self.find_empty_channels()
        for i in free_channels:
            self.states[i] = 1 # Встановити значення пристрою: ʼзайнятийʼ
            self.tnexts[i] = self.tcurr + super().get_delay() # Встановити коли значення пристрою стане: ʼвільнийʼ
            break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
                if self.queue > self.max_queue_length:
                    self.max_queue_length = self.queue
            else:
                self.failure += 1
            
    def out_act(self):
        # виконуємо збільшення лічильника кількості
        super().out_act()
        current_channels = self.find_curr_channels()
        
        for i in current_channels:
            self.tnexts[i] = np.inf
            self.states[i] = 0 # Пристрій вільний

            # Якщо в черзі є елемент - дістаємо його
            if self.queue > 0:
                self.queue -= 1
                self.states[i] = 1
                self.tnexts[i] = self.tcurr + super().get_delay()
            elif self.next_elements is not None:
                next_element = np.random.choice(self.next_elements, p = self.p)
                next_element.in_act()
        
    def print_info(self):
        super().print_info()
        print(f'failure={self.failure}')
        
    def do_statistics(self, delta):
        self.mean_queue += delta * self.queue
