#stuff to add
#win if player has 5 cards
#display the fith cards(ordering might be fucked?)
#opening screen
#dealer personalities
#players + personalities
from card import Card
from hand import Hand
from time import sleep
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
mainImg = pygame.image.load("main.png")
betImg = pygame.image.load("bet.png")
cardTemplate = pygame.image.load("card.png")
openingImg = pygame.image.load("opening.png")
bg = mainImg
cardTemplateY = 142.03/2
cardTemplateX = 87.885/2

#default options
shuffle_count = 100000
deck_size = 8
hands = []
dealerLimit = 18
bet = 0
game = True
opening = True
money = 1000
currentHand = 0
fontObject = pygame.font.SysFont("freesansbold.ttf", 60)

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
    textSurface = fontObject.render(text, True, color)
    textRectangle = textSurface.get_rect()
    textRectangle.center = x, y
    win.blit(textSurface, textRectangle)


def redrawWindow():
    global money
    #general
    win.blit(bg, [0, 0])
    #dealer
    textWrite("Dealer", 60, (255,255,255), 400, 40)
    showCards(1, 160)
    #textWrite(str(hands[1].printHand()).strip("[]"), 60, (255,255,255), 400, 100)
    #textWrite("Value: " + str(hands[1].getHandValue()), 60, (255,255,255), 400, 160)
    #player
    #textWrite(str(hands[0].printHand()).strip("[]"), 60, (255,255,255), 400, 540)
    #textWrite("Value: " + str(hands[0].getHandValue()), 60, (255,255,255), 400, 600)
    textWrite("Cash: " + str(money), 60, (255,255,255), 650, 40)
    showCards(0, 550)
    #split hand
    if hands[0].hasSplit == True:
        showCards(-1, 400)
    playerEvent()
    pygame.display.update()


def playerEvent():
    global money
    global bet
    global currentHand
    #bust
    if  hands[currentHand].bust == True:
        textWrite("Bust!", 60, (255,255,255), 400, 310)
        pygame.display.update()
        sleep(2)
        money = money - bet
        if currentHand == -1 or hands[0].hasSplit == False:
            if currentHand == -1:
                hands[0].hasSplit = False
            currentHand = 0
            makeBet()
            resetDeck(2)
            startHand()
        else:
            currentHand = -1
        hands[currentHand].bust = False
    #stand/win
    if hands[currentHand].stand == True:
        if hands[currentHand].hasSplit == True:
            currentHand = -1
            hands[0].stand = False
            textWrite("Stand!", 60, (255,255,255), 400, 310)
            sleep(2)
        elif hands[0].hasSplit == False or currentHand == -1:
            textWrite("Dealer's Turn!", 60, (255,255,255), 400, 270)
            pygame.display.update()
            sleep(2)
            if hands[1].multipleHits(dealerLimit) == True:
                    hands[1].addCard(deck[0])
                    deck.pop(0)
            else:
                #win
                if hands[currentHand].getHandValue() > hands[1].getHandValue() or hands[1].getHandValue() > 21:
                    textWrite("You Win!", 60, (255,255,255), 400, 310)
                    money = money + bet
                #lose
                elif hands[currentHand].getHandValue() < hands[1].getHandValue() and hands[1].getHandValue() < 22:
                    textWrite("You Lose!", 60, (255,255,255), 400, 310)
                    money = money - bet
                #tie
                else:
                    textWrite("Tie!", 60, (255,255,255), 400, 310)
                pygame.display.update()
                hands[currentHand].stand = False
                currentHand = 0
                sleep(2)
                makeBet()
                resetDeck(2)
                startHand()
                hands[currentHand].stand = False
    #forfeit
    if hands[currentHand].forfeit == True:
        textWrite("Forfeit!", 60, (255,255,255), 400, 310)
        money = money - bet/2
        pygame.display.update()
        sleep(2)
        hands[currentHand].forfeit = False
        if currentHand == 0 and hands[0].hasSplit == True:
            currentHand = -1
        else:
            currentHand = 0
            resetDeck(2)
            startHand()
            makeBet()
        
    #double
    if hands[currentHand].double == True:
        textWrite("Double!", 60, (255,255,255), 400, 310)
        bet = bet*2
        hands[currentHand].addCard(deck[0])
        deck.pop(0)
        pygame.display.update()
        sleep(2)
        hands[currentHand].checkStand()
        hands[currentHand].double = False
    pygame.display.update()
    #split
    if hands[0].hasSplit == False:
        if hands[0].split == True:
            textWrite("Split!", 60, (255,255,255), 400, 310)
            pygame.display.update()
            sleep(2)
            hands.append(Hand())
            hands[-1].cards.append(hands[0].cards[1])
            del hands[0].cards[1]
            hands[0].hasSplit = True
            hands[0].split = False


def input(eventtype, event, x1, x2, y1 ,y2):
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if event.type == eventtype:
        if x1 < mx < x2:
            if y1 < my < y2:
                return True


def resetDeck(number):
    hands.clear()
    deck.clear()
    createDeck()
    shuffle(deck)
    for i in range(number):
        hands.append(Hand())


def startHand():
    for hand in hands:
        for i in range(2):
            hand.addCard(deck[0])
            deck.pop(0)


def makeBet():
    global bet
    win.blit(betImg, [0, 0])
    textWrite("Make Your Bet!", 60, (255,255,255), 400, 460)
    chooseBet = True
    pygame.display.update()
    
    while chooseBet == True:

        clock.tick(27)
        mx, my = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    chooseBet = False
                    pygame.quit()
                    quit()

            elif input(pygame.MOUSEBUTTONDOWN, event, 100, 200, 650, 700) == True:
                bet = 10
                chooseBet = False

            elif input(pygame.MOUSEBUTTONDOWN, event, 225, 325, 650, 700) == True:
                bet = 20
                chooseBet = False

            elif input(pygame.MOUSEBUTTONDOWN, event, 350, 450, 650, 700) == True:
                bet = 50
                chooseBet = False
            
            elif input(pygame.MOUSEBUTTONDOWN, event, 475, 575, 650, 700) == True:
                bet = 100
                chooseBet = False
            
            elif input(pygame.MOUSEBUTTONDOWN, event, 600, 700, 650, 700) == True:
                bet = 200
                chooseBet = False


def showCards(handNum, cardY):
    cardAmount = len(hands[handNum].cards)
    hands[handNum].printHand()
    if cardAmount == 1:
        win.blit(cardTemplate, (400-cardTemplateX,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 400, cardY)
    if cardAmount == 2:
        win.blit(cardTemplate, (350-cardTemplateX,cardY-cardTemplateY))
        win.blit(cardTemplate, (450-cardTemplateX,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 350, cardY)
        textWrite(str(hands[handNum].hand[1]), 50, (0,0,0), 450, cardY)
    elif cardAmount == 3:
        win.blit(cardTemplate, (300-cardTemplateX,cardY-cardTemplateY))
        win.blit(cardTemplate, (400-cardTemplateX,cardY-cardTemplateY))
        win.blit(cardTemplate, (500-cardTemplateX,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 300, cardY)
        textWrite(str(hands[handNum].hand[1]), 50, (0,0,0), 400, cardY)
        textWrite(str(hands[handNum].hand[2]), 50, (0,0,0), 500, cardY)
    elif cardAmount == 4:
        win.blit(cardTemplate, (250-cardTemplateX,cardY-cardTemplateY))
        win.blit(cardTemplate, (350-cardTemplateX,cardY-cardTemplateY))
        win.blit(cardTemplate, (450-cardTemplateX,cardY-cardTemplateY))
        win.blit(cardTemplate, (550-cardTemplateX,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 250, cardY)
        textWrite(str(hands[handNum].hand[1]), 50, (0,0,0), 350, cardY)
        textWrite(str(hands[handNum].hand[2]), 50, (0,0,0), 450, cardY)
        textWrite(str(hands[handNum].hand[2]), 50, (0,0,0), 550, cardY)


while opening == True:

    clock.tick(27)
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    win.blit(openingImg, [0, 0])
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                game = False
                pygame.quit()
                quit()
    
        if input(pygame.MOUSEBUTTONDOWN, event, 300, 500, 300, 500) == True:
            opening = False

resetDeck(2)
startHand()
makeBet()

while game == True:

    clock.tick(27)
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                game = False
                pygame.quit()
                quit()

        #double
        if input(pygame.MOUSEBUTTONDOWN, event, 100, 200, 650, 700) == True:
            hands[currentHand].checkDouble()

        #split
        elif input(pygame.MOUSEBUTTONDOWN, event, 225, 325, 650, 700) == True:
            hands[0].checkSplit()

        #hit
        elif input(pygame.MOUSEBUTTONDOWN, event, 350, 450, 650, 700) == True:
            if hands[currentHand].getHandValue() < 21 and hands[currentHand].stand == False:
                hands[currentHand].addCard(deck[0])
                deck.pop(0)
        
        #stand
        elif input(pygame.MOUSEBUTTONDOWN, event, 475, 575, 650, 700) == True:
            hands[currentHand].checkStand()

        #forfeit
        elif input(pygame.MOUSEBUTTONDOWN, event, 600, 700, 650, 700) == True:
            hands[currentHand].checkForfeit()

    hands[currentHand].checkBust()
    hands[currentHand].checkWin()
    redrawWindow()
