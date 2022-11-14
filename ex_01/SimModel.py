import sys
sys.path.append('../laba_04')
from Element import Element
from Create import Create
from Process import Process
from Despose import Despose
from Model import Model


class SimModel():
    def __init__(self):
        c = Create(delay_mean = 0.89, name = 'CREATOR', distribution = 'exp')
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

        model = Model(elements, display_logs = True)
        model.simulate(10000)

Element.id = 0
s = SimModel()
