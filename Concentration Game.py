import numpy as np
import random
import string

class Card():
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        self.value = "{} of {}".format(self.number, self.suit)

    def show(self):
        print("{} of {}".format(self.number, self.suit))

class Deck():
    def __init__(self): 
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        num = list(range(2,11))
        pictures = ["Jack", "Queen", "King"]
        values = ["Ace"]
        wholeDeck = [Card(0, "Joker").value]*4
        values += num + pictures
        #wholeDeck = []
        for s in list(range(4)):
            for i in list(range(13)):
                card = Card(str(values[i]), suits[s])
                wholeDeck.append(card.value)
        #wholeDeck += jokers
        self.deck = wholeDeck

    def deckGrid(self):
        rows = 7
        cols = 8
        return np.array(self.deck).reshape(rows, cols)

    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck

    def show(self):
        print(self.deck)
        
class Board():
    def __init__(self): #deck is object of the Deck Class 
        self.rows = 7
        self.cols = 8 
        
        rowHeader = list(string.ascii_lowercase)
        header1 = "     {:>2}".format(rowHeader[0])
        for col in range(1,self.cols):
            header1 += "{:>5}".format(rowHeader[col])
        self.header1 = header1
        rowHeader = list(range(1, self.rows+1))
        self.rowHeader = rowHeader
        self.line = ""
        self.lineList = []

    def progress(self, match = False, rowNum=1, colNum=1):
        # rowNum-=1
        # colNum-=1
        newLine = ""
        sep = "  "
        newlineList = []

        print(self.header1)
        print("\n")
        if match == True:
            self.lineList[rowNum][colNum] = "\'0\'"
            for row in range(self.rows):
                newLine = sep.join(self.lineList[row])

                print(" {:<4}".format(self.rowHeader[row]) + newLine)
                print("\n")

                eachRow = newLine.split("  ")
                newlineList.append(eachRow)
            self.lineList = newlineList
        else:
            for row in range(self.rows):
                newLine = sep.join(self.lineList[row])
                print(" {:<4}".format(self.rowHeader[row]) + newLine)
                print("\n")

                eachRow = newLine.split("  ")
                newlineList.append(eachRow)
            self.lineList = newlineList
            
    def show(self):
        line = ""
        entry = "\'?\'"
        lineList = []

        for col in range(self.cols):
            line += "{:5}".format(entry)

        print(self.header1)
        print("\n")

        for row in range(self.rows): #printing the grid
            print(" {:<4}".format(self.rowHeader[row]) + line)
            print("\n")

            eachRow = line.split("  ")
            lineList.append(eachRow)

        self.lineList = lineList

class Game():
    def __init__(self):
        self.selection1 = ''
        self.selection2 = ''
        self.numrow1 = 0
        self.numcol1 = 0
        self.numrow2 = 0
        self.numcol2 = 0
        self.match = False
        self.end = False

    def startScreen(self):
        print("Welcome to Concentration!")

    def gameComplete(self, board):
        for line in board.lineList:
            for i in range(board.cols):
                if line[i] == " 0 ":
                    self.end = True
                else:
                    self.end = False

    def makeSelection(self, deck_of_cards):
        a = list(string.ascii_lowercase)
        coordinate1 = input("Please enter a coordinate:") #of the form a1, b1 etc
        self.coordinate1 = coordinate1
        selection1 = list(coordinate1)
        row1 = int(selection1[1])  
        row1 -= 1
        col1 = int(a.index(selection1[0]))
        #selection1[1] = row1
        self.selection1 = deck_of_cards.deckGrid()[row1, col1]
        self.numcol1 = col1
        self.numrow1 = row1
        print("You have selected the > {} <".format(self.selection1))

        coordinate2 = input("Please enter a coordinate:") #of the form a1, b1 etc
        self.coordinate2 = coordinate2
        selection2 = list(coordinate2)
        row2 = int(selection2[1])
        row2 -= 1
        col2 = int(a.index(selection2[0]))
        #selection2[1] = row2
        self.selection2 = deck_of_cards.deckGrid()[row2, col2]
        self.numcol2 =col2
        self.numrow2 = row2
        print("You have selected the > {} <".format(self.selection2))
        print("\n")
        print("Your selections were: the {} and the {}.".format(self.selection1, self.selection2))

    def check(self):
        self.selection1.split(" of ")
        self.selection2.split(" of ")
        if self.selection1[0] == self.selection2[0]:
            print("Congrats! {} and {} are pairs!".format(self.coordinate1, self.coordinate2))
            print("\n")
            self.match = True
            return True
        else:
            print("Unfortunately, {} and {} are not pairs.".format(self.coordinate1, self.coordinate2))
            print("Try again")
            print("\n")
            self.match = False
            return False

    def run(self):
        self.startScreen()
        deck_of_cards = Deck()
        print("Initializing...")
        deck_of_cards.shuffle()
        inp = input("The cards has been shuffled once.\nWould you like to shuffle the cards again? (Y/N) \n>>>")
        if inp.lower() == "y":
            deck_of_cards.shuffle()
            print("Shuffling...\nShuffling complete! \nThe game is starting now!")
            print("\n")
            board = Board()
        else:
            print("Alright then, the game is starting now!")
            print("\n")
            board = Board()
        board.show()
        while self.end == False:
            self.makeSelection(deck_of_cards)
            self.check()
            if self.match == True:
                board.progress(self.match,self.numrow1,self.numcol1)
                board.progress(self.match,self.numrow2,self.numcol2)
            else:
                board.progress(self.match,self.numrow1,self.numcol1)

            self.gameComplete(board)
        if self.end == True:
            board.progress(self.match,self.numrow1,self.numcol1)
            print("Congratulations! You have won the game!")
            print("Exiting...")

    def test(self):
        self.startScreen
        deck_of_cards = Deck()
        print("Initializing...")
        inp = input("The cards has not been shuffled.\nWould you like to shuffle the cards? (Y/N) \n>>>")
        if inp.lower() == "y":
            deck_of_cards.shuffle()
            print("Shuffling...\nShuffling complete! \nThe game is starting now!")
            print("\n")
            board = Board()
        else:
            print("Alright then, the game is starting now!")
            print("\n")
            board = Board()
        board.show()
        while self.end == False:
            self.makeSelection(deck_of_cards)
            self.check()
            if self.match == True:
                board.progress(self.match,self.numrow1,self.numcol1)
                board.progress(self.match,self.numrow2,self.numcol2)
            else:
                board.progress(self.match,self.numrow1,self.numcol1)

            self.gameComplete(board)
        if self.end == True:
            board.progress(self.match,self.numrow1,self.numcol1)
            print("Congratulations! You have won the game!")
            print("Exiting...")

    def difficulty(self, setting): #1-3 levels of difficulty
        pass


game = Game()
#game.run()
game.test()

