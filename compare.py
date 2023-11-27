from functools import lru_cache


def sortRule(x):
    return x.value

def concatenateInts(a, b):
    return a*100 + b


def getValueOfHand(parent, hand):
    
    # hand value = 01-10 + 01-13 e.g. 0510 = jack high straight
    
    hand.sort(key=sortRule)
    concurrent = 0
    straight = 0
    suitCount = [0, 0, 0, 0]
    pairCount = [0, 0, 0] # pair, three, four
    suits = parent.deck.suits
    prevCard = None
    names = ['Pair', 'Three of a kind', 'Four of a kind']
    hands = []
    hasStraight = False
    hasFlush = False
    highestStraightCard = None
    highestPairCard = None
    for i in range(len(hand)):
        if not i == 0:
            
            # check for pair, two pair, three of a kind, and four of a kind
            if prevCard.value == hand[i].getValue():
                concurrent += 1
                
            if concurrent >= 1 and not prevCard.getValue() == hand[i].getValue():
                pairCount[concurrent - 1] += 1
                concurrent = 0
                highestPairCard = prevCard
            elif not prevCard.getValue() == hand[i].getValue():
                concurrent = 0
            
            # check for straight - 05
            if prevCard.getValue() + 1 == hand[i].getValue():
                straight += 1
                
            if straight >= 4 and not prevCard.getValue() + 1 == hand[i].getValue():
                highestStraightCard = prevCard
                hasStraight = False
                straight = 0
            elif not prevCard.getValue() + 1 == hand[i].getValue():
                straight = 0
    
        prevCard = hand[i]
        
        #check for flush
        suitCount[suits.index(hand[i].getSuit())] += 1
    
    # get high card - 01
    highCard = hand[len(hand) - 1]
    value = concatenateInts(1, highCard.getValue())
    hands.append(value)
#     print(highCard.getValueName(), 'high')
    
    # print pairs - 02, 03, 04, 08
    for i in range(len(pairCount)):
        if i == 0:
            if pairCount[i] == 1:
                value = concatenateInts(2, highestPairCard.getValue())
                hands.append(value)
#                 print("Pair of " + highestPairCard.getValueName() + "'s")
            elif pairCount[i] == 2:
                value = concatenateInts(3, highestPairCard.getValue())
                hands.append(value)
#                 print("Two Pair " + highestPairCard.getValueName() + "'s")
        elif i == 1:
            if pairCount[i] == 1:
                value = concatenateInts(4, highestPairCard.getValue())
                hands.append(value)
#                 print("Three of a kind " + highestPairCard.getValueName() + "'s")
        elif i == 2:
            if pairCount[i] == 1:
                value = concatenateInts(8, highestPairCard.getValue())
                hands.append(value)
#                 print("Four of a kind " + highestPairCard.getValueName() + "'s")
    
    # check for full house - 07
    if pairCount[0] >= 1 and pairCount[1] >= 1:
        value = concatenateInts(7, highestPairCard.getValue())
        hands.append(value)
#         print("Full house " + highestPairCard.getValueName() + " high")
        
    # print flush - 06
    for i in range(len(suitCount)):
        if suitCount[i] >= 5:
            for i in hand:
                if i.getSuit() == suit[i]:
                    bestCard = i
            value = concatenateInts(6, bestCard.getValue())
            hands.append(value)
            hasFlush = True
#             print(suit[i] ,'Flush')


    if hasStraight:
        if hasFlush:
            value = concatenateInts(9, highestStraightCard.getValue())
            hands.append(value)
#           print(highestStraightCard.getValueName(), 'Flush High Straight')
        else:
            value = concatenateInts(5, highestStraightCard.getValue())
            hands.append(value)
#           print(highestStraightCard.getValueName(), 'High Straight')
            
    return max(hands)

def valueToName(parent, value):
    hands = {
        1 : "? High",
        2 : "Pair of ?'s",
        3 : "Two Pair ?'s",
        4 : "Three of a Kind",
        5 : "? High Straight",
        6 : "? High Flush",
        7 : "Full House",
        8 : "Four of a Kind",
        9 : "? High Straight Flush",
    }
    
    cardNames = parent.deck.deck[0].values
    
    handNumber, cardName = int(str(value)[:1]), cardNames[int(str(value)[1:])]
    
    if value != 913:
        handName = hands[handNumber].replace("?", cardName)
    else:
        handName = "Royal Flush"
    
    return handName
    
    

    