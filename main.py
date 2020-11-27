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
cardTemplateY = 113.1165/2
cardTemplateX = 70.0245/2

#default options
shuffle_count = 100000
deck_size = 8
hands = []
dealerLimit = 18
harmonLimit = 20
maxwellLimit = 16
bet = 50
game = True
opening = True
dealerShow = False
currentEvent = "Your Turn!"
money = 1000
currentHand = 0
fontObject = pygame.font.SysFont("freesansbold.ttf", 50)
harmonButton = 1

deck = []
suits = ["S","C","H","D"]
faces = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
values = [11,2,3,4,5,6,7,8,9,10,10,10,10]

#creates the deck
def createDeck():
    for d in range(1, deck_size):
        for s in suits:
            for i in range(12):
                is_ace = False
                if values[i] == 11:
                    is_ace = True
                card = Card(s, faces[i], values[i], is_ace)
                deck.append(card)


#shuffles the deck
def shuffle(deck):
    global shuffle_count

    for i in range(shuffle_count):
        x = random.randint(0, len(deck)-1)
        y = random.randint(0, len(deck)-1)

        temp = deck[x]
        deck[x] = deck[y]
        deck[y] = temp


#text write function taken from stackoverflow 
#at https://stackoverflow.com/questions/45586690/pygame-text-function
def textWrite(text, size, color, x, y):
    textSurface = fontObject.render(text, True, color)
    textRectangle = textSurface.get_rect()
    textRectangle.center = x, y
    win.blit(textSurface, textRectangle)


#redraws the window every frame
def redrawWindow():
    global money
    #general
    win.fill((0,0,0))
    win.blit(bg, [0, 0])
    textWrite(currentEvent, 60, (255,255,255), 150, 40)
    #dealer
    textWrite("Dealer", 60, (255,255,255), 400, 40)
    showCards(1, 180, 0, dealerShow)
    #player
    textWrite("Cash: " + str(money), 60, (255,255,255), 650, 40)
    showCards(0, 580, 0, True)
    #other players
    showCards(2, 320, 225, True)
    showCards(3, 320, -225, True)
    #split hand
    if hands[0].hasSplit == True:
        showCards(-1, 450, 0, True)
    #general events
    playerEvent()
    #update screen
    pygame.display.update()


#different events eg: stand, split, hit, etc
def playerEvent():
    global dealerShow
    global money
    global bet
    global currentHand
    #bust
    if  hands[currentHand].bust == True:
        currentEvent = "Bust!"
        textWrite(currentEvent, 60, (255,255,255), 150, 70)
        pygame.display.update()
        sleep(2)
        money = money - bet
        if currentHand == -1 or hands[0].hasSplit == False:
            if currentHand == -1:
                hands[0].hasSplit = False
            currentHand = 0
            makeBet()
            resetDeck(4)
            startHand()
        else:
            currentHand = -1
        hands[currentHand].bust = False
    #stand/win
    if hands[currentHand].stand == True:
        if hands[currentHand].hasSplit == True:
            currentHand = -1
            hands[0].stand = False
            currentEvent = "Stand!"
            textWrite(currentEvent, 60, (255,255,255), 150, 70)
            pygame.display.update()
            sleep(2)
        elif hands[0].hasSplit == False or currentHand == -1:
            dealerShow = True
            currentEvent = "Dealer's Turn!"
            textWrite(currentEvent, 60, (255,255,255), 150, 70)
            pygame.display.update()
            sleep(2)
            if hands[2].multipleHits(harmonLimit) == True:
                    hands[2].addCard(deck[0])
                    deck.pop(0)
            elif hands[3].multipleHits(maxwellLimit) == True:
                    hands[3].addCard(deck[0])
                    deck.pop(0)
            elif hands[1].multipleHits(dealerLimit) == True:
                    hands[1].addCard(deck[0])
                    deck.pop(0)
            else:
                if hands[0].hasSplit == False:
                    #win
                    if hands[currentHand].getHandValue() > hands[1].getHandValue() or hands[1].getHandValue() > 21:
                        currentEvent = "You Win!"
                        textWrite(currentEvent, 60, (255,255,255), 150, 100)
                        money = money + bet
                    #lose
                    elif hands[currentHand].getHandValue() < hands[1].getHandValue() and hands[1].getHandValue() < 22:
                        currentEvent = "You Lose!"
                        textWrite(currentEvent, 60, (255,255,255), 150, 100)
                        money = money - bet
                    #tie
                    else:
                        currentEvent = "Tie!"
                        textWrite(currentEvent, 60, (255,255,255), 150, 100)
                #calculates winnings if the player has split with both hands standing
                else:
                    splitTie = True
                    #win x 2
                    if hands[0].getHandValue() > hands[1].getHandValue() or hands[1].getHandValue() > 21:
                        if hands[currentHand].getHandValue() > hands[1].getHandValue() or hands[1].getHandValue() > 21:
                            currentEvent = "You Win!"
                            textWrite(currentEvent, 60, (255,255,255), 150, 100)
                            money = money + bet*2
                            splitTie = False
                    #lose x 2
                    elif hands[0].getHandValue() < hands[1].getHandValue() and hands[1].getHandValue() < 22:
                        if hands[currentHand].getHandValue() < hands[1].getHandValue() and hands[1].getHandValue() < 22:
                            currentEvent = "You Lose!"
                            textWrite(currentEvent, 60, (255,255,255), 150, 100)
                            money = money - bet*2
                            splitTie = False
                    #win x 1
                    if hands[0].getHandValue() > hands[1].getHandValue() and hands[currentHand].getHandValue() == hands[1].getHandValue():
                        currentEvent = "You Win!"
                        textWrite(currentEvent, 60, (255,255,255), 150, 100)
                        money = money + bet
                    #win x 1
                    elif hands[currentHand].getHandValue() > hands[1].getHandValue() and hands[0].getHandValue() == hands[1].getHandValue():
                        currentEvent = "You Win!"
                        textWrite(currentEvent, 60, (255,255,255), 150, 100)
                        money = money + bet
                    #lose x 1
                    elif hands[0].getHandValue() < hands[1].getHandValue() and hands[currentHand].getHandValue() == hands[1].getHandValue():
                        currentEvent = "You Lose!"
                        textWrite(currentEvent, 60, (255,255,255), 150, 100)
                        money = money - bet
                    #lose x 1
                    elif hands[currentHand].getHandValue() < hands[1].getHandValue() and hands[0].getHandValue() == hands[1].getHandValue():
                        currentEvent = "You Lose!"
                        textWrite(currentEvent, 60, (255,255,255), 150, 100)
                        money = money - bet
                    #tie - tie - one wine one lose
                    elif splitTie == True:
                        currentEvent = "Tie!"
                        textWrite(currentEvent, 60, (255,255,255), 150, 100)

                pygame.display.update()
                hands[currentHand].stand = False
                currentHand = 0
                sleep(2)
                makeBet()
                resetDeck(4)
                startHand()
                dealerShow = False
                hands[currentHand].stand = False
    #forfeit
    if hands[currentHand].forfeit == True:
        currentEvent = "Forfeit!"
        textWrite(currentEvent, 60, (255,255,255), 150, 70)
        money = money - bet/2
        pygame.display.update()
        sleep(2)
        hands[currentHand].forfeit = False
        if currentHand == 0 and hands[0].hasSplit == True:
            currentHand = -1
        else:
            currentHand = 0
            resetDeck(4)
            startHand()
            makeBet()
    #double
    if hands[currentHand].double == True:
        currentEvent = "Double!"
        textWrite(currentEvent, 60, (255,255,255), 150, 70)
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
            currentEvent = "Split!"
            textWrite(currentEvent, 60, (255,255,255), 150, 70)
            pygame.display.update()
            sleep(2)
            hands.append(Hand())
            hands[-1].cards.append(hands[0].cards[1])
            del hands[0].cards[1]
            hands[0].hasSplit = True
            hands[0].split = False


#when player has five cards they autowin
def winGame():
    global money
    #accounting for split
    if hands[0].split == False or currentHand == -1:
        currentEvent = "You Win - 5 cards!"
        textWrite(currentEvent, 60, (255,255,255), 150, 70)
        money = money + bet
        pygame.display.update()
        sleep(2)
        currentHand = 0
        resetDeck(4)
        startHand()
        makeBet()
    else:
        currentEvent = "You Win - 5 cards!"
        textWrite(currentEvent, 60, (255,255,255), 150, 70)
        money = money + bet
        pygame.display.update()
        sleep(2)
        currentHand = -1

#function for input events in pygame
def input(eventtype, event, x1, x2, y1 ,y2):
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if event.type == eventtype:
        if x1 < mx < x2:
            if y1 < my < y2:
                return True


#resets the deck
def resetDeck(number):
    hands.clear()
    deck.clear()
    createDeck()
    shuffle(deck)
    for i in range(number):
        hands.append(Hand())


#creates hands for each deck
def startHand():
    for hand in hands:
        for i in range(2):
            hand.addCard(deck[0])
            deck.pop(0)


#screen for player to make bets and determine computer players personality
def makeBet():
    global bet
    global dealerLimit
    global maxwellLimit
    global harmonButton
    chooseBet = True

    win.blit(betImg, [0, 0])
    textWrite("Make a Bet", 50, (255,255,255), 400, 600)
    pygame.display.update() 
    
    while chooseBet == True:

        clock.tick(27)
        mx, my = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        win.blit(betImg, [0, 0])
        textWrite("Make a Bet", 50, (255,255,255), 400, 600)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    chooseBet = False
                    pygame.quit()
                    quit()

            #start button
            elif input(pygame.MOUSEBUTTONDOWN, event, 200, 600, 400, 580) == True:
                chooseBet = False

            #different bet buttons
            elif input(pygame.MOUSEBUTTONDOWN, event, 50, 150, 630, 730) == True:
                bet = 10
            elif input(pygame.MOUSEBUTTONDOWN, event, 200, 300, 630, 730) == True:
                bet = 20
            elif input(pygame.MOUSEBUTTONDOWN, event, 350, 450, 630, 730) == True:
                bet = 50
            elif input(pygame.MOUSEBUTTONDOWN, event, 500, 600, 630, 730) == True:
                bet = 100
            elif input(pygame.MOUSEBUTTONDOWN, event, 650, 750, 630, 730) == True:
                bet = 200
            #different personalities
            #dealer
            elif input(pygame.MOUSEBUTTONDOWN, event, 310, 410, 125, 205) == True:
                dealerLimit = 20
            elif input(pygame.MOUSEBUTTONDOWN, event, 470, 570, 125, 205) == True:
                dealerLimit = 18
            elif input(pygame.MOUSEBUTTONDOWN, event, 625, 725, 125, 205) == True:
                dealerLimit = 16
            #harmon
            elif input(pygame.MOUSEBUTTONDOWN, event, 310, 410, 190, 270) == True:
                harmonButton = 1
            elif input(pygame.MOUSEBUTTONDOWN, event, 470, 570, 190, 270) == True:
                harmonButton = 2
            elif input(pygame.MOUSEBUTTONDOWN, event, 625, 725, 190, 270) == True:
                harmonButton = 3
            #maxwell
            elif input(pygame.MOUSEBUTTONDOWN, event, 310, 410, 265, 355) == True:
                maxwellLimit = 20
            elif input(pygame.MOUSEBUTTONDOWN, event, 470, 570, 265, 355) == True:
                maxwellLimit = 18
            elif input(pygame.MOUSEBUTTONDOWN, event, 625, 725, 265, 355) == True:
                maxwellLimit = 16

        #display user feedback for bet
        if bet == 10:
            pygame.draw.rect(win, (0,255,0),(50, 735, 100, 10))
        elif bet == 20:
            pygame.draw.rect(win, (0,255,0),(200, 735, 100, 10))
        elif bet == 50:
            pygame.draw.rect(win, (0,255,0),(350, 735, 100, 10))
        elif bet == 100:
            pygame.draw.rect(win, (0,255,0),(500, 735, 100, 10))
        elif bet == 200:
            pygame.draw.rect(win, (0,255,0),(650, 732, 100, 10))
        
        #display user feedback for personalities
        #dealer
        if dealerLimit == 20:
            pygame.draw.rect(win, (0,255,0),(310, 195, 110, 10))
        elif dealerLimit == 18:
            pygame.draw.rect(win, (0,255,0),(470, 195, 100, 10))
        elif dealerLimit == 16:
            pygame.draw.rect(win, (0,255,0),(615, 195, 110, 10))
        #harmon
        if harmonButton == 1:
            pygame.draw.rect(win, (0,255,0),(310, 265, 110, 10))
        elif harmonButton == 2:
            pygame.draw.rect(win, (0,255,0),(470, 265, 100, 10))
        elif harmonButton == 3:
            pygame.draw.rect(win, (0,255,0),(615, 265, 110, 10))
        #maxwell
        if maxwellLimit == 20:
            pygame.draw.rect(win, (0,255,0),(310, 340, 110, 10))
        elif maxwellLimit == 18:
            pygame.draw.rect(win, (0,255,0),(470, 340, 100, 10))
        elif maxwellLimit == 16:
            pygame.draw.rect(win, (0,255,0),(615, 340, 110, 10))

        pygame.display.update()


#this function shows the cards
def showCards(handNum, cardY, center, show):
    cardAmount = len(hands[handNum].cards)
    hands[handNum].printHand()
    if cardAmount == 1:
        win.blit(cardTemplate, (400-cardTemplateX-center,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 400, cardY)
    if cardAmount == 2:
        win.blit(cardTemplate, (355-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (445-cardTemplateX-center,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 355-center, cardY)
        if show == True:
            textWrite(str(hands[handNum].hand[1]), 50, (0,0,0), 445-center, cardY)
        else:
            textWrite("?", 50, (0,0,0), 445-center, cardY)
    elif cardAmount == 3:
        win.blit(cardTemplate, (310-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (400-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (490-cardTemplateX-center,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 310-center, cardY)
        textWrite(str(hands[handNum].hand[1]), 50, (0,0,0), 400-center, cardY)
        textWrite(str(hands[handNum].hand[2]), 50, (0,0,0), 490-center, cardY)
    elif cardAmount == 4:
        win.blit(cardTemplate, (265-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (355-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (445-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (535-cardTemplateX-center,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 265-center, cardY)
        textWrite(str(hands[handNum].hand[1]), 50, (0,0,0), 355-center, cardY)
        textWrite(str(hands[handNum].hand[2]), 50, (0,0,0), 445-center, cardY)
        textWrite(str(hands[handNum].hand[2]), 50, (0,0,0), 535-center, cardY)
    elif cardAmount == 5:
        win.blit(cardTemplate, (260-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (330-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (400-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (470-cardTemplateX-center,cardY-cardTemplateY))
        win.blit(cardTemplate, (540-cardTemplateX-center,cardY-cardTemplateY))
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 260-center, cardY)
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 330-center, cardY)
        textWrite(str(hands[handNum].hand[1]), 50, (0,0,0), 400-center, cardY)
        textWrite(str(hands[handNum].hand[2]), 50, (0,0,0), 470-center, cardY)
        textWrite(str(hands[handNum].hand[0]), 50, (0,0,0), 540-center, cardY)

#opening screen
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

#starting arangements
resetDeck(4)
startHand()
makeBet()

#main game loop
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
            #checks if there are two cards
            if len(hands[0].cards) == 2:
                #checks if the cards equal each other
                if hands[0].cards[0].getCardValue() == hands[0].cards[1].getCardValue():
                    #checks if the player has enough money
                    if money > bet*2:
                        hands[0].checkSplit()

        #hit
        elif input(pygame.MOUSEBUTTONDOWN, event, 350, 450, 650, 700) == True:
            if hands[currentHand].getHandValue() < 21 and hands[currentHand].stand == False:
                hands[currentHand].addCard(deck[0])
                deck.pop(0)
                #checks if player has five cards
                if hands[currentHand].handFive() == True:
                    winGame()
        
        #stand
        elif input(pygame.MOUSEBUTTONDOWN, event, 475, 575, 650, 700) == True:
            hands[currentHand].checkStand()

        #forfeit
        elif input(pygame.MOUSEBUTTONDOWN, event, 650, 750, 650, 700) == True:
            hands[currentHand].checkForfeit()

    hands[currentHand].checkBust()
    hands[currentHand].checkWin()
    redrawWindow()
