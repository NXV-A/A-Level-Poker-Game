import json

deck = json.loads(open("deck.txt", "r").read())
cards = ['10 of Hearts', '6 of Hearts', '6 of Diamonds', '5 of Hearts', '4 of Hearts', '2 of Diamonds', '2 of Hearts']

textnames = {
    14 : 'Ace',
    13 : 'King',
    12 : 'Queen',
    11 : 'Jack'
}

handnames = {
    2 : ' Pair',
    3 : ' Three Of A Kind',
    4 : ' Four Of A Kind',
    
}


# 10 hand types

def sortRule1(x):
    return deck[x][0]


def sortRule2(x):
    if not x:
        return 0
    else:
        return x[1]


def getCardName(value):
    if value >= 11:
        cardName = textnames[value]
    else:
        cardName = str(value)
    return cardName


def getHigh(value):
    return getCardName(value) + " High"


def checkDsc(array, limit):
    limit -= 1
    lastNum = deck[array[0]][0]
    for i in range(len(array)):
        value = deck[array[i]][0]
        if value + 1 == lastNum and not i == 0:
            if streak == 0:
                streak += 1
        else:
            streak = 0
        if streak == limit:
            return True, lastNum
        lastNum = value
    return False


def checkAlike(array, cards):
    previousCard = 0
    streak = 0
    for i in range(len(array)):
        value = deck[array[i]][0]
        if value == previousCard and not i == 0:
            streak += 1
            if streak == cards - 1:
                return True, previousCard
        else:
            streak = 0
        previousCard = value
    return False, previousCard


def sortCards(cards):
    sortedHand = {
        'Hearts' : [],
        'Diamonds' : [],
        'Spades' : [],
        'Clubs' : [],
        'ordGeneral' : []
    }
    for card in cards:
        suit = deck[card][1]
        sortedHand[suit].append(card)
        sortedHand['ordGeneral'].append(card)  
    for group in sortedHand:
        sortedHand[group].sort(key=sortRule1, reverse=True)
    return sortedHand


def flushCheck(cards):
    name = ''
    value = 0
    for group in cards:
        if not group == 'ordGeneral' and len(cards[group]) >= 5:
            cardValue = deck[cards[group][0]][0]
            print(checkDsc(cards[group], 5))
            if checkDsc(cards[group], 5):
                name = getHigh(checkDsc(cards[group], 5)) + " straight flush"
                value = cardValue + 140
            else:
                name = getHigh(cardValue) + " flush"
            value = cardValue + 84
    if value > 0:
        return [name, value]
    else:
        return False


def pairCheck(cards):
    pass
#     sort = {}
#     for i in cards['ordGeneral']:
#         value = deck[i][0]
#         print(sort[value])
#             
#     print(sort)


# def pairCheck(cards):
#     multiplier = 8
#     for pairs in range(4, 1, -1):
#         result = checkAlike(cards['ordGeneral'], pairs)
#         if result[0]:
#             name = getHigh(result[1]) + handnames[pairs]
#             value = result[1] + (int(14 * multiplier) - 1)
#             return [name, value]
#         multiplier = multiplier / 2
#     return False


def straightCheck(cards):
    if checkDsc(cards['ordGeneral'], 5):
        name = getHigh(deck[cards['ordGeneral'][0]][0]) + " straight"
        value = deck[cards['ordGeneral'][0]][0] + 56
        return [name, value]
    return False

    
def returnHighest(array):
    array.sort(key=sortRule2, reverse=True)
    return array[0]


def handValue(cards):
    hand = []
    
    # Sort the cards
    sortedHand = sortCards(cards)
    
    # Check for straight flush and flush
    hand.append(flushCheck(sortedHand))
    
    # Check for pairs etc
    hand.append(pairCheck(sortedHand))
        
    # Check for straight
    hand.append(straightCheck(sortedHand))
        
    # Check for high card
    value = deck[sortedHand['ordGeneral'][0]][0]
    hand.append([getHigh(value), value])
    
    print(hand)
    
    return returnHighest(hand)

print(handValue(cards))