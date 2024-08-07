import random
import time

class GoFish:
    
    def __init__(self):
        self.deck = []
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.suits = ["Clubs", "Spades", "Hearts", "Diamonds"]
        for rank in self.ranks:
            for suit in self.suits:
                self.deck.append((rank, suit))
        self.playerHand = []
        self.computerHand = []
        self.playerPoints = 0
        self.computerPoints = 0
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self, player, quiet = True):
        if player == "player":
            dealtCard = self.deck.pop()
            self.playerHand.append(dealtCard)
            if not quiet:
                print("You drew {0} of {1}!".format(dealtCard[0], dealtCard[1]))
        else:
            self.computerHand.append(self.deck.pop())
            
    def deckEmpty(self):
        if len(self.deck) == 0:
            return True
        else:
            return False
        
    def inHand(self, player, rank):
        if player == "player":
            hasCard = False
            for card in self.playerHand:
                if card[0] == rank:
                    hasCard = True
        else:
            hasCard = False
            for card in self.computerHand:
                if card[0] == rank:
                    hasCard = True
        return hasCard
    
    def fourOfAKind(self, player, rank):
        if not self.inHand(player, rank):
            return False
        else:
            if player == "player":
                cardCount = 0
                for card in self.playerHand:
                    if card[0] == rank:
                        cardCount += 1
            else:
                cardCount = 0
                for card in self.computerHand:
                    if card[0] == rank:
                        cardCount += 1
            if cardCount == 4:
                return True
            else:
                return False
    
    def showHand(self, player):
        if player == "player":
            hand = self.playerHand
        else:
            hand = self.computerHand
        for rank in self.ranks:
            currentRank = []
            for card in hand:
                if card[0] == rank:
                    currentRank.append(card[1])
            if len(currentRank) > 0:
                print("{0}: {1}".format(rank, str(currentRank)))
    
    def game(self):
        self.shuffle()
        for dealt in range(5):
            self.deal("player")
            self.deal("computer")
        turn = "player"
        lastGuess = ""
        while len(self.computerHand) > 0 and len(self.playerHand) > 0:
            if turn == "player":
                self.showHand("player")
                print("\nPlayer points: {0}\nComputer points: {1}".format(self.playerPoints, self.computerPoints))
                fishedCard = str(input("Choose a card to fish for: "))
                while not self.inHand("player", fishedCard) or not fishedCard in self.ranks:
                    if not fishedCard in self.ranks:
                        print("Choose a legal rank.")
                    elif not self.inHand("player", fishedCard):
                        print("Choose a rank that is in your hand")
                    fishedCard = str(input("Choose a card to fish for: "))
                time.sleep(1)
                if not self.inHand("computer", fishedCard):
                    print("\nGo Fish!\n")
                    self.deal("player", False)
                    if self.fourOfAKind("player", fishedCard):
                        movedCards = []
                        for card in range(len(self.playerHand) - 1, -1, -1):
                            if self.playerHand[card][0] == fishedCard:
                                movedCards.append(card)
                        for card in movedCards:
                            self.playerHand.pop(card)
                        self.playerPoints += 1
                    else:
                        turn = "computer"
                else:
                    movedCards = []
                    for card in range(len(self.computerHand) - 1, -1, -1):
                        if self.computerHand[card][0] == fishedCard:
                            movedCards.append(card)
                    for card in movedCards:
                        self.playerHand.append(self.computerHand.pop(card))
                    print("\n{0} {1}s!\n".format(len(movedCards), fishedCard))
                    if self.fourOfAKind("player", fishedCard):
                        movedCards = []
                        for card in range(len(self.playerHand) - 1, -1, -1):
                            if self.playerHand[card][0] == fishedCard:
                                movedCards.append(card)
                        for card in movedCards:
                            self.playerHand.pop(card)
                        self.playerPoints += 1
            else:
                possibleCards = []
                for card in self.computerHand:
                    if self.inHand("player", card[0]):
                       for cheat in range(3):
                           possibleCards.append(card[0])
                    elif card[0] != lastGuess:
                        possibleCards.append(card[0])
                if len(possibleCards) == 0:
                    tryGuess = random.choice(self.computerHand)[0]
                    attempt = 0
                    while tryGuess == lastGuess and attempt < 10:
                        tryGuess = random.choice(self.computerHand)[0]
                        attempt += 1
                    lastGuess = tryGuess
                else:
                    lastGuess = random.choice(possibleCards)
                print("Got any {0}s?".format(lastGuess))
                time.sleep(2)
                if self.inHand("player", lastGuess):
                    movedCards = []
                    for card in range(len(self.playerHand) - 1, -1, -1):
                        if self.playerHand[card][0] == lastGuess:
                            movedCards.append(card)
                    for card in movedCards:
                        self.computerHand.append(self.playerHand.pop(card))
                    print("\n{0} {1}s!\n".format(len(movedCards), lastGuess))
                    if self.fourOfAKind("computer", lastGuess):
                        movedCards = []
                        for card in range(len(self.computerHand) - 1, -1, -1):
                            if self.computerHand[card][0] == lastGuess:
                                movedCards.append(card)
                        for card in movedCards:
                            self.computerHand.pop(card)
                        self.computerPoints += 1
                else:
                    print("\nGo Fish!\n")
                    self.deal("computer")
                    if self.fourOfAKind("computer", lastGuess):
                        movedCards = []
                        for card in range(len(self.computerHand) - 1, -1, -1):
                            if self.computerHand[card][0] == lastGuess:
                                movedCards.append(card)
                        for card in movedCards:
                            self.computerHand.pop(card)
                        self.computerPoints += 1
                    else:
                        turn = "player"
            for rank in self.ranks:
                if self.fourOfAKind("player", rank):
                    movedCards = []
                    for card in range(len(self.playerHand) - 1, -1, -1):
                        if self.playerHand[card][0] == rank:
                            movedCards.append(card)
                    for card in movedCards:
                        self.playerHand.pop(card)
                    self.playerPoints += 1
                elif self.fourOfAKind("computer", rank):
                    movedCards = []
                    for card in range(len(self.computerHand) - 1, -1, -1):
                        if self.computerHand[card][0] == rank:
                            movedCards.append(card)
                    for card in movedCards:
                        self.computerHand.pop(card)
                    self.computerPoints += 1
                    
        print("\nPlayer points: {0}\nComputer points: {1}".format(self.playerPoints, self.computerPoints))
        if self.playerPoints > self.computerPoints:
            print("You win!")
        elif self.playerPoints < self.computerPoints:
            print("You lose...")
        else:
            print("Tie")
    
        
newDeck = GoFish()
newDeck.shuffle()
newDeck.game()