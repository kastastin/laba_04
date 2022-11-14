import numpy as np
from Element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def out_act(self):
        super().out_act() # Збільшення лічильника кількості (quantity++)
        self.tnexts[0] = self.tcurr + super().get_delay() # Записуємо вільний пристрій
        next_element = np.random.choice(self.next_elements, p=self.p) # Передаємо наступним елементам
        next_element.in_act() # Вхід в наступний елемент
