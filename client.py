import socket, os, json, threading, pygame, base64, assetloader, time, math, queue

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


#change port back to 6778

class Client():
    def __init__(self, username, pfp='', main=None):
        self.username = username
        self.pfp = pfp
        self.main = main

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.connection = None

        self.turn = False
        self.betting = 0
        self.money = [0, 0, 0, 0, 0]
        self.values = [1, 2, 4, 8, 16]
        self.totalMoney = 0
        self.currentPlayer = None
        self.id = None
        self.networkQueue = queue.Queue()
        self.folded = False

        self.stopping = threading.Event()
        self.timeDebounce = 0
    

    def serialiseClient(self):
        data = {
            'Name' : self.username,
        }
        
        return json.dumps(data)
    
    def sendingImages(self, picture):
        try:
            with open('./User Images/' + self.pfp, 'rb') as f:
                convertedImage = base64.b64encode(f.read())       
                self.client.sendall((convertedImage + b'\x1e'))
        except:
            with open(assetloader.imagePaths['no image'], 'rb') as f:
                convertedImage = base64.b64encode(f.read())       
                self.client.sendall((convertedImage + b'\x1e'))

    def connect(self, serverIp, port):
        self.serverIp = serverIp
        self.port = int(port != ''  and port or 27015)
        try:
            self.client.connect((self.serverIp, self.port))
            threading.Thread(target=self.clientLoop, args=(), daemon=True).start()
            return True
        except Exception as e:
            print("Connection error:", e)
            return False
        
    def send(self, data):
        try:
            self.client.sendall((data + '\x1e').encode())
        except Exception as e:
            print('Sending error:', e)

    def recieveData(self):
        data = b''
        while not self.stopping.is_set():
            try:
                recv = self.client.recv(4096)
                data += recv
                if not recv:
                    break
                elif recv[-1:] == b'\x1e':
                    data = data[:-1]
                    break
            except Exception as e:
                print('fuck you', e)
                break
            except:
                break
        packetId = ''
        while len(data) > 0 and chr(data[0]).isnumeric():
            packetId += chr(data[0])
            data = data[1:]
        if packetId == '':
            return '1000', None
        return packetId, data

    def clientLoop(self):
        self.send(self.serialiseClient())
        self.sendingImages(self.pfp)
        while not self.stopping.is_set():
            packetId, data = self.recieveData()
            match packetID[packetId]: 
                case "Connect":
                    pass
                case "Disconnect":
                    pass
                case "Id":
                    data = json.loads(data.decode())
                    self.id = data[0]
                case "Player Data":
                    print(data)
                    data = json.loads(data.decode())
                    self.main.game.players = data['Players']
                    self.turn = data['Current Player'] and (data['Current Player']['Id'] == self.main.client.id)

                    if len(self.main.game.mainPlayerHUD.playerDisplays.keys()) > 0:
                        for idx, val in enumerate(data['Players']):
                            if (val['Id'] != self.main.client.id):
                                self.main.game.mainPlayerHUD.playerDisplays[val['Id']].money = val['Money']
                                self.main.game.mainPlayerHUD.playerDisplays[val['Id']].action = val['Last Action']
                                self.main.game.mainPlayerHUD.playerDisplays[val['Id']].username = val['Name']

                    self.main.game.mainPlayerHUD.hand = [
                        self.main.Card(self.main, data['Hand'][0]['suit'], data['Hand'][0]['value']), 
                        self.main.Card(self.main, data['Hand'][1]['suit'], data['Hand'][1]['value'])
                    ] 
                    self.main.game.communityCards = []
                    for card in data['Community Cards']:
                        self.main.game.communityCards.append(self.main.Card(self.main, card['suit'], card['value']))
                    self.main.game.mainPlayerHUD.drawHand()

                    if data['Current Player']:
                        self.currentPlayer = data['Current Player']['Name']

                    print(data)
                    self.main.client.money = data['Money']
                    self.main.game.mainPlayerHUD.role = data['Role']
                    self.main.game.pot = data['Pot']
                    self.main.game.lastbet = data['Last Bet']
                case "New Game":
                    for display in self.main.game.mainPlayerHUD.playerDisplays.values():
                        display.remove2()
                    self.main.game.mainPlayerHUD.playerDisplays = {}
                    self.main.game.mainPlayerHUD.drawPlayers()
                    for clientId, playerInfo in self.main.game.mainPlayerHUD.playerDisplays.items():
                        if os.path.exists('./pfp/' +  clientId + '.png'):
                            playerInfo.profilePicture.update(pygame.image.load('./pfp/' + clientId + '.png'))
                    self.networkQueue.put(b'6[]\x1e')
                case "Picture":
                    data = data[1:]
                    clientId = ''
                    while len(data) > 0 and chr(data[0]).isnumeric():
                        clientId += chr(data[0])
                        data = data[1:]
                    data = data[1:]
                    picture = base64.b64decode(data + b'==')
                    with open('./pfp/' + clientId + '.png', 'wb') as f:
                        f.write(picture)
                    
                    for cid, playerInfo in self.main.game.mainPlayerHUD.playerDisplays.items():
                        if os.path.exists('./pfp/' +  clientId + '.png') and cid == clientId:
                            playerInfo.profilePicture.update(pygame.image.load('./pfp/' + clientId + '.png'))
                case "Message":
                    data = str(data.decode('utf-8'))
                    print(data)
                    if len(self.main.game.mainPlayerHUD.chatMessages) <= 4:
                        self.main.game.mainPlayerHUD.chatMessages.append(data[0])
                    else:
                        self.main.game.mainPlayerHUD.chatMessages.pop(0)
                        self.main.game.mainPlayerHUD.chatMessages.append(data[0])
                case "Turn":
                    self.main.client.turn = True
                    pygame.mixer.Sound("Assets/Sound/Ping.mp3").play()
                    self.totalMoney = self.calculateMoney()
                    self.betting = self.main.game.lastbet
                case "Start Game":
                    data = json.loads(data)
                    self.main.game.gameStart = data['Start Time']
                case _:
                    pass
            if not self.stopping.is_set():
                if not self.networkQueue.empty():
                    self.client.sendall(self.networkQueue.get())
                else:
                    self.client.sendall(b'1000[]\x1e')

    def minAmount(self):
        for idx, val in enumerate(self.money):
            if val >= 1:
                return self.values[idx]


    def increaseBet(self):
        minAmount = self.minAmount()
        if time.time() - self.timeDebounce >= 0.1:
            self.timeDebounce = time.time()
            if not self.betting + 1 > self.totalMoney:
                self.betting += minAmount

    def decreaseBet(self):
        minAmount = self.minAmount()
        if time.time() - self.timeDebounce >= 0.1:
            self.timeDebounce = time.time()
            if not self.betting - 1 < 0 and not self.betting - 1 < self.main.game.getLastBet():
                self.betting -= minAmount

    def fold(self):
        self.folded = True
        self.betting = 0
        self.endGo() 

    def endGo(self):
        if self.folded:
            self.networkQueue.put(b'11[]\x1e')
        else:
            self.networkQueue.put(bytes(f'10[{self.betting}]\x1e', 'utf-8'))
        self.turn = False
        self.betting = 0

    def calculateMoney(self):
        value = 1
        totalMoney = 0
        for i in self.money:
            amount = value * i
            totalMoney += amount
            value *= 2
        self.totalMoney = totalMoney
        return self.totalMoney
    
    def bet(self, amount):
        starting = amount
        chipsAdded = [0, 0, 0, 0, 0]
        print(amount)
        if not amount == 0:
            for i in range(4, -1, -1):
                print(amount, self.values[i])
                if amount >= self.values[i] and self.money[i]:
                    amountOfTimes = amount // self.values[i]
                    if amountOfTimes <= self.money[i]:
                        chipsAdded[i] += amountOfTimes
                        amount -= amountOfTimes * self.values[i]
                    else:
                        chipsAdded[i] = self.money[i]
                        amount -= self.money[i] * self.values[i]
            if amount == 0:
                self.lastbet = starting
                print(chipsAdded)
                self.minusChips(chipsAdded)
                self.endGo()
        else:
            self.endGo()
                    

        
        
    def minusChips(self, arrayChips):
        for index in range(len(self.money)):
            self.money[index] -= arrayChips[index] 
    

    def disconnect(self):
        self.stopping.set()
        self.recieveData()
        self.send('1[Disconnect]')
        # self.client.close()

    
            

        
if __name__ == "__main__":
    c = Client(username='Bartholomew Montgomery Clyde')
    c.money = [10, 5, 3, 2, 1]
    c.bet(65)
                   