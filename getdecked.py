values = {
    1 : "2",
    2 : "3",
    3 : "4",
    4 : "5",
    5 : "6",
    6 : "7",
    7 : "8",
    8 : "9",
    9 : "10",
    10 : "Jack",
    11 : "Queen",
    12 : "King",
    13 : "Ace"
}

suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.name = values[self.value] + " of " + self.suit

def getDeck():
    deck = []        
    for suit in suits:
        for value in range(1, 14):
            deck.append(Card(suit, value))
    return deck
        
