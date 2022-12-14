import json

deck = {}
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
types = ['Jack', 'Queen', 'King', 'Ace']

for suit in suits:
    for i in range(13):
        value = i + 2
        data = [value, suit]
        if not value > 10:
            card = str(value) + " of " + suit
            deck[card] = data
        else:
            card = types[value - 11] + " of " + suit
            deck[card] = data
        
f = open("deck.txt", "w")
f.write(json.dumps(deck))
f.close()

