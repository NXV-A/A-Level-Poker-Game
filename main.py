import random, pygame, pygame.locals, os, traceback, time, math, compare
from assetloader import *

settings = {
    "Fullscreen" : True,
    "Username" : "Bartholomew Montgomery Clyde",
    
}

class Main:
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
        
        self.localplayer = Player(self, username=settings['Username'])
        
        
        if settings["Fullscreen"]:
            self.window = pygame.display.set_mode(self.size, pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.window = pygame.display.set_mode((int(self.width / 2), self.height-50), pygame.RESIZABLE)
            self.size = [int(self.Width / 2), self.height - 50]
            self.width = self.size[0]
            self.height = self.size[1]
            
        self.grey = (20, 20, 20)
        self.green = (15, 138, 19)
            
        self.load()
        
        
        
        pygame.display.set_caption("poke you")
        pygame.display.set_icon(self.images['Poker icon'])
        
        self.mainMenu()
        
        self.loop()
       
        
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    

                if self.game: 
                    if event.key == pygame.K_SPACE:
                        self.game.mainPlayer.flipHand()
                    elif event.key == pygame.K_c:
                        self.game.showCommunityCards()
                    elif event.key == pygame.K_UP:
                        self.localplayer.increaseBet()
                    elif event.key == pygame.K_DOWN:
                        self.localplayer.decreaseBet()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    pos = pygame.mouse.get_pos()
                    buttonPressed = False
                    for object in self.objects:
                        if type(object) == Button:
                            if object.rect.collidepoint(pos) and not buttonPressed:
                                object.call_back()
                                buttonPressed = True
                                
            # if self.game:
            #     if event.type == self.game.gamingEvent:
            #         print('Hello Mate')
                

    def quit(self):
        self.running = False
                            
    def render(self):
        self.window.fill(self.background)
        self.sprites.draw(self.window)
     
    def removeAllSprites(self):
        self.sprites.empty()
        for object in self.objects:
            object.remove()
        self.objects = []
                            
    def load(self):
        for (name, group) in imgGroups.items():
            for item in group:
                ext = ".png"
                splitted = item.split(".")
                if len(splitted) > 1:
                    item = splitted[0]
                    ext = "." + splitted[1]
                    
                self.images[item] = pygame.image.load(os.path.join(name, item + ext)).convert_alpha()
                
                
    def mainMenu(self):
        self.removeAllSprites()
        self.background = self.grey
        self.logo = Image(self, xy=[self.width/2 - 25, 75], dim=[50,50], group=self.sprites, image=self.images['Poker icon'])
        self.b1 = Button(self, xy=[self.width/2, 150], function=self.modeSelect, text='Play', dim=[200, 50], group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 200], function=self.settingsMenu, text='Settings', dim=[200, 50], group=self.objects)
        self.b3 = Button(self, xy=[self.width/2, 250], function=self.quit, text='Quit', dim=[200, 50], group=self.objects)
        self.qr = Image(self, xy=[self.width/2, 350], dim=[58,58], group=self.sprites, image=self.images['QR'])

    def settingsMenu(self):
        self.removeAllSprites()
        self.background = self.grey
        self.b1 = Button(self, xy=[self.width/2, 150], function=None, text='Setting 1', dim=[200, 50], group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 200], function=None, text='Setting 2', dim=[200, 50], group=self.objects)
        self.b3 = Button(self, xy=[self.width/2, 250], function=self.mainMenu, text='Back', dim=[200, 50], group=self.objects)

    def modeSelect(self):
        self.removeAllSprites()
        self.background = self.grey
        self.logo = Image(self, xy=[self.width/2 - 25, 75], dim=[50,50], group=self.sprites, image=self.images['Poker icon'])
        self.b1 = Button(self, xy=[self.width/2, 150], function=self.singleplayer, text='Singleplayer', dim=[200, 50], group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 200], function=self.joinOrCreate, text='Multiplayer', dim=[200, 50], group=self.objects)
        self.b3 = Button(self, xy=[self.width/2, 250], function=self.mainMenu, text='Back', dim=[200, 50], group=self.objects)
        self.qr = Image(self, xy=[self.width/2, 350], dim=[58,58], group=self.sprites, image=self.images['QR'])


    def joinOrCreate(self):
        self.removeAllSprites()
        self.background = self.grey
        self.logo = Image(self, xy=[self.width/2 - 25, 75], dim=[50,50], group=self.sprites, image=self.images['Poker icon'])
        self.b1 = Button(self, xy=[self.width/2, 150], text='Join a lobby', dim=[200, 50], group=self.objects)
        self.b2 = Button(self, xy=[self.width/2, 200], function=self.removeAllSprites, text='Create a lobby', dim=[200, 50], group=self.objects)
        self.b3 = Button(self, xy=[self.width/2, 250], function=self.modeSelect, text='Back', dim=[200, 50], group=self.objects)
        self.qr = Image(self, xy=[self.width/2, 350], dim=[58,58], group=self.sprites, image=self.images['QR'])


    def singleplayer(self):
        self.removeAllSprites()
        self.background = self.green
        self.players = [self.localplayer, Bot(self), Bot(self), Bot(self), Bot(self)]
        self.game = Game(self, gametype="Singleplayer", players=self.players)


    def updateObjects(self):
        for object in self.objects:
            object.update()
                            

    def loop(self):
        while self.running:
            self.dt = self.clock.tick(100) / 1000
            self.events()
            self.render()
            self.updateObjects()
            pygame.display.flip()
        pygame.quit()
        exit()

class Player():
    def __init__(self, parent, username='nothing', hand=[None, None], money=[10, 5, 3, 2, 1]):
        self.parent = parent
        self.username = username
        self.hand = hand
        self.role = None # Player, Dealer, Small Blind, Big Blind
        self.validRoles = ['Player', 'Dealer', 'Small Blind', 'Big Blind']
        self.money = money
        self.overallMoney = self.calculateMoney()
        self.betting = 0
        self.folded = False

    def setRole(self, role):
        if role in self.validRoles:
            self.role = role
        else:
            print('Invalid Role')

    def getUsername(self):
        return self.username
    
    def getHand(self):
        return self.hand
    
    def getRole(self):
        return self.role
    
    def promptAction(self):
        pass
    
    def bet(self, amount):
        for i in amount:
            pass

    def calculateMoney(self):
        value = 1
        money = 0
        for i in self.money:
            amount = value * i
            money += amount
            value *= 2
        return money

    def increaseBet(self):
        if not self.betting + 1 > self.calculateMoney():
            self.betting += 1

    def decreaseBet(self):
        if not self.betting - 1 < 0:
            self.betting -= 1
            
    def fold(self):
        self.folded = True
        
        
#         self.info = playerInfo(username=self.username, xy=[parent.width/20, parent.height/12])

class Bot(Player):
    def __init__(self, parent, username='nothing', hand=[None, None]):
        super().__init__(parent, username="Mr Reghif")


class Game():
    def __init__(self, parent, gametype=None, players=[], bots=None):
        self.parent = parent
        self.gametype = gametype
        self.Players = players
        self.font = pygame.font.SysFont('Calibri',35)
        self.textColour = [0, 0, 0]
        self.bots = bots
        self.gameStart = pygame.time.get_ticks()
        self.pot = [0, 0, 0, 0, 0]
        self.communityCards = []
        self.lastbet = 0
        
        self.deck = Deck(self.parent)
        
        # self.currentPlayer = self.Players[0]

        if self.gametype == "Singleplayer":
            # self.bots = [Bot()] * 5
            print(self.bots)
        elif self.gametype == "Multiplayer":
            print('Ok')
        else:
            print('you have gone and buggered and truggered up the game')
        
        self.mainPlayer = mainPlayerUI(self, size=100, picture=self.parent.images['gameoil'], username=self.parent.localplayer.getUsername())
        
        self.drawCommunityCards()
        
        
        self.startGame()
        
    def startGame(self):
        self.gameStartText = 'Game starts in:'
        self.startingTime = 0.
        self.currentTime = 0
#         while self.currentTime <= self.startingTime:
#             self.currentTime = math.floor((pygame.time.get_ticks() - self.gameStart) / 1000)
#             self.gameStartRendered = self.font.render(self.gameStartText + str(self.startingTime - self.currentTime) , True, self.textColour)
#             self.parent.window.blit(self.gameStartRendered, (self.parent.width/2, 20))
        self.gamingEvent = pygame.locals.USEREVENT + 1
        pygame.time.set_timer(self.gamingEvent, 20000)
        
    def drawCommunityCards(self):
        self.emptyCards = []
        self.xy = [self.parent.width /2, 30]
        for card in self.communityCards:
            card.setXY(self.xy)
            card.show()
            self.xy[0] += 70
        for card in range(5 - len(self.communityCards)):
            blankCard = Card(self.parent, None, None)
            blankCard.setXY(self.xy)
            blankCard.show()
            blankCard.switch()
            self.emptyCards.append(blankCard)
            self.xy[0] += 70
            
    def removeCommunityCards(self):
        for blank in self.emptyCards:
            blank.remove()
        self.emptyCards = []
        for card in self.communityCards:
            card.hide()

        
    def showCommunityCards(self):
        self.removeCommunityCards()
        if len(self.communityCards) == 0:
            for i in range(3):
                self.communityCards.append(self.deck.getCard())
        elif len(self.communityCards) == 3:
            self.communityCards.append(self.deck.getCard())
        elif len(self.communityCards) == 4:
            self.communityCards.append(self.deck.getCard())
        else:
            print('You have gone and buggered and truggered up the game')
        
        self.drawCommunityCards()

    def haveAGo(self):
        pass
    
    def nextPlayer(self):
        print('mate')
    
    def drawPlayers(self):
        pass
    
    def checkClock(self):
        pass
        
        

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
        
        
    def switch(self):
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
            
    def getValue(self):
        return self.value
    
    def setValue(self, nValue):
        self.value = nValue
        
    def getName(self):
        return self.name
    
    def getValueName(self):
        return self.values[self.value]
    
    def setName(self):
        self.name = values[self.value] + " of " + self.suit
        
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
        
    def hide(self):
        self.image.kill()
        
    def remove(self):
        self.image.kill()
        del self

class Deck():
    def __init__(self, parent):
        self.suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.parent = parent
        self.regenDeck()
        
    def getCard(self):
        self.choice = random.choice(self.deck)
        self.deck.pop(self.deck.index(self.choice))
        return self.choice
    
    def regenDeck(self):
        self.deck = []
        for suit in self.suits:
            for value in range(1, 14):
                self.deck.append(Card(self.parent, suit, value))
        

class Button():
    def __init__(self, parent, text='Die', font='Calibri', dim=[100,50], xy=[0,0], textColour=[0, 0, 0], buttonColour=[122, 122, 122], function=None, group=None):
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
    
    def call_back(self, *args):
        self.buttonColour = self.buttonActive[2]
        if self.function:
            return self.function(*args)
        
    def remove(self):
        global buttonList
        if self in self.group:
            self.group.remove(self)
        else:
            print('Im already gone')
            
        

class Image(pygame.sprite.Sprite):
    def __init__(self, parent, image=None, xy=[0,0], dim=[100,100], group=None):
        super().__init__()
        self.parent = parent
        self.graphic = image
        self.image = pygame.transform.scale(self.graphic, (dim[0], dim[1]))
        self.xy = xy
        self.dim = dim
        self.group = parent.sprites
        self.rect = self.image.get_rect(topleft=(self.xy[0], self.xy[1]))
        
        self.group.add(self)
        
    def update(self, image):
        self.graphic = image
        self.image = pygame.transform.scale(self.graphic, (self.dim[0], self.dim[1]))
        self.rect = self.image.get_rect(topleft=(self.xy[0], self.xy[1]))
    
    def remove2(self):
        if self in self.group:
            self.group.remove(self)
            self.kill()
        else:
            print('Im already gone')


class playerInfo():
    def __init__(self, parent, username='teams', picture=None, money=[5, 5, 5, 5, 5], hand=[None, None], xy=[100, 100], font='Calibri', textColour=[0,0,0], size=100):
        self.parent = parent
        self.xy = xy
        self.money = money
        self.hand = hand
        self.username = username
        self.graphic = picture
        self.group = self.parent.objects
        self.size = size
        
        self.drawChips()
        
        self.group.append(self)

        self.textColour = textColour
        self.font = pygame.font.SysFont(font, int(self.size * 0.35))
        self.text = self.font.render(self.username, True, self.textColour)
        
        self.profilePicture = Image(self.parent, image=self.graphic, xy=self.xy, dim=[self.size, self.size])
        
    def drawChips(self):
        value = 1
        chipSpacingX = self.size / 4
        chipSpacingY = self.size / 50
        chipXY = [self.xy[0] + (self.size * 1.1),  self.xy[1] + (self.size / 2)]
        for index in self.money:
            for x in range(index):
                Image(self.parent, image=self.parent.images[str(value)], xy=(chipXY[0], chipXY[1]), dim=[self.size / 4, self.size / 4])
                chipXY[1] -= chipSpacingY
            chipXY[0] += chipSpacingX
            chipXY[1] = self.xy[1] + (self.size / 2)
            value *= 2
        
    def update(self):
        self.parent.window.blit(self.text, (self.xy[0] + (self.size * 1.1), self.xy[1]), )
        
    def remove2(self):
        if self in self.group:
            self.group.remove(self)
        else:
            print('Im already gone')
        
    
      
      
class mainPlayerUI():
    def __init__(self, parent, username='teams', picture=None, money=[10, 5, 3, 2, 1], hand=[None, None], font='Calibri', textColour=[0,0,0], size=100):
        self.parent = parent
        self.size = 100
        self.xy = [parent.parent.width/2 - self.size * 2.5, 3 * parent.parent.height / 4]
        self.money = money
        self.hand = [self.parent.deck.getCard(), self.parent.deck.getCard()]
        self.overallHand = []
        self.username = username
        self.graphic = picture
        self.group = self.parent.parent.objects
        self.group.append(self)
        self.handShown = 0
        
        self.textColour = textColour
        self.font = pygame.font.SysFont(font, int(self.size * 0.35))

        self.bettingAmount = 0
        self.action = "Check"
        self.foldAction = "Fold"
        self.handAction = "Check Hand"
        self.handName = ''
        self.timeElapsed = '0'
        self.foldActionText = self.font.render(self.foldAction, True, self.textColour)
        self.handActionText = self.font.render(self.handAction, True, self.textColour)
        
        self.drawSelfPlayerInfo()
        self.drawControls()
        self.drawHand()
        self.drawPlayers()

        # group.append(self)
        
    def drawSelfPlayerInfo(self):
        self.profilePicture = Image(self.parent.parent, image=self.graphic, xy=self.xy, dim=[self.size, self.size])
        self.text = self.font.render(self.username, True, self.textColour)
        self.drawChips()
        
        
    def drawChips(self):
        value = 1
        chipSpacingX = self.size / 1.5
        chipSpacingY = 4 * self.size / 80
        chipXY = [self.xy[0] + (self.size * 1.1),  self.xy[1] + (self.size / 1.5)]
        self.chips = []
        for index in self.money:
            for x in range(index):
                self.chips.append(Image(self.parent.parent, image=self.parent.parent.images[str(value)], xy=(chipXY[0], chipXY[1]), dim=[self.size / 1.5, self.size / 1.5]))
                chipXY[1] -= chipSpacingY
            chipXY[0] += chipSpacingX
            chipXY[1] = self.xy[1] + (self.size / 1.5)
            value *= 2

    def drawControls(self):
        self.xpos = self.parent.parent.width
        self.ypos = self.parent.parent.height - 160
        self.upArrow = Image(self.parent.parent, image=self.parent.parent.images['Up'],xy=[self.xpos - 40, self.ypos] , dim=[40, 40])
        self.downArrow = Image(self.parent.parent, image=self.parent.parent.images['Down'], xy=[self.xpos - 80, self.ypos], dim=[40, 40])
        self.enter = Image(self.parent.parent, image=self.parent.parent.images['Enter'], xy=[self.xpos - 40, self.ypos + 40], dim=[40, 40])
        self.fKey = Image(self.parent.parent, image=self.parent.parent.images['F'], xy=[self.xpos - 40, self.ypos + 80], dim=[40, 40])
        self.spacebar = Image(self.parent.parent, image=self.parent.parent.images['Space'], xy=[self.xpos - 40, self.ypos + 120], dim=[40, 40])
        
    def drawHand(self):
        print('set your shit')
        card1 = self.hand[0]
        card2 = self.hand[1]
        card1.setXY([self.parent.parent.width/2 - 100, self.parent.parent.height - 100])
        card2.setXY([self.parent.parent.width/2 - 30, self.parent.parent.height - 100])
        card1.show()
        card2.show()
        card1.switch()
        card2.switch()
#         cardXY = [self.parent.parent.width/2 - 100, self.parent.parent.height - 100]
#         for card in self.hand:
#             card.setXY(cardXY)
#             card.show()
#             card.switch()
#             
#             cardXY[0] += 70
#             print('its been added')
            
    def drawPlayers(self):
        players = self.parent.Players
        playerPositions = [
            [self.parent.parent.width/20, self.parent.parent.height/12],
            [self.parent.parent.width/20, self.parent.parent.height/2],
            [self.parent.parent.width - self.parent.parent.width/5, self.parent.parent.height/2],
            [self.parent.parent.width - self.parent.parent.width/5, self.parent.parent.height/12]
        ]
        self.playerDisplays = []
        
        for playerNumber in range(len(players)):
            if players[playerNumber] != self.parent.parent.localplayer:
                playerCrap = playerInfo(self.parent.parent, username=players[playerNumber].getUsername(), picture=self.parent.parent.images['teams'], xy=playerPositions[playerNumber - 1])
                self.playerDisplays.append(playerCrap)
            
#         self.player1 = playerInfo(self.parent, username='player1', picture=parent.images['teams'], xy=)
#         self.player2 = playerInfo(self.parent, username='player2', picture=parent.images['teams'], xy=)
#         self.player3 = playerInfo(self.parent, username='player3', picture=parent.images['teams'], xy=)
#         self.player4 = playerInfo(self.parent, username='player4', picture=parent.images['teams'], xy=)
            
    def flipHand(self):
        self.cardXY = [self.parent.parent.width/2 - 70, self.parent.parent.height - 100]
        if self.handShown == 0:
            self.handShown = 1
        else:
            self.handShown = 0
        for card in self.hand:
            card.switch()
#         self.cardXY = [self.parent.width/2 - 70, self.parent.height - 100]
#         for card in self.hand:
#             card.setXY(self.cardXY)
#             card.switch()
#             
#             self.cardXY[0] += 70

    def getTime(self):
        self.timeInMs = pygame.time.get_ticks() - self.parent.gameStart
        self.timeInS = math.floor(self.timeInMs / 1000)
        self.minutesElapsed = math.floor(self.timeInS/60)
        self.hoursElapsed = math.floor(self.minutesElapsed/60)
        
        self.timer = str(self.hoursElapsed) + ":" + str(self.minutesElapsed - (self.hoursElapsed * 60)) + ":" + str(self.timeInS - (self.minutesElapsed * 60))
        return self.timer
        
    def update(self):
        self.overallHand = self.hand + self.parent.communityCards
        keys = pygame.key.get_pressed()
        
        self.betText = self.font.render(("£" + str(self.parent.parent.localplayer.betting)), True, self.textColour)
        if self.parent.lastbet == self.parent.parent.localplayer.betting:
            self.betPromptText = self.font.render("Call", True, self.textColour)
        elif self.parent.lastbet < self.parent.parent.localplayer.betting:
            self.betPromptText = self.font.render("Raise", True, self.textColour)
        elif self.parent.parent.localplayer.betting == 0:
            self.betPromptText = self.font.render("Check", True, self.textColour)
        self.timeText = self.font.render(self.getTime(), True, self.textColour)
        self.betTextRect = self.betText.get_rect()
        self.betPromptRect = self.betPromptText.get_rect()
        self.parent.parent.window.blit(self.text, (self.xy[0] + (self.size * 1.1), self.xy[1]))
        self.parent.parent.window.blit(self.betText, (self.xpos - self.betTextRect.width - 85, self.ypos))
        self.parent.parent.window.blit(self.betPromptText, (self.xpos - self.betPromptRect.width - 45, self.ypos + 40))
        self.parent.parent.window.blit(self.foldActionText, (self.xpos - 105, self.ypos + 80))
        self.parent.parent.window.blit(self.handActionText, (self.xpos - 210, self.ypos + 120))
        self.parent.parent.window.blit(self.timeText, (self.parent.parent.width/2, 0))
        
        if self.handShown == 1:
            self.handValue = compare.getValueOfHand(self.parent, self.overallHand)
            self.handName = compare.valueToName(self.parent, self.handValue)
            self.handNameText = self.font.render(self.handName, True, self.textColour)
            self.handNameTextRect = self.handNameText.get_rect()
            self.parent.parent.window.blit(self.handNameText, (self.parent.parent.width/2 - (self.handNameTextRect.width /2), (self.parent.parent.height * 9/10) - self.handNameTextRect.height))
            
            
        fpsText = self.font.render(str(int(self.parent.parent.clock.get_fps())), True, self.textColour)
        self.parent.parent.window.blit(fpsText, (0, 0))
        
        

if __name__ == '__main__':
    Main()

pygame.quit()
