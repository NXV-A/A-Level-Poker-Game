import socket, sys, json, time, random, threading, pygame, base64, queue, assetloader, compare

packetID = {
    '0' : 'Connect',
    '1' : 'Disconnect',
    '2' : 'Player Data',
    '3' : 'New Game',
    '4' : 'Picture',
    '5' : 'Id',
    '6' : 'Loaded',
    '7' : 'Message',
    '8' : 'Start Game',
    '9' : 'Turn',
    '10' : 'Bet',
    '11' : 'Fold',
    '1000' : 'Ping',
}

botNames = ('John', 'Greg', 'Barbara', 'Joe', 'Bahn', 'Kallum', 'Jorge', 'Lukas', 'Jim', 'Red Chief', 'Sachet', 'Graham', 'Margaret', 'Agatha', 'Helena', 'Christine', 'Jenny')

winningPercentages = {
    13 : {
        13 : 0.85,
        12 : 0.68,
        11 : 0.67,
        10 : 0.66,
        9 : 0.66,
        8 : 0.64,
        7 : 0.63,
        6 : 0.63,
        5 : 0.62,
        4 : 0.62,
        3 : 0.61,
        2 : 0.60,
        1 : 0.59,
    },
    12 : {
        13 : 0.66,
        12 : 0.83,
        11 : 0.64,
        10 : 0.64,
        9 : 0.63,
        8 : 0.61,
        7 : 0.60,
        6 : 0.59,
        5 : 0.58,
        4 : 0.58,
        3 : 0.57,
        2 : 0.56,
        1 : 0.55,
    },
    11 : {
        13 : 0.65,
        12 : 0.62,
        11 : 0.80,
        10 : 0.61,
        9 : 0.61,
        8 : 0.59,
        7 : 0.58,
        6 : 0.56,
        5 : 0.55,
        4 : 0.55,
        3 : 0.54,
        2 : 0.53,
        1 : 0.52,
    },
    10 : {
        13 : 0.65,
        12 : 0.62,
        11 : 0.59,
        10 : 0.78,
        9 : 0.59,
        8 : 0.57,
        7 : 0.56,
        6 : 0.54,
        5 : 0.53,
        4 : 0.52,
        3 : 0.51,
        2 : 0.50,
        1 : 0.50,
    },
    9 : {
        13 : 0.64,
        12 : 0.61,
        11 : 0.59,
        10 : 0.57,
        9 : 0.75,
        8 : 0.56,
        7 : 0.54,
        6 : 0.53,
        5 : 0.51,
        4 : 0.49,
        3 : 0.49,
        2 : 0.48,
        1 : 0.47,
    },
    8 : {
        13 : 0.62,
        12 : 0.59,
        11 : 0.57,
        10 : 0.55,
        9 : 0.53,
        8 : 0.72,
        7 : 0.53,
        6 : 0.51,
        5 : 0.50,
        4 : 0.48,
        3 : 0.46,
        2 : 0.46,
        1 : 0.45,
    },
    7 : {
        13 : 0.61,
        12 : 0.58,
        11 : 0.55,
        10 : 0.53,
        9 : 0.52,
        8 : 0.50,
        7 : 0.69,
        6 : 0.50,
        5 : 0.49,
        4 : 0.47,
        3 : 0.45,
        2 : 0.43,
        1 : 0.43,
    },
    6 : {
        13 : 0.60,
        12 : 0.57,
        11 : 0.54,
        10 : 0.52,
        9 : 0.50,
        8 : 0.48,
        7 : 0.47,
        6 : 0.67,
        5 : 0.48,
        4 : 0.46,
        3 : 0.45,
        2 : 0.43,
        1 : 0.41,
    },
    5 : {
        13 : 0.59,
        12 : 0.56,
        11 : 0.53,
        10 : 0.50,
        9 : 0.48,
        8 : 0.47,
        7 : 0.46,
        6 : 0.45,
        5 : 0.64,
        4 : 0.46,
        3 : 0.44,
        2 : 0.42,
        1 : 0.40,
    },
    4 : {
        13 : 0.60,
        12 : 0.55,
        11 : 0.52,
        10 : 0.49,
        9 : 0.47,
        8 : 0.45,
        7 : 0.44,
        6 : 0.43,
        5 : 0.43,
        4 : 0.61,
        3 : 0.44,
        2 : 0.43,
        1 : 0.41,
    },
    3 : {
        13 : 0.59,
        12 : 0.54,
        11 : 0.51,
        10 : 0.48,
        9 : 0.46,
        8 : 0.43,
        7 : 0.42,
        6 : 0.41,
        5 : 0.41,
        4 : 0.41,
        3 : 0.58,
        2 : 0.43,
        1 : 0.40,
    },
    2 : {
        13 : 0.58,
        12 : 0.54,
        11 : 0.50,
        10 : 0.48,
        9 : 0.45,
        8 : 0.43,
        7 : 0.40,
        6 : 0.39,
        5 : 0.39,
        4 : 0.39,
        3 : 0.38,
        2 : 0.55,
        1 : 0.39,
    },
    1 : {
        13 : 0.57,
        12 : 0.53,
        11 : 0.49,
        10 : 0.47,
        9 : 0.44,
        8 : 0.42,
        7 : 0.40,
        6 : 0.37,
        5 : 0.37,
        4 : 0.37,
        3 : 0.36,
        2 : 0.35,
        1 : 0.51,
    },
}

Id = 0

botImage = None
# with open('./Assets/Default Pfp/John.png', 'rb') as f:
#     botImage = base64.b64encode(f.read())

def getBotName():
    return random.choice(botNames)

botImages = {}
for name in botNames:
    with open('./Assets/Default Pfp/' + name + '.png', 'rb') as f:
        image = base64.b64encode(f.read())
    botImages[name] = image
        
    


#change port back to 6778

class Server():
    def __init__(self, game=None, port=27015, maxClients=5, isInternal=False):
        self.hostname = socket.gethostname()
        self.globalIp = socket.gethostbyname(self.hostname)
        if isInternal:
            self.acceptedIp = "127.0.0.1"
        else:
            self.acceptedIp = "0.0.0.0"
        self.port = port
        self.maxClients = maxClients
        self.clients = []
        self.waitingRoom = []
        self.currentPlayer = None
        self.startDelay = 10
        self.gameStarted = False
        self.isInternal = isInternal
        self.game = game

        self.gameNumber = 0
        self.playerNumber = 0
        self.communityCards = []
        self.pot = [0, 0, 0, 0, 0]
        self.lastbet = 0
        self.currentPlayer = None
        self.currentDealer = 0
        self.turnWait = 20.0
        
        self.stopping = threading.Event()


        self.deck = Deck()
        self.timer = None

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.settimeout(1)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.acceptedIp, int(self.port)))
        except socket.error as e:
            print('Error at server binding:', e)
        
        self.server.listen(self.maxClients + (self.maxClients - 1))
        print('The bluetooth device is-uh ready to pair.')

        threading.Thread(target=self.serverLoop, args=(), daemon=True).start()

    def recievingImages(self, client):
        try:
            data = b''
            while not self.stopping.is_set():
                try:
                    recv = client.recv(4096)
                    data += recv
                    if not recv:
                        break
                    elif recv[-1:] == b'\x1e':
                        data = data[:-1]
                        break
                except Exception as e:
                    print('Error when recieving an image:', e)
            return data
        except:
            print('sexing hell')

    def sendingImages(self, player):
        try:
            allClients = self.clients + self.waitingRoom
            for client in allClients:
                if (not client.isBot()) and client != player:
                    client.addToQueue((b'4|'+ str(player.id).encode() + b'|' + player.pfp + b'\x1e'))
        except:
            print('fucking hell')

    def sendAllImages(self, player):
        try:
            allClients = self.clients + self.waitingRoom
            for client in allClients:
                if client != player:
                    player.addToQueue((b'4|'+ str(client.id).encode() + b'|' + client.pfp + b'\x1e'))
        except:
            print('shitting hell')

    def startGame(self):
        self.serverStartTime = time.time()

        time.sleep(self.startDelay)
        self.gameStarted = True

        self.startOfNewRound()

    def networkLoop(self):
        while not self.stopping.is_set():
            for client in self.clients + self.waitingRoom:
                if not client.isBot() and client.connected:
                    try: 
                        if client.queue.qsize() > 0:
                            jargon = client.queue.get()
                            client.connection.sendall(jargon)
                    except:
                        pass
                    data = self.recieveData(client.connection, load=False)
                    packetId = ''
                    while len(data) > 0 and data[0].isnumeric():
                        packetId += data[0]
                        data = data[1:]
                    if packetId == '':
                        packetId = '1000'
                    match packetID[packetId]: 
                        case "Disconnect":
                            client.connected = False
                            self.players -= 1
                            if client in self.waitingRoom:
                                self.waitingRoom.remove(client)
                            else:
                                botName = getBotName()
                                bot = ServerBot(username='Bot ' + botName, pfp=botImages[botName], server=self)
                                if self.gameStarted:
                                    client.folded = True
                                    client.lastAction = 'Folded'
                                    bot.fold()
                                    bot.id = client.id
                                    bot.hand = [Card(suit='Spades', value=1)] * 2
                                    # bot.money = [10, 5, 3, 2, 1]
                                    bot.lastAction = 'Sat Out'
                                self.clients[self.clients.index(client)] = bot
                                if self.gameStarted and self.currentPlayer and self.currentPlayer.id == client.id:
                                    self.endGo()
                            client.connection.close()
                            if self.players <= 0:
                                self.close()
                        case "Loaded":
                            if self.gameStarted:
                                client.isLoaded = True
                        case "Fold":
                            if self.gameStarted:
                                if self.currentPlayer.id == client.id:
                                    client.fold()
                                    client.lastAction = 'Folded'
                                    self.endGo()
                        case "Bet":
                            money = json.loads(data)[0]
                            if self.gameStarted:
                                if self.currentPlayer.id == client.id:
                                    if self.lastbet < money:
                                        client.betting = money
                                        client.lastAction = 'Raise: ' + str(money)
                                        self.endGo()
                                    elif self.lastbet == money:
                                        client.lastAction = 'Call: ' + str(money)
                                        client.betting = money
                                        self.endGo()
                                    elif client.money == self.lastbet and self.lastbet == money:
                                        client.lastAction = 'All in'
                                        client.betting = client.money
                                        self.endGo()
                        case "Message":
                            for c in self.clients:
                                if not c.isBot(): # client.id != c.id and
                                    c.addToQueue(b'7' + bytes(data, 'utf-8') + b'\x1e')
                        case _:
                            pass

    def serverLoop(self):
        self.bots = 0
        self.players = 0

        for i in range(self.maxClients):
            botName = getBotName()
            self.clients.append(ServerBot(username='Bot ' + botName, pfp=botImages[botName], server=self))
            self.bots += 1
        # try:
        threading.Thread(target=self.networkLoop, args=(), daemon=True).start()
        if not self.isInternal:

            while not self.stopping.is_set():
                try:
                    connection, address = self.server.accept()
                    connection.settimeout(1)
                    playerInfo = self.recieveData(connection)
                    playerImage = self.recievingImages(connection)
                    print('The bluetooth device is a connected-uh successfulay to:', address)
                    if not self.gameStarted:
                        client = ServerClient(connection, address[0], username=playerInfo['Name'], pfp=playerImage)
                        self.clients[self.players] = client
                        self.players += 1
                        self.bots -= 1
                        self.send(client, '5' + json.dumps([client.id]))
                        if client.isHost():
                            threading.Thread(target=self.startGame, args=(), daemon=True).start()

                        self.sendingImages(client)
                        self.sendAllImages(client)
                    elif len(self.waitingRoom) <= self.bots:
                        self.waitingRoom.append(ServerClient(connection, address[0], username=playerInfo['Name'], pfp=playerImage))
                    else:
                        connection.close()
                except Exception as e:
                    print('cunt', e)
        else:
            connection, address = self.server.accept()
            connection.settimeout(1)
            playerInfo = self.recieveData(connection)
            playerImage = self.recievingImages(connection)
            print('The bluetooth device is a connected-uh successfulay to:', address)
            client = ServerClient(connection, address[0], username=playerInfo['Name'], pfp=playerImage)
            self.clients[self.players] = client
            self.players += 1
            self.bots -= 1
            self.send(client, '5' + json.dumps([client.id]))
            threading.Thread(target=self.startGame, args=(), daemon=True).start()
            self.sendingImages(client)
            self.sendAllImages(client)
        # except KeyboardInterrupt:
            #self.close()
            
        # except Exception as Error:
           # print("the uhh bluethooth device fucked itself??", Error)

    def serialiseClients(self):
        data = []

        for client in self.clients:
            data.append({
                'Role' : client.role,
                'Host' : client.host,
                'Bot' : client.bot,
                'Turn' : client.turn,
                'Name' : client.username,
                'Money' : client.money,
                'Id' : client.id,
                'Folded' : client.folded,
                'Last Action' : client.lastAction,
            })

        return data

    def sendAllClients(self, data):
        try:
            allClients = self.clients + self.waitingRoom
            for client in allClients:
                if not client.isBot():
                    client.addToQueue((data + '\x1e').encode())
        except:
            print('mating hell')

    def recieveData(self, connection, load=True):
        data = ''
        while not self.stopping.is_set():
            try:
                recv = connection.recv(4096)
                data += recv.decode()
                if not recv:
                    break
                elif recv[-1:] == b'\x1e':
                    data = data[:-1]
                    break
            except Exception as e:
                print('General recieving error:', e)
                break
        if load:
            print(data)
            try:
                return json.loads(data)
            except:
                return ''
        else:
            return data
    
# game logic/functionality

    def startOfNewRound(self):

        self.gameNumber += 1
        self.playerNumber = self.currentDealer
        self.lastbet = 0
        self.communityCards = []

        for idx, client in enumerate(self.clients):
            if client.isBot() and len(self.waitingRoom) > 0:
                self.clients[idx] = self.waitingRoom.pop(0)

        for client in self.clients:
            client.setPlayingStatus(True)
            client.setRole('Player')
            client.lastbet = 0
            client.handValue = 0
            client.folded = False
            client.hand = []
            client.lastAction = ''
            client.betting = 0
            client.turn = False
            if not client.isBot():
                client.isLoaded = False
        self.clients[(self.playerNumber) % len(self.clients)].setRole('Dealer')
        self.clients[(self.playerNumber + 1) % len(self.clients)].setRole('Little Blind')
        self.clients[(self.playerNumber + 1) % len(self.clients)].betting = 1
        self.clients[(self.playerNumber + 1) % len(self.clients)].lastbet = 1
        self.lastbet = 1
        betAmount = self.clients[(self.playerNumber + 1) % len(self.clients)].bet(self.lastbet)
        self.addChipsToPot(betAmount)
        self.clients[(self.playerNumber + 2) % len(self.clients)].setRole('Big Blind')
        self.clients[(self.playerNumber + 2) % len(self.clients)].betting = 2
        betAmount = self.clients[(self.playerNumber + 2) % len(self.clients)].bet(self.lastbet)
        self.clients[(self.playerNumber + 2) % len(self.clients)].lastbet = 2
        self.lastbet = 2
        self.addChipsToPot(betAmount)
        whoBet = (self.playerNumber + 2) % len(self.clients)#
        basebetNumber = self.lastbet

        self.playerNumber = (self.playerNumber + 3) % len(self.clients)

        self.deck.regenDeck()

        for client in self.clients:
            client.hand = [self.deck.getCard(), self.deck.getCard()]
            
        self.updatePlayers()

        self.sendAllClients("3[]")
        
        self.waitForPlayers()
        self.sendAllClients('8' + json.dumps({
            'Start Time' : time.time()
        }))
        # pre flop, flop, the turn, the river, the showdown
        endGame = False
        for i in range(5):
            if endGame:
                break
            for i in range(len(self.clients)):
                print('Next Go')
                self.currentPlayer = self.clients[self.playerNumber]
                self.updatePlayers()
                if not self.currentPlayer.folded:
                    self.timer = threading.Timer(self.turnWait, self.endGo, args=(True,))
                    self.timer.start()
                    self.currentPlayer.promptAction()
                    self.timer.join()

                print('testing data:', self.currentPlayer.lastbet, basebetNumber, self.currentPlayer.folded, whoBet)
                self.playerNumber = (self.playerNumber + 1) % len(self.clients)
                foldCount = 0
                for player in self.clients:
                    if player.folded:
                        foldCount += 1
            for player in self.clients:
                player.lastbet = 0
            self.lastbet = 0
            print('mate')
            self.showCommunityCards()
        winners = self.returnWinners()
        self.rewardPlayers(winners)
        self.pot = [0, 0, 0, 0, 0]
        time.sleep(5)
        self.currentDealer += 1
        self.startOfNewRound()

    def rewardPlayers(self, winners):
        potMoney = self.calculatePot()
        reward = potMoney // len(winners)
        for winner in winners:
            winner.addChips(reward)
            winner.lastAction = 'Won: ' + str(reward) + ' with ' + compare.valueToName(winner.handValue)

    def calculatePot(self):
        value = 1
        totalMoney = 0
        for i in self.pot:
            amount = value * i
            totalMoney += amount
            value *= 2
        return totalMoney


    def returnWinners(self):
        for player in self.clients:
            if not player.folded:
                player.handValue = compare.getValueOfHand(player.hand + self.communityCards)
            else:
                player.handValue = 0
        maxHandValue = max(self.clients, key=lambda c: c.handValue).handValue
        print('best hand ever', maxHandValue)
        winners = list(filter(lambda c: c.handValue >= maxHandValue and not c.folded, self.clients))
        print('these people have won', winners)
        return winners


    def updatePlayers(self):
        clientData = self.serialiseClients()
        for client in self.clients:
            self.send(client, '2' + json.dumps({
                'Hand' : [{
                    'suit' : client.hand[0].suit,
                    'value' : client.hand[0].value,
                },
                {
                    'suit' : client.hand[1].suit,
                    'value' : client.hand[1].value,
                }],
                'Money' : client.money,
                'Role' : client.role,
                'Pot' : self.pot,
                'Players' : clientData,
                'Community Cards' : self.serialiseCommunityCards(),
                'Last Bet' : self.lastbet,
                'Current Player' : (self.currentPlayer and {
                        'Name' : self.currentPlayer.getUsername(),
                        'Id' : self.currentPlayer.id,
                    }) or False,
            }))

    def serialiseCommunityCards(self):
        serialisedCards = []
        for card in self.communityCards:
            cardData = {
                'suit' : card.suit,
                'value' : card.value,
            }
            serialisedCards.append(cardData)
        return serialisedCards

    
    def endGo(self, outOfTime=False):
        if self.timer:
            self.timer.cancel()
        if outOfTime:
            self.currentPlayer.fold()
        elif not self.currentPlayer.folded:
            lastbet = self.currentPlayer.betting
            chipsToPot = self.currentPlayer.bet(self.lastbet)
            self.currentPlayer.lastbet = lastbet
            self.lastbet = lastbet
            print(chipsToPot)
            self.addChipsToPot(chipsToPot)

        self.updatePlayers()
        
    def addChipsToPot(self, arrChips):
        for idx, val in enumerate(arrChips):
            print(val)
            self.pot[idx] += val

    def waitForPlayers(self):
        for client in self.clients:
            if not client.isBot():
                while not client.isLoaded:
                    pass

    def send(self, client, data):
        try:
            if not client.isBot():
                client.addToQueue((data + '\x1e').encode())
        except Exception as e:
            print(e)

    def finishGo(self):
        self.playerNumber = (self.playerNumber + 1) % len(self.clients)
        self.currentPlayer = self.clients[self.playerNumber]
        if not self.currentPlayer.folded:
            self.currentPlayer.promptAction()
        else:
            self.finishGo(self)

    def showCommunityCards(self):
        if len(self.communityCards) == 0:
            for i in range(3):
                self.communityCards.append(self.deck.getCard())
        elif len(self.communityCards) == 3:
            self.communityCards.append(self.deck.getCard())
        elif len(self.communityCards) == 4:
            self.communityCards.append(self.deck.getCard())
        else:
            print('Unable to show more community cards')
        print(self.communityCards)

    def close(self):
        for client in self.clients + self.waitingRoom:
            if not client.isBot():
                client.connection.close()
        self.stopping.set()

class ServerBot():
    def __init__(self, username='Bot', pfp=None, server=None):
        global Id
        self.isPlaying = False
        self.role = 'Player'
        self.host = False
        self.bot = True
        self.turn = False
        self.pfp = pfp
        self.username = username
        self.money = [10, 5, 3, 2, 1]
        self.hand = None
        self.picture = None
        self.betting = 0
        self.overallMoney = self.calculateMoney()
        self.folded = False
        self.id = str(Id)
        self.lastbet = 0
        self.server = server
        self.handValue = 0
        self.lastAction = ''
        Id += 1

        self.botConfidence = random.randint(20, 90)/100
        

    def isHost(self):
        return self.host
    
    def setPlayingStatus(self, status):
        self.isPlaying = status

    def setRole(self, role):
        self.role = role

    def isBot(self):
        return self.bot
    
    def setTurn(self, value):
        self.turn = value

    def getTurn(self):
        return self.turn
    
    def promptAction(self):
        # time.sleep(random.randint(2, 10))
        self.folded = False
        moneyRatio = 1.5 * self.calculateMoney()/64
        bettingWinChance = winningPercentages[self.hand[0].value][self.hand[1].value] / self.botConfidence * moneyRatio
        print(bettingWinChance)

        if len(self.server.communityCards) < 3:
            if random.random() < bettingWinChance:
                if bettingWinChance < random.randint(80 - round(5 * self.botConfidence), 80 + round(5 * self.botConfidence))/100:
                    print(round(5 * moneyRatio * self.botConfidence))
                    self.betting = self.server.lastbet + random.randint(1, round(5 * moneyRatio * self.botConfidence))
                    print(self.username, 'i am betting this')
                else:
                    self.betting = self.server.lastbet
                    print(self.username, 'i am betting this')
            else:
                self.fold()
                print(self.username, 'i fold')
        else:
            handValueWinning = compare.getValueOfHand(self.hand + self.server.communityCards)/100 / self.botConfidence + bettingWinChance
            if random.random() < handValueWinning:
                if handValueWinning > random.randint(80 - round(5 * self.botConfidence), 80 + round(5 * self.botConfidence))/100:
                    self.betting = self.server.lastbet + 1
                    print(self.username, 'i am betting this')
                else:
                    self.betting = self.server.lastbet
                    print(self.username, 'i am betting this')
            else:
                self.fold()
                print(self.username, 'i fold')
        self.server.endGo()      

    def fold(self):
        self.lastAction = 'Folded'
        self.folded = True

    
    def setGame(self, game):
        self.currentGame = game

    def getUsername(self):
        return self.username
    
    def getHand(self):
        return self.hand
    
    def getRole(self):
        return self.role
    
    def getMoney(self):
        return self.money
    
    def bet(self, lastbet):
        chipsAdded = [0, 0, 0, 0, 0]
        values = [1, 2, 4, 8, 16]
        if lastbet < self.betting:
            self.lastAction = 'Raise: ' + str(self.betting) 
        elif lastbet == self.betting:
            self.lastAction = 'Call: ' + str(self.betting) 
        elif self.betting == self.overallMoney:
            self.lastAction = 'All in'
        elif self.betting == 0:
            self.lastAction = 'Check'
        if not self.betting == 0:
            for i in range(4, -1, -1):
                print(self.betting, values[i])
                if self.betting >= values[i] and self.money[i]:
                    amountOfTimes = self.betting // values[i]
                    if amountOfTimes <= self.money[i]:
                        chipsAdded[i] += amountOfTimes
                        self.betting -= amountOfTimes * values[i]
                    else:
                        chipsAdded[i] = self.money[i]
                        self.betting -= self.money[i] * values[i]
        elif self.betting == 0:
            self.betting = 0
            print(chipsAdded)
        self.minusChips(chipsAdded)
        return chipsAdded
    
    def minusChips(self, arrayChips):
        for index in range(len(self.money)):
            self.money[index] -= arrayChips[index] 

    def addChips(self, money):
        values = [1, 2, 4, 8, 16]
        if not money == 0:
            for i in range(4, -1, -1):
                if money >= values[i]:
                    amountOfTimes = money // values[i]
                    if amountOfTimes > 5 and values[i] > 4:
                        amountOfTimes = min([amountOfTimes, 5])
                    self.money[i] += amountOfTimes
                    money -= amountOfTimes * values[i]
            

    def calculateMoney(self):
        value = 1
        money = 0
        for i in self.money:
            amount = value * i
            money += amount
            value *= 2
        self.overallMoney = money
        return money

class ServerClient(ServerBot):
    def __init__(self, connection, address, username='Mohaves', pfp=None):
        super().__init__(username, pfp)
        self.connection = connection
        self.address = address
        self.bot = False
        self.queue = queue.Queue()
        self.isLoaded = False
        self.betting = 0
        self.connected = True

        if self.address == "127.0.0.1":
            self.host = True
        else:
            self.host = False
    
    def addToQueue(self, data):
        self.queue.put(data)

    def promptAction(self):
        self.addToQueue(b'9[]\x1e')

class Deck():
    def __init__(self):
        self.suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.regenDeck()
        
    def getCard(self):
        self.choice = random.choice(self.deck)
        self.deck.pop(self.deck.index(self.choice))
        return self.choice
    
    def regenDeck(self):
        self.deck = []
        for suit in self.suits:
            for value in range(1, 14):
                self.deck.append(Card(suit, value))

class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.values = {
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
        if self.value:
            self.name = self.values[self.value] + " of " + self.suit
        else:
            self.name = None
        
        self.cardShown = False
            
    def getValue(self):
        return self.value
    
    def setValue(self, nValue):
        self.value = nValue
        
    def getName(self):
        return self.name
    
    def getValueName(self):
        return self.values[self.value]
    
    def setName(self):
        self.name = self.values[self.value] + " of " + self.suit
        
    def getSuit(self):
        return self.suit
    
    def setSuit(self, nSuit):
        self.suit = nSuit

if __name__ == '__main__':
    s = Server()