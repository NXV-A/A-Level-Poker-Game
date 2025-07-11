import random, pygame, pygame.locals, os, traceback, time, math, compare, client, server, json
from assetloader import *

try:
    with open('settings.txt', 'r') as f:
        settings = json.loads(f.read())
except:
    settings = {
        "Width": "1920", 
        "Height": "1080", 
        "Fullscreen": True, 
        "Username": "Username", 
        "Picture": "", 
        "Server Port": "27015"
    }
    with open('settings.txt', 'w') as f:
        f.write(json.dumps(settings))


class Main():
    images = []
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.info = pygame.display.Info()
        self.width, self.height = self.info.current_w, self.info.current_h
        self.size = [self.width, self.height]
        self.images = {}
        self.running = True
        self.sprites = pygame.sprite.Group()
        self.objects = []
        self.game = None

        self.Card = Card
        
        
        if settings["Fullscreen"]:
            self.window = pygame.display.set_mode(self.size, pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.window = pygame.display.set_mode((int(settings['Width']), int(settings['Height'])), pygame.RESIZABLE)
            self.size = [settings['Width'], settings['Height']]
            
        self.grey = (20, 20, 20)
        self.green = (15, 138, 19)
            
        self.load()
        self.client = client.Client(username=settings['Username'], pfp=settings['Picture'], main=self)
         
        
        
        pygame.display.set_caption("Pixel Poker")
        pygame.display.set_icon(self.images['Poker icon'])
        
        self.mainMenu()
        
        self.loop()
    
    def updateSettings(self):
        with open('settings.txt', 'w') as f:
            f.write(json.dumps(settings))

    def writeSettings(self, param, data):
        settings[param] = data
        if param == 'Username': 
            self.client.username = data
        elif param == 'Picture':
            self.client.pfp = data
        self.updateSettings()
        
    def updateFullscreen(self):
        if settings['Fullscreen']:
            self.writeSettings('Fullscreen', False)
        else:
            self.writeSettings('Fullscreen', True)
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:
                #     self.quit()
                    

                if self.game:
                    if self.client.turn:
                        if event.key == pygame.K_RETURN:
                            self.client.bet(self.client.betting)
                    
            pos = pygame.mouse.get_pos()
            for Object in self.objects:
                if type(Object) == TextInput:
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        if Object.rect.collidepoint(pos): 
                            Object.active = True
                        else: 
                            Object.active = False
                            Object.call_back()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE and Object.active: 
            
                            Object.textInput = Object.textInput[:-1]
                        elif event.key == pygame.K_RETURN and Object.active:
                            Object.active = False
                            Object.call_back()
                        elif event.key == pygame.K_ESCAPE and Object.active:
                            Object.active = False
                        elif Object.active and len(Object.textInput) <= Object.charLimit: 
                            Object.textInput += event.unicode
                
                elif type(Object) == Button:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:            
                            buttonPressed = False
                            if Object.rect.collidepoint(pos) and not buttonPressed:
                                pygame.mixer.Sound("Assets/Sound/Click.mp3").play()
                                Object.call_back()
                                buttonPressed = True

    def quit(self):
        self.running = False
        self.client.disconnect()
                            
    def render(self):
        self.window.fill(self.background)
        self.sprites.draw(self.window)
     
    def removeAllSprites(self):
        self.sprites.empty()
        for object in self.objects:
            try:
                object.remove()
            except:
                object.remove2()
        self.objects = []
                            
    def load(self):
        self.imagePaths = {}
        for (name, group) in imgGroups.items():
            for item in group:
                ext = ".png"
                splitted = item.split(".")
                if len(splitted) > 1:
                    item = splitted[0]
                    ext = "." + splitted[1]
                    
                self.images[item] = pygame.image.load(os.path.join(name, item + ext)).convert_alpha()
                self.imagePaths[item] = os.path.join(name, item + ext)
                
                
    def mainMenu(self):
        self.removeAllSprites()
        self.background = self.grey
        self.logo = Image(self, xy=[self.width/2 - 84, 30], dim=[169,95], group=self.sprites, image=self.images['Logo'])
        self.b1 = Button(self, xy=[self.width/2, 150], function=self.modeSelect, text='Play', dim=[200, 50], group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 200], function=self.settingsMenu, text='Settings', dim=[200, 50], group=self.objects)
        self.b3 = Button(self, xy=[self.width/2, 250], function=self.quit, text='Quit', dim=[200, 50], group=self.objects)
        self.qr = Image(self, xy=[self.width/2, 350], dim=[58,58], group=self.sprites, image=self.images['QR'])

    def settingsMenu(self):
        self.removeAllSprites()
        self.background = self.grey
        self.userText = TextLabel(self, text='Username:', xy=[self.width/2 - 180, 150], group=self.objects)
        self.pictureText = TextLabel(self, text='Picture:', xy=[self.width/2 - 160, 186], group=self.objects)
        self.portText = TextLabel(self, text='Port:', xy=[self.width/2 - 140, 222], group=self.objects)
        self.widthText = TextLabel(self, text='Width:', xy=[self.width/2 - 150, 318], group=self.objects)
        self.heightText = TextLabel(self, text='Height:', xy=[self.width/2 - 150, 354], group=self.objects)
        self.t1 = TextInput(self, default=settings['Username'], xy=[self.width/2 - 100, 150], function=self.writeSettings, param='Username', group=self.objects)
        self.t2 = TextInput(self, default=settings['Picture'], xy=[self.width/2 - 100, 186], function=self.writeSettings, param='Picture', group=self.objects)
        self.t3 = TextInput(self, default=settings['Server Port'], xy=[self.width/2 - 100, 222], function=self.writeSettings, param='Server Port', group=self.objects)
        self.b1 = Button(self, xy=[self.width/2, 287], function=self.updateFullscreen, text='Fullscreen Toggle' , dim=[250, 50], group=self.objects)
        self.fScreentxt = TextLabel(self, text='(restart to take effect)', xy=[self.width/2 + 290, 272], group=self.objects)
        self.t4 = TextInput(self, default=settings['Width'], xy=[self.width/2 - 100, 318], function=self.writeSettings, param='Width', group=self.objects)
        self.t5 = TextInput(self, default=settings['Height'], xy=[self.width/2 - 100, 354], function=self.writeSettings, param='Height', group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 419], function=self.mainMenu, text='Back', dim=[200, 50], group=self.objects)

    def modeSelect(self):
        self.removeAllSprites()
        self.background = self.grey
        self.logo = Image(self, xy=[self.width/2 - 84, 30], dim=[169,95], group=self.sprites, image=self.images['Logo'])
        self.b1 = Button(self, xy=[self.width/2, 150], function=self.singleplayer, text='Singleplayer', dim=[200, 50], group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 200], function=self.joinOrCreate, text='Multiplayer', dim=[200, 50], group=self.objects)
        self.b3 = Button(self, xy=[self.width/2, 250], function=self.mainMenu, text='Back', dim=[200, 50], group=self.objects)
        self.qr = Image(self, xy=[self.width/2, 350], dim=[58,58], group=self.sprites, image=self.images['QR'])


    def joinOrCreate(self):
        self.removeAllSprites()
        self.background = self.grey
        self.logo = Image(self, xy=[self.width/2 - 84, 30], dim=[169,95], group=self.sprites, image=self.images['Logo'])
        self.b1 = Button(self, xy=[self.width/2, 150], function=self.joinServerMenu, text='Join a lobby', dim=[200, 50], group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 200], function=self.createMultiplayerServer, text='Create a lobby', dim=[200, 50], group=self.objects)
        self.b3 = Button(self, xy=[self.width/2, 250], function=self.modeSelect, text='Back', dim=[200, 50], group=self.objects)
        self.qr = Image(self, xy=[self.width/2, 350], dim=[58,58], group=self.sprites, image=self.images['QR'])

    def joinServerMenu(self):
        self.removeAllSprites()
        self.background = self.grey
        self.userText = TextLabel(self, text='Server Ip:', xy=[self.width/2 - 185, 150], group=self.objects)
        self.portText = TextLabel(self, text='Port:', xy=[self.width/2 - 150, 186], group=self.objects)
        self.t1 = TextInput(self, default='', xy=[self.width/2 - 100, 150], group=self.objects)
        self.t2 = TextInput(self, default='', xy=[self.width/2 - 100, 186], group=self.objects)
        self.b1 = Button(self, xy=[self.width/2, 250], function=self.connectToServer, text='Join', dim=[200, 50], group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 300], function=self.joinOrCreate, text='Back', dim=[200, 50], group=self.objects)


    def connectToServer(self):
        self.background = self.green
        self.connectionIp = self.t1.textInput
        self.connectionPort = self.t2.textInput
        self.removeAllSprites()
        self.game = Game(self, gametype="Multiplayer - J")

    def createMultiplayerServer(self):
        self.removeAllSprites()
        self.background = self.green
        self.game = Game(self, gametype="Multiplayer - C")

    def singleplayer(self):
        self.removeAllSprites()
        self.background = self.green
        self.game = Game(self, gametype="Singleplayer")


    def updateObjects(self):
        for Object in self.objects:
            Object.update()
                            

    def loop(self):
        while self.running:
            self.dt = self.clock.tick(100) / 1000
            self.events()
            self.render()
            self.updateObjects()
            pygame.display.flip()
        pygame.quit()
        exit()

class Game():
    def __init__(self, parent, gametype=None, bots=None):
        self.parent = parent
        self.gametype = gametype
        self.players = []
        self.font = pygame.font.SysFont('Calibri',35)
        self.textColour = [0, 0, 0]
        self.gameStart = None

        self.pot = [0, 0, 0, 0, 0]
        self.communityCards = []
        self.lastbet = 0
        self.gameNumber = 0
        self.playerNumber = 0


        self.playerNumber = 0

        if self.gametype == "Singleplayer":
            self.server = server.Server(isInternal=True, game=self, port=settings['Server Port'])
            connected = self.parent.client.connect('127.0.0.1', settings['Server Port'])
        elif self.gametype == "Multiplayer - C":
            self.server = server.Server(game=self, port=settings['Server Port'])
            connected = self.parent.client.connect('127.0.0.1', settings['Server Port'])
        elif self.gametype == "Multiplayer - J":
            connected = self.parent.client.connect(self.parent.connectionIp, self.parent.connectionPort)
            self.server = False
        else:
            print('Attempted to create a gametype which isn\'t recognised')

        if not connected:
            print('Failed to connect.')
            return self.parent.mainMenu()

        
        self.mainPlayerHUD = MainPlayerUI(self, size=100, picture=self.parent.client.pfp, username=self.parent.client.username)
    
    def setup(self):
        for player in self.players:
            player.setGame(self)
        
    def setLastBet(self, amount):
        self.lastbet = amount
        
    def getLastBet(self):
        return self.lastbet
        
    def getTurnNumber(self):
        return self.turnNumber
    
    def getGameNumber(self):
        return self.gameNumber
    
    def getPlayers(self):
        return self.players
    
    def getCommunityCards(self):
        return self.communityCards
    
        
        

class Card():
    def __init__(self, parent, suit, value, xy=[100, 100], size=[100, 100]):
        self.parent = parent
        self.suit = suit
        self.value = value
        self.xy = xy
        self.size = size
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
            self.card = self.parent.images[self.name]
        else:
            self.card = self.parent.images['card_empty']
            self.name = None
        self.back = self.parent.images['card_back']
        
        self.cardShown = False
        
        
    def switch(self):
        try:
            if self.value:
                if self.image.graphic == self.card:
                    self.image.update(self.back)
                else:
                    self.image.update(self.card)
            else:
                if self.image.graphic == self.card:
                    self.image.update(self.back)
                else:
                    self.image.update(self.parent.images['card_empty'])
        except:
            pass
            
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
        
    def getXY(self):
        return self.xy
    
    def setXY(self, nXY):
        self.xy = nXY
        
    def show(self):
        self.image = Image(self.parent, xy=self.xy, dim=self.size, group=self.parent.sprites, image=self.card)
        self.cardShown = True
        
    def hide(self):
        self.image.kill()
        self.cardShown = False
        
    def remove(self):
        self.image.kill()
        del self
        

class Button():
    def __init__(self, parent, text='Button', font='Calibri', dim=[100,50], xy=[0,0], textColour=[0, 0, 0], buttonColour=[122, 122, 122], function=None, args=None, group=None):
        self.buttonText = text
        self.font = pygame.font.SysFont(font,35)
        self.buttonDim = dim
        self.xy = xy
        self.textColour = textColour
        self.buttonColour = buttonColour
        self.buttonActive = self.getButtonColours()
        self.function = function
        self.pressed = False
        self.parent = parent
        self.group = group
        self.args = args
        
        self.image = pygame.Surface((self.buttonDim[0], self.buttonDim[1]))
        self.rect = self.image.get_rect(center=(self.xy[0], self.xy[1]))

        self.text = self.font.render(self.buttonText, True, self.textColour)
        
        self.group.append(self)
        
    def colourChange(self):
        self.buttonColour = self.buttonActive[0]
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.buttonColour = self.buttonActive[1]
        
    def update(self):
        self.colourChange()
        mouse = pygame.mouse.get_pos()
        self.image.fill((self.pressed and self.buttonActive[0]) or self.buttonColour)
        self.image.blit(self.text, [self.rect.width/2 - self.text.get_rect().width/2, self.rect.height/2 - self.text.get_rect().height/2])
        self.parent.window.blit(self.image, self.rect)
        
    def getButtonColours(self):
        original = self.buttonColour
        highlight = []
        click = []
        for value in self.buttonColour:
            highlight.append(value + 50)
            click.append(value - 50)
        return [original, highlight, click]
    
    def call_back(self):
        self.buttonColour = self.buttonActive[2]
        if self.function:
            if self.args:
                self.function(self.args)
            else:
                self.function()
                
    def remove(self):
        global buttonList
        if self in self.group:
            self.group.remove(self)
        else:
            print('Im already gone')
            
class TextInput():
    def __init__(self, parent, font='Calibri', currentColour=(50, 50, 50), selectColour=(100, 100, 100), default='', xy=[100, 100], size=[140, 35], function=None, param=None, group=None):
        self.size = size
        self.xy = xy
        self.font = pygame.font.SysFont(font, self.size[1])
        self.textInput = str(default)
        self.rect = pygame.Rect(xy[0], xy[1], self.size[0], self.size[1]) 
        self.selectedColour = selectColour
        self.passiveColour = currentColour
        self.currentColour = self.passiveColour
        self.charLimit = 30
        self.active = False
        self.group = group
        self.parent = parent
        self.group.append(self)
        self.function = function
        self.param = param
        
    def update(self):
        if self.active: 
            self.currentColour = self.selectedColour
        else: 
            self.currentColour = self.passiveColour
          
        pygame.draw.rect(self.parent.window, self.currentColour, self.rect)
        inputtedText = self.font.render(self.textInput, True, (255, 255, 255))
        self.rect.w = max(100, inputtedText.get_width()+10) 
        self.parent.window.blit(inputtedText, (self.rect.x + 5, self.rect.y + 5))

    def call_back(self):
        if self.function and self.param:
            self.function(self.param, self.textInput)
        elif self.function:
            self.function(self.textInput)

    def remove(self):
        if self in self.group:
            self.group.remove(self)
        else:
            print('Im already gone')
        

class Image(pygame.sprite.Sprite):
    def __init__(self, parent, image=None, xy=[0,0], dim=[100,100], group=None):
        super().__init__()
        self.parent = parent
        self.graphic = image
        self.xy = xy
        if self.graphic != None:
            self.image = pygame.transform.scale(self.graphic, (dim[0], dim[1]))
        else:
            self.graphic = self.parent.images['no image']
            self.image = pygame.transform.scale(self.graphic, (dim[0], dim[1]))
        self.rect = self.image.get_rect(topleft=(self.xy[0], self.xy[1]))
        self.dim = dim
        self.group = parent.sprites
        
        
        self.group.add(self)
        
    def update(self, image):
        self.graphic = image
        if self.graphic != None:
            self.image = pygame.transform.scale(self.graphic, (self.dim[0], self.dim[1]))
            self.rect = self.image.get_rect(topleft=(self.xy[0], self.xy[1]))
    
    def remove2(self):
        if self in self.group:
            self.group.remove(self)
            self.kill()
        else:
            print('Im already gone')

class TextLabel():
    def __init__(self, parent, text='', font='Calibri', xy=[0,0], textColour=(255, 255, 255), size=35, group=None):
        self.size = size
        self.font = pygame.font.SysFont(font, self.size)
        self.parent = parent
        self.text = text
        self.xy = xy
        self.group = group
        self.colour = textColour

        self.renderText = self.font.render(self.text, True, textColour)
        self.renderRect = self.renderText.get_rect()
        
        self.group.append(self)

    def update(self):
        self.parent.window.blit(self.renderText, (self.xy[0] - self.renderRect.w/2, self.xy[1]), )
    
    def remove(self):
        if self in self.group:
            self.group.remove(self)
        else:
            print('Im already gone')


class PlayerInfo():
    def __init__(self, parent, player=None, xy=[100, 100], font='Calibri', textColour=[0,0,0], size=100):
        self.parent = parent
        self.player = player
        self.xy = xy
        print(self.player)
        self.money = self.player['Money']
        self.username = self.player['Name']
        self.graphic = None
        self.group = self.parent.objects
        self.size = size
        self.chips = []
        self.roleIcon = None
        self.action = ''
        

        self.textColour = textColour
        self.font = pygame.font.SysFont(font, int(self.size * 0.35))
        self.text = self.font.render(self.username, True, self.textColour)
        
        self.profilePicture = Image(self.parent, image=self.graphic, xy=self.xy, dim=[self.size, self.size])

        self.group.append(self)
        self.drawChips()
        self.drawRole()
        
    def drawChips(self):
        value = 1
        chipSpacingX = self.size / 4
        chipSpacingY = self.size / 50
        chipXY = [self.xy[0] + (self.size * 1.1),  self.xy[1] + (self.size / 2)]
        if self.chips != []:
            for chip in self.chips:
                chip.kill()
        self.chips = []
        for index in self.money:
            for x in range(index):
                self.chips.append(Image(self.parent, image=self.parent.images[str(value)], xy=(chipXY[0], chipXY[1]), dim=[self.size / 4, self.size / 4]))
                chipXY[1] -= chipSpacingY
            chipXY[0] += chipSpacingX
            chipXY[1] = self.xy[1] + (self.size / 2)
            value *= 2
    
    def drawRole(self):
        iconXY = [self.xy[0] + 100,  self.xy[1] + 100]
        if self.roleIcon != None:
            self.roleIcon.kill()
        playerRole = self.player['Role']
        if not playerRole == 'Player':
            if playerRole == 'Dealer':
                self.roleIcon = Image(self.parent, image=self.parent.images['Dealer'], xy=(iconXY[0], iconXY[1]), dim=[self.size / 4, self.size / 4])
            elif playerRole == 'Little Blind':
                self.roleIcon = Image(self.parent, image=self.parent.images['Little blind'], xy=(iconXY[0], iconXY[1]), dim=[self.size / 4, self.size / 4])
            elif playerRole == 'Big Blind':
                self.roleIcon = Image(self.parent, image=self.parent.images['Big blind'], xy=(iconXY[0], iconXY[1]), dim=[self.size / 4, self.size / 4])

        
    def update(self):
        self.actionText = self.font.render(self.action, True, self.textColour)
        self.parent.window.blit(self.actionText, (self.xy[0] + (self.size * 1.1), self.xy[1] + 80), )
        if self.text:
            self.parent.window.blit(self.text, (self.xy[0] + (self.size * 1.1), self.xy[1]), )
        self.drawChips()
        self.drawRole()
        
    def remove2(self):
        if self in self.group:
            self.group.remove(self)
        else:
            print('Im already gone')
    
      
      
class MainPlayerUI():
    def __init__(self, parent, username='Username', picture=None, hand=[None, None], font='Calibri', textColour=[0,0,0], size=100):
        self.parent = parent
        self.size = 100
        self.xy = [parent.parent.width/2 - self.size * 2.5, 3 * parent.parent.height / 4]
        self.hand = []
        self.overallHand = []
        self.username = username
        try:
            self.graphic = pygame.image.load('./User Images/' + picture).convert_alpha()
        except:
            self.graphic = self.parent.parent.images['no image']
        self.group = self.parent.parent.objects
        self.group.append(self)
        self.handShown = 0
        self.chips = []
        self.potChips = []
        self.emptyCards = []
        self.roleIcon = None
        self.role = 'Player'
        self.totalMoney = 0
        self.playerDisplays = {}
        
        self.textColour = textColour
        self.font = pygame.font.SysFont(font, int(self.size * 0.35))

        self.bettingAmount = 0
        self.action = "Check"
        self.foldAction = "Fold"
        self.handAction = "Check Hand"
        self.chatText = 'Toggle Chat'
        self.handName = ''
        self.timeElapsed = '0'
        self.foldActionText = self.font.render(self.foldAction, True, self.textColour)
        self.handActionText = self.font.render(self.handAction, True, self.textColour)
        self.pokerHelp = False
        self.pokermenu = None
        self.paused = False
        self.lastTime = 0
        self.lastTime2 = 0
        self.b1 = None
        self.textInput = None
        self.chatMessages = ['mate', 'john', 'egg']
        self.chatting = False
        self.messages = []
        self.textObjects = []

        self.drawSelfPlayerInfo()
        self.drawControls()
        self.drawHand()
        self.drawPlayers()
        self.drawCommunityCards()
        self.drawRole()

    def drawPokerHelpMenu(self):
        if self.pokerHelp:
            if not self.pokermenu:
                self.pokermenu = Image(self.parent.parent, image=self.parent.parent.images['Poker Assistance'], dim=[self.parent.parent.width/2, self.parent.parent.height], xy=[self.parent.parent.width/2 - self.parent.parent.width/4, 0])
        elif self.pokermenu:
            self.pokermenu.remove2()
            self.pokermenu = None
        
    def drawSelfPlayerInfo(self):
        self.profilePicture = Image(self.parent.parent, image=self.graphic, xy=self.xy, dim=[self.size, self.size])
        self.text = self.font.render(self.username, True, self.textColour)
        
        
    def drawChips(self):
        value = 1
        chipSpacingX = self.size / 1.5
        chipSpacingY = 4 * self.size / 80
        chipXY = [self.xy[0] + (self.size * 1.1),  self.xy[1] + (self.size / 1.5)]
        if self.chips != []:
            for chip in self.chips:
                chip.kill()
        self.chips = []
        for index in self.parent.parent.client.money:
            for x in range(index):
                self.chips.append(Image(self.parent.parent, image=self.parent.parent.images[str(value)], xy=(chipXY[0], chipXY[1]), dim=[self.size / 1.5, self.size / 1.5]))
                chipXY[1] -= chipSpacingY
            chipXY[0] += chipSpacingX
            chipXY[1] = self.xy[1] + (self.size / 1.5)
            value *= 2
            
    def calculatePot(self):
        value = 1
        totalMoney = 0
        for i in self.parent.pot:
            amount = value * i
            totalMoney += amount
            value *= 2
        return totalMoney
            
    def drawPot(self):
        value = 1
        chipSpacingX = self.size / 1.5
        chipSpacingY = 4 * self.size / 80
        chipY = self.parent.parent.height / 2
        chipXY = [self.parent.parent.width/2 - self.size * 2,  chipY]
        if self.potChips != []:
            for chip in self.potChips:
                chip.kill()
        self.potChips = []
        for index in self.parent.pot:
            for x in range(index):
                self.potChips.append(Image(self.parent.parent, image=self.parent.parent.images[str(value)], xy=(chipXY[0], chipXY[1]), dim=[self.size / 1.5, self.size / 1.5]))
                chipXY[1] -= chipSpacingY
            chipXY[0] += chipSpacingX
            chipXY[1] = chipY
            value *= 2
            
        self.potValue = self.font.render('Pot: £' + str(self.calculatePot()), True, self.textColour)
        self.potVRect = self.potValue.get_rect()

    def drawRole(self):
        iconXY = [self.xy[0] + 100,  self.xy[1] + 100]
        if self.roleIcon != None:
            self.roleIcon.kill()
        playerRole = self.role
        if not playerRole == 'Player':
            if playerRole == 'Dealer':
                self.roleIcon = Image(self.parent.parent, image=self.parent.parent.images['Dealer'], xy=(iconXY[0], iconXY[1]), dim=[self.size / 4, self.size / 4])
            elif playerRole == 'Little Blind':
                self.roleIcon = Image(self.parent.parent, image=self.parent.parent.images['Little blind'], xy=(iconXY[0], iconXY[1]), dim=[self.size / 4, self.size / 4])
            elif playerRole == 'Big Blind':
                self.roleIcon = Image(self.parent.parent, image=self.parent.parent.images['Big blind'], xy=(iconXY[0], iconXY[1]), dim=[self.size / 4, self.size / 4])

    def drawControls(self):
        self.xpos = self.parent.parent.width
        self.ypos = self.parent.parent.height - 160
        self.upArrow = Image(self.parent.parent, image=self.parent.parent.images['Up'],xy=[self.xpos - 40, self.ypos] , dim=[40, 40])
        self.downArrow = Image(self.parent.parent, image=self.parent.parent.images['Down'], xy=[self.xpos - 80, self.ypos], dim=[40, 40])
        self.enter = Image(self.parent.parent, image=self.parent.parent.images['Enter'], xy=[self.xpos - 40, self.ypos + 40], dim=[40, 40])
        self.fKey = Image(self.parent.parent, image=self.parent.parent.images['F'], xy=[self.xpos - 40, self.ypos + 80], dim=[40, 40])
        self.spacebar = Image(self.parent.parent, image=self.parent.parent.images['Space'], xy=[self.xpos - 40, self.ypos + 120], dim=[40, 40])
        self.tabkey = Image(self.parent.parent, image=self.parent.parent.images['Tab'], xy=[self.xpos - 40, self.ypos - 40], dim=[40, 40])
        if self.parent.server:
            if not self.parent.server.isInternal:
                self.altkey = Image(self.parent.parent, image=self.parent.parent.images['Alt'], xy=[self.xpos - 40, self.ypos - 80], dim=[40, 40])
        else:
            self.altkey = Image(self.parent.parent, image=self.parent.parent.images['Alt'], xy=[self.xpos - 40, self.ypos - 80], dim=[40, 40])

    def drawHand(self):
        if len(self.hand) >= 2:
            card1 = self.hand[0]
            card2 = self.hand[1]
            card1.setXY([self.parent.parent.width/2 - 100, self.parent.parent.height - 100])
            card2.setXY([self.parent.parent.width/2 - 30, self.parent.parent.height - 100])
            card1.show()
            card2.show()
            card1.switch()
            card2.switch()
            
    def drawPlayers(self):
        players = self.parent.players
        playerIndex = 0
        for idx, val in enumerate(players):
            if val['Id'] == self.parent.parent.client.id:
                playerIndex = idx
                break
        visPlayers = players[playerIndex:] + players[:playerIndex]
        playerPositions = [
            [self.parent.parent.width/20, self.parent.parent.height/2],
            [self.parent.parent.width/20, self.parent.parent.height/12],
            [self.parent.parent.width - self.parent.parent.width/5, self.parent.parent.height/12],
            [self.parent.parent.width - self.parent.parent.width/5, self.parent.parent.height/2],
        ]

        self.playerDisplays = {}
        
        for playerNumber in range(len(visPlayers)):
            if visPlayers[playerNumber]['Id'] != self.parent.parent.client.id:
                playerObject = PlayerInfo(self.parent.parent, player=visPlayers[playerNumber], xy=playerPositions[playerNumber - 1])
                self.playerDisplays[visPlayers[playerNumber]['Id']] = playerObject

            
    def flipHand(self):
        self.cardXY = [self.parent.parent.width/2 - 70, self.parent.parent.height - 100]
        if self.handShown == 0:
            self.handShown = 1
        else:
            self.handShown = 0
        for card in self.hand:
            card.switch()

    def drawCommunityCards(self):
        self.cardsxy = [self.parent.parent.width /2 - 190, 70]
        for card in self.parent.communityCards:
            card.setXY(self.cardsxy)
            card.show()
            self.cardsxy[0] += 70
        for card in range(5 - len(self.parent.communityCards)):
            blankCard = Card(self.parent.parent, None, None)
            blankCard.setXY(self.cardsxy)
            blankCard.show()
            blankCard.switch()
            self.emptyCards.append(blankCard)
            self.cardsxy[0] += 70
            
    def removeCommunityCards(self):
        for blank in self.emptyCards:
            blank.remove()
        self.emptyCards = []
        for card in self.parent.communityCards:
            if card.cardShown:
                card.hide()

    def gameInfo(self):
        if self.parent.parent.client.currentPlayer != None:
            self.currentPlayerText = self.font.render(self.parent.parent.client.currentPlayer + "'s Turn", True, self.textColour)
        else:
            self.currentPlayerText = self.font.render("Game is starting", True, self.textColour)
        self.parent.parent.window.blit(self.currentPlayerText, (self.parent.parent.width/2 - self.currentPlayerText.get_rect().width/2, 40))
        
        self.timeText = self.font.render(self.getTime() + ' Game 1, Turn 1', True, self.textColour)
        self.timeRect = self.timeText.get_rect()
        self.parent.parent.window.blit(self.timeText, (self.parent.parent.width/2 - self.timeRect.width/2, 0))

    def getTime(self):
        if self.parent.gameStart:
            self.timeInS = math.floor(time.time() - self.parent.gameStart)
            self.minutesElapsed = math.floor(self.timeInS/60)
            self.hoursElapsed = math.floor(self.minutesElapsed/60)
            
            self.timer = f"{self.hoursElapsed:02}:{self.minutesElapsed - (self.hoursElapsed * 60):02}:{self.timeInS - (self.minutesElapsed * 60):02}"
            return self.timer
        else:
            return 'Waiting For Start,'
    
    def togglePause(self):
        if not self.paused and time.time() - self.lastTime >= 0.1:
            self.lastTime = time.time()
            self.paused = True
        elif time.time() - self.lastTime >= 2:
            self.lastTime = time.time()
            self.b1.remove()
            self.b1 = None
            self.b2.remove()
            self.b2 = None
            self.paused = False

    def toggleChat(self):
        if not self.chatting and time.time() - self.lastTime2 >= 0.1:
            self.lastTime2 = time.time()
            self.chatting = True
        elif time.time() - self.lastTime2 >= 2:
            self.lastTime2 = time.time()
            self.textInput.remove()
            for i in self.textObjects:
                i.remove()
            self.textObjects = []
            self.textInput = None
            self.chatting = False
    
    def leave(self):
        self.parent.parent.client.disconnect()
        self.parent.parent.game = None
        self.parent.parent.mainMenu()

    def sendMessage(self, text):
        print('Yes you called')
        if self.textInput and text != '':
            self.parent.parent.client.networkQueue.put(b'7['+ bytes(text, 'utf-8') + b']\x1e')
            self.textInput.textInput = ''
    
    def chatMenu(self):
        positions = [
            [150, self.parent.parent.height - 135],
            [150, self.parent.parent.height - 170],
            [150, self.parent.parent.height - 205],
            [150, self.parent.parent.height - 240],
            [150, self.parent.parent.height - 275]
        ]
        pygame.draw.rect(self.parent.parent.window, (20, 20, 20), pygame.Rect(50, self.parent.parent.height - 300, 270, 200))
        if not self.textInput:
            self.textInput = TextInput(self.parent.parent, function=self.sendMessage, param='', xy=[50, self.parent.parent.height - 100], group=self.parent.parent.objects)
        for i in self.textObjects:
            i.remove()
        self.textObjects = []
        count = 0
        for message in self.chatMessages:
            self.textObjects.append(TextLabel(self.parent.parent, text=message, xy=positions[count], group=self.parent.parent.objects))
            count += 1

    
    def pauseMenu(self):
        pygame.draw.rect(self.parent.parent.window, (20, 20, 20), pygame.Rect(0, 0, self.parent.parent.width, self.parent.parent.height))
        if not self.b1 or not self.b2:
            self.b1 = Button(self.parent.parent, text='Quit', function=self.parent.parent.quit,  xy=[self.parent.parent.width/2, self.parent.parent.height/2],group=self.parent.parent.objects)
            self.b2 = Button(self.parent.parent, text='Main Menu', function=self.leave, dim=[250, 50], xy=[self.parent.parent.width/2, self.parent.parent.height/2 - 50],group=self.parent.parent.objects)
        
        
    def update(self):
        self.overallHand = self.hand + self.parent.communityCards

        self.drawPokerHelpMenu()
        self.drawPot()
        self.drawChips()
        self.gameInfo()
        self.removeCommunityCards()
        self.drawCommunityCards()
        self.drawRole()

        self.betText = self.font.render(("£" + str(self.parent.parent.client.betting)), True, self.textColour)
        self.pokerAssistance = self.font.render("Poker Assistance", True, self.textColour)
        self.textChat = self.font.render(self.chatText, True, self.textColour)
        if self.parent.lastbet < self.parent.parent.client.betting:
            self.betPromptText = self.font.render("Raise", True, self.textColour)
        elif self.parent.parent.client.betting == 0:
            self.betPromptText = self.font.render("Check", True, self.textColour)
        elif self.parent.lastbet == self.parent.parent.client.betting:
            self.betPromptText = self.font.render("Call", True, self.textColour)
        elif self.parent.parent.client.betting == self.parent.parent.client.betting:
            self.betPromptText = self.font.render("All in", True, self.textColour)
        self.betTextRect = self.betText.get_rect()
        self.betPromptRect = self.betPromptText.get_rect()
        self.parent.parent.window.blit(self.text, (self.xy[0] + (self.size * 1.1), self.xy[1]))
        self.parent.parent.window.blit(self.betText, (self.xpos - self.betTextRect.width - 85, self.ypos))
        self.parent.parent.window.blit(self.pokerAssistance, (self.xpos - 280, self.ypos - 40))
        self.parent.parent.window.blit(self.betPromptText, (self.xpos - self.betPromptRect.width - 45, self.ypos + 40))
        self.parent.parent.window.blit(self.foldActionText, (self.xpos - 105, self.ypos + 80))
        self.parent.parent.window.blit(self.handActionText, (self.xpos - 210, self.ypos + 120))
        self.parent.parent.window.blit(self.potValue, (self.parent.parent.width - self.potVRect.width, 0))
        if self.parent.server:
            if not self.parent.server.isInternal:
                self.parent.parent.window.blit(self.textChat, (self.xpos - 280, self.ypos - 80))
        else:
            self.parent.parent.window.blit(self.textChat, (self.xpos - 280, self.ypos - 80))
        if self.handShown == 1:
            self.handValue = compare.getValueOfHand(self.overallHand)
            self.handName = compare.valueToName(self.handValue)
            self.handNameText = self.font.render(self.handName, True, self.textColour)
            self.handNameTextRect = self.handNameText.get_rect()
            self.parent.parent.window.blit(self.handNameText, (self.parent.parent.width/2 - (self.handNameTextRect.width /2), (self.parent.parent.height * 9/10) - self.handNameTextRect.height))
            
            
        fpsText = self.font.render(str(int(self.parent.parent.clock.get_fps())), True, self.textColour)
        if self.parent.server:
            if self.parent.server.isInternal:
                serverInfoText = self.font.render("Singleplayer", True, self.textColour)
            else:
                serverInfoText = self.font.render("Server Ip: " + self.parent.server.globalIp + ":" + str(self.parent.parent.client.port), True, self.textColour)
        else:
            serverInfoText = self.font.render("Server Ip: " + self.parent.parent.client.serverIp + ":" + str(self.parent.parent.client.port), True, self.textColour)
        serverInfoTextRect = serverInfoText.get_rect()
        self.parent.parent.window.blit(fpsText, (0, 0))
        self.parent.parent.window.blit(serverInfoText, (0, self.parent.parent.height - serverInfoTextRect.height))
        
        if self.handShown == 1:
            self.flipHand()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: self.flipHand()
        if keys[pygame.K_ESCAPE]: self.togglePause()
        if keys[pygame.K_LALT]: self.toggleChat()
        if keys[pygame.K_p]: self.parent.parent.client.networkQueue.put(b'7["Mr Margon"]\x1e')
        if keys[pygame.K_TAB]: 
            self.pokerHelp = True
        else:
            self.pokerHelp = False
        if self.parent.parent.client.turn:
            if keys[pygame.K_UP]: 
                self.parent.parent.client.increaseBet()
            elif keys[pygame.K_DOWN]: 
                self.parent.parent.client.decreaseBet()
            elif keys[pygame.K_f]: 
                self.parent.parent.client.betting = 0
                self.parent.parent.client.fold()

        if self.paused:
            self.pauseMenu()
        if self.chatting:
            self.chatMenu()
        
    def remove(self):
        for i in self.potChips:
            i.remove()
        for i in self.chips:
            i.remove()
        self.removeCommunityCards()
        
        

if __name__ == '__main__':
    m = Main()

pygame.quit()
                                                
