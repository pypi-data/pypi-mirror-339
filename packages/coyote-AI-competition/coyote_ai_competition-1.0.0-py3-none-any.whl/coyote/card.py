import random

class Card:
    def __init__(self, value):
        self.value = value

    def cardnumber_show(self):
       return self.value
'''        
class Deck:
    def __init__(self):
        cards =[100, 101, 102, 103, -10, -5, -5, 0, 0, 0, 
        1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
         5, 5, 5, 5, 10, 10, 10, 15, 15, 20]
         #100:? 101:max->0 102:0(黒) 103:x2
        self.cards = [Card(value) for value in cards]
        random.shuffle(self.cards)
    
    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop().value
        return None'
'''