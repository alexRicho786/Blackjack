class Hand:
    "Base class for a hand of cards"

    def __init__(self):
        self.cards = []
        self.hand = []
        self.bust = False
        self.win = False
        self.stand = False
        self.forfeit = False
        self.double = False
        self.split = False
        self.hasSplit = False


    def addCard(self, c):
        self.cards.append(c)


    def removeCards(self):
        self.cards.clear()


    def getHandValue(self):
        hand_value = 0
        has_ace = False

        for c in self.cards:
            hand_value += c.value
            if c.is_ace == True:
                has_ace = True

        if hand_value > 21 and has_ace == True:
            for cd in self.cards:
                if hand_value > 21:
                    if cd.is_ace == True:
                        hand_value -= 10

        return hand_value
    
    #if players hand gets to 5
    def handFive(self):
        if len(self.cards) == 5:
            return True


    def printHand(self):
        self.hand.clear()
        for c in self.cards:
            self.hand.append(c.suit + c.face)
        return self.hand

    def checkBust(self):
        if self.getHandValue() > 21:
            self.bust = True


    def checkWin(self):
       if self.getHandValue() == 21:
           self.stand = True
    

    def clearCards(self):
        self.cards.clear()
        self.hand.clear()


    def checkStand(self):
        self.stand = True


    def checkForfeit(self):
        self.forfeit = True
    

    def checkDouble(self):
        self.double = True


    def checkSplit(self):
        self.split = True


    #when player stands this determines
    #how the other players play
    def multipleHits(self, limit):
        if self.getHandValue() < limit:
            return True
        else:
            return False
        
