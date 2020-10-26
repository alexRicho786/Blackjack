class Hand:
    "Base class for a hand of cards"

    def __init__(self):
        self.cards = []
        self.hand = []

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


    def printHand(self):
        self.hand.clear()
        for c in self.cards:
            self.hand.append(c.suit + c.face)
        return self.hand
