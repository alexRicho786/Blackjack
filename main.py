#stuff to add
#from dealer hand append hand to a list and have one of them
#working inputs
#opening screen
#dealer personalities
#player personalities
from card import Card
from hand import Hand
import random
import pygame

#pygame init
pygame.init()
screenwidth = 800
screenheight = 800
win = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

#images
mainimg = pygame.image.load("main.png")
bg = mainimg

#default options
shuffle_count = 100000
deck_size = 8

game = True
deck = []
suits = ["S","C","H","D"]
faces = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
values = [11,2,3,4,5,6,7,8,9,10,10,10,10]


def createDeck():
    for d in range(1, deck_size):
        for s in suits:
            for i in range(12):
                is_ace = False
                if values[i] == 11:
                    is_ace = True
                card = Card(s, faces[i], values[i], is_ace)
                deck.append(card)


def shuffle(deck):
    # Note: Python has a random.shuffle() function that
    #       could also be used, however there is much
    #       less control over iterations

    global shuffle_count

    for i in range(shuffle_count):
        x = random.randint(0, len(deck)-1)
        y = random.randint(0, len(deck)-1)

        temp = deck[x]
        deck[x] = deck[y]
        deck[y] = temp


#text write func taken from stackoverflow 
#at https://stackoverflow.com/questions/45586690/pygame-text-function
def textWrite(text, size, color, x, y):
    fontObject = pygame.font.SysFont("freesansbold.ttf", size)
    textSurface = fontObject.render(text, True, color)
    textRectangle = textSurface.get_rect()
    textRectangle.center = x, y
    win.blit(textSurface, textRectangle)


def redrawWindow():
    win.blit(bg, [0, 0])
    textWrite(str(hand.printHand()).strip("[]"), 60, (255,255,255), 400, 540)
    textWrite("Value: " + str(hand.getHandValue()), 60, (255,255,255), 400, 600)
    pygame.display.update()


def input(eventtype, x1, x2, y1 ,y2):
    x, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if event.type == eventtype:
        if x1 < mx < x2:
            if y1 < my < y2:
                return True

createDeck()
shuffle(deck)

# The following shows how to create a hand, deal it 4
# cards and then print out the hand and the value of it
hand = Hand()

for i in range(2):
    hand.addCard(deck[0])
    print(deck[0].value, end=" ")
    deck.pop(0)

while game == True:

    clock.tick(27)
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                game = False
                pygame.quit()
                quit()

        if input(pygame.MOUSEBUTTONDOWN, 375, 425, 650, 700) == True:
            hand.addCard(deck[0])
            print(deck[0].value, end=" ")
            deck.pop(0)

    redrawWindow()
