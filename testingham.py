import random, pygame

screenSize = (800, 800)
pygame.init()
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("poke you")
clock = pygame.time.Clock()

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

sprites = []


class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.name = values[self.value] + " of " + self.suit


class Deck():
    def __init__(self):
        self.regenDeck()
        
    def getCard(self):
        self.choice = random.choice(self.deck)
        self.deck.pop(self.deck.index(self.choice))
        return self.choice
    
    def regenDeck(self):
        self.deck = []
        for suit in suits:
            for value in range(1, 14):
                self.deck.append(Card(suit, value))
        

class Player():
    def __init__(self):
        self.hand = []
        
        
class Menu():
    def __init__(self):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, text='Die', font='Calibri', dim=[100,50], xy=[0,0], textColour=[0, 0, 0], buttonColour=[122, 122, 122], function=None, multiClick=False, group=sprites):
        self.buttonText = text
        self.font = pygame.font.SysFont(font,35)
        self.buttonDim = dim
        self.xy = xy
        self.textColour = textColour
        self.buttonColour = buttonColour
        self.buttonActive = self.getButtonColours()
        self.multiClick = multiClick
        self.function = function
        self.pressed = False
        self.group = group
        
        self.buttonSurface = pygame.Surface((self.buttonDim[0], self.buttonDim[1]))
        self.rect = self.buttonSurface.get_rect(center=(self.xy[0], self.xy[1]))

        self.text = self.font.render(self.buttonText, True, self.textColour)
        
        self.group.append(self)
        super().__init__()
        
        
    def render(self):
        mouse = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.buttonColour)
        if self.rect.collidepoint(mouse):
            self.buttonSurface.fill(self.buttonActive[0])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.buttonActive[1])
                if self.multiClick and self.function:
                    self.function()
                elif not self.pressed and self.function:
                    self.function()
                    self.pressed = True
            else:
                self.pressed = False
        self.buttonSurface.blit(self.text, [self.rect.width/2 - self.text.get_rect().width/2, self.rect.height/2 - self.text.get_rect().height/2])
        screen.blit(self.buttonSurface, self.rect)
        
    def getButtonColours(self):
        highlight = []
        click = []
        for value in self.buttonColour:
            highlight.append(value + 50)
            click.append(value - 50)
        return [highlight, click]
        
    def remove(self):
        if self in self.group:
            self.group.remove(self)
            self.kill()
        else:
            print('Im already gone')
        

class Image(pygame.sprite.Sprite):
    def __init__(self, image='gameoil.jpg', xy=[0,0], dim=[100,100], group=sprites):
        self.graphic = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.graphic, (dim[0], dim[1]))
        self.xy = xy
        self.dim = dim
        self.group = group
        self.rect = self.image.get_rect(center=(self.xy[0], self.xy[1]))
        
        self.group.append(self)
        super().__init__()
        
    def render(self):
        screen.blit(self.image, self.rect)
        
    def update(self, image):
        self.image = pygame.transform.scale(self.graphic, (dim[0], dim[1]))
        self.rect = self.image.get_rect(center=(self.xy[0], self.xy[1]))
    
    def remove(self):
        if self in self.group:
            self.group.remove(self)
            self.kill()
        else:
            print('Im already gone')
            
            
# class ImageButton(Image, Button):
#     def __init__(self, dim=[100,50], xy=[0,0], function=None, multiClick=False, image='gameoil.jpg', group=sprites):
#         self.graphic = pygame.image.load(image).convert_alpha()
#         self.image = pygame.transform.scale(self.graphic, (dim[0], dim[1]))
#         self.xy = xy
#         self.dim = dim
#         self.group = group
#         self.rect = self.image.get_rect(center=(self.xy[0], self.xy[1]))
#         self.buttonActive = self.getButtonColours()
#         self.multiClick = multiClick
#         self.function = function
#         self.pressed = False
#         
#         self.group.append(self)
#         super().__init__()
        
        


d = Deck()
p = Player()
# i = ImageButton()

for i in range(7):
    p.hand.append(d.getCard())
   
   
background = (255, 255, 255)

def stop():
    global running
    running = False
    
def settings():
    global screenSize
    global sprites
    sprites = []
    b1 = Button(xy=[screenSize[0]/2, 150], function=None, text='Setting 1', dim=[200, 50], group=sprites)
    b2 = Button(xy=[screenSize[0]/2, 200], function=None, text='Setting 2', dim=[200, 50], group=sprites)
    b3 = Button(xy=[screenSize[0]/2, 250], function=mainMenu, text='Back', dim=[200, 50], group=sprites)

def mainMenu():
    global screenSize
    global sprites
    sprites = []
    logo = Image(xy=[screenSize[0]/2, 100], dim=[50,50], group=sprites)
    b1 = Button(xy=[screenSize[0]/2, 150], function=None, text='Play', dim=[200, 50], group=sprites)
    b2 = Button(xy=[screenSize[0]/2, 200], function=settings, text='Settings', dim=[200, 50], group=sprites)
    b3 = Button(xy=[screenSize[0]/2, 250], function=stop, text='Quit', dim=[200, 50], group=sprites)

   
mainMenu()

running = True
while running:
    screen.fill(background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
    for sprite in sprites:
        sprite.render()
                
    pygame.display.flip()
pygame.quit()