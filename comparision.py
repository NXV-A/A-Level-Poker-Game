import json

deck = json.loads(open("deck.txt", "r").read())
cards = ['8 of Diamonds', 'Queen of Diamonds', 'Jack of Diamonds', '9 of Diamonds', '10 of Diamonds']
textnames = {
    14 : 'Ace',
    13 : 'King',
    12 : 'Queen',
    11 : 'Jack'
    }


# 10 hand types

def sortRules(x):
    return deck[x][0]


def checkDsc(array, limit, start=0):
    lastNum = deck[array[start]][0]
    valid = 'True'
    for i in range(start, limit):
        if not deck[array[i]][0] + 1 == lastNum and not i == 0:
            valid = 'False'
        else:
            lastNum = deck[array[i]][0]
    return valid

def handValue(cards):
    sortedHand = {
        'Hearts' : [],
        'Diamonds' : [],
        'Spades' : [],
        'Clubs' : [],
        'ordGeneral' : []
    }
    
    hand = []
    
    for card in cards:
        suit = deck[card][1]
        sortedHand[suit].append(card)
        sortedHand['ordGeneral'].append(card)
        
    for group in sortedHand:
        sortedHand[group].sort(key=sortRules, reverse=True)
        
    for group in sortedHand:
        if not group == 'ordGeneral' and len(sortedHand[group]) >= 5:
            if checkDsc(sortedHand[group], 5):
                cardValue = deck[sortedHand[group][0]][0]
                if cardValue >= 11:
                    cardName = textnames[cardValue]
                else:
                    cardName = cardValue
                name = cardName + " high straight flush"
                value = cardValue + 140
                hand = [name, value]
    return hand
print(handValue(cards))
