import numpy as np
from Despose import Despose
from Process import Process


class Model():
    def __init__(self, elements = [], display_logs = False):
        self.elements = elements
        self.tnext = 0
        self.event = elements[0]
        self.tcurr = self.tnext
        self.display_logs = display_logs
        
    def simulate(self, time):
        self.time_modeling = time
        while self.tcurr < self.time_modeling:
            self.tnext = np.inf

            for element in self.elements:
                tnext_min = np.min(element.tnexts) # Найменше значення моменту часу з усіх елементів
                if tnext_min < self.tnext and not isinstance(element, Despose):
                    self.tnext = tnext_min
                    self.event = element
            
            for element in self.elements:
                element.do_statistics(self.tnext - self.tcurr) # вираховуємо статистики
                
            # Переміщення до операції завершення
            self.tcurr = self.tnext
            for element in self.elements:
                element.tcurr = self.tcurr
            
            self.event.out_act() # Операція завершення (вихід з елементу)

            for element in self.elements:
                if self.tcurr in element.tnexts:
                    element.out_act()

        return self.print_statistic()
        
    def print_info(self):
        for element in self.elements:
            element.print_info()
            
    def print_statistic(self):
        n_processors = 0
        global_mean_load_accumulator = 0
        global_max_queue = 0
        global_mean_queue_accumulator = 0
        global_failure_accumulator = 0
        global_max_load = 0

        if self.display_logs:
            print('-----RESULT-----')
        
        for e in self.elements:
            if self.display_logs:
                e.print_statistic() 
            if isinstance(e, Process):
                n_processors += 1
                mean_queue = e.mean_queue / self.tcurr
                failure = e.failure / (e.quantity + e.failure) if (e.quantity + e.failure) != 0 else 0
                mean_load = e.quantity / self.time_modeling
                
                global_mean_queue_accumulator += mean_queue
                global_failure_accumulator += failure
                global_mean_load_accumulator += mean_load
                
                if e.max_queue_length > global_max_queue:
                    global_max_queue = e.max_queue_length
                    
                if mean_load > global_max_load:
                    global_max_load = mean_load
                
                if self.display_logs:
                    print(f"Average queue length: {mean_queue}")
                    print(f"Failure probability: {failure}")
                    print(f"Average load: {mean_load}\n")
                
        global_mean_queue = global_mean_queue_accumulator / n_processors
        global_failure = global_failure_accumulator / n_processors
        global_mean_load = global_mean_load_accumulator / n_processors
        
        if self.display_logs:
            print(f"Global max load: {global_max_load}")
            print(f"Average Global Loading: {global_mean_load}")
            print(f"Global mean queue length: {global_mean_queue}")
            print(f"Global failure probability: {global_failure}")
            print(f"Global max observed queue length: {global_max_queue}\n")
        
        return self.elements[0].quantity
