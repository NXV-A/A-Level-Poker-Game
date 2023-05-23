if __name__ == "__main__":
    import testingham as main
    
    d = main.Deck()
    p = main.Player()
    
    for i in range(7):
        p.hand.append(d.getCard())
        
        
def sortRule(x):
    return x.value

p.hand.sort(key=sortRule)

for i in p.hand:
    print(i.name)

def pairCheck(hand):
    concurrent = 0
    prev = 0
    names = ['Pair', 'Two Pair', 'Three', 'Four']
    for i in range(len(p.hand)):
        if not i == 0:
            if prev == p.hand[i].value:
                concurrent += 1
                print('pair')
            else:
                concurrent = 0
        if concurrent > prev:
            pass
        prev = p.hand[i].value
            
                
pairCheck(p.hand)