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
        #wholeDeck = [Card(0, "Joker").value]*4
        wholeDeck = []
        values += num + pictures
        #wholeDeck = []
        for s in list(range(4)):
            for i in list(range(13)):
                card = Card(str(values[i]), suits[s])
                wholeDeck.append(card.value)
        self.deck = wholeDeck

    def deckGrid(self):
        rows = 4
        cols = 13
        return np.array(self.deck).reshape(rows, cols)

    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck

    def show(self):
        print(self.deck)
        
class Board():
    def __init__(self): #deck is object of the Deck Class 
        self.rows = 4
        self.cols = 13 
        
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
            
    def show(self, end=False): #end = Boolean
        line = ""
        entry = "\'?\'"
        if end == True:
            entry = "\'0\'"
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

class Coordinate():
    def __init__(self, deck_of_cards, board):
        a = list(string.ascii_lowercase)
        coordinates = input("Please enter a coordinate (a1,c4 etc):\n>>>") #of the form a1, b1 etc
        selection = list(coordinates) # ['a', '1']  
        row = int(selection[1]) 
        row -= 1
        col = int(a.index(selection[0]))
        self.coordinates = coordinates # 'a1'
        self.row = row
        self.col = col        
        if self.row < 0 or self.row >= board.rows or self.col >= board.cols:
            self.allowed = False
            print("Invalid input, please ensure your row number is between 1 and {} and your column number from a to {}".format(board.rows,a[board.cols-1]))
        else:
            self.allowed = True
            self.name = deck_of_cards.deckGrid()[self.row, self.col] # e.g. 3 of Hearts

class Game():
    def __init__(self):
        self.numrow1 = 0
        self.numcol1 = 0
        self.numrow2 = 0
        self.numcol2 = 0
        self.match = False
        self.end = False
        self.memoryList = []
        self.skip = False
        self.coordinate1 = 0
        self.coordinate2 = 0

    def startScreen(self):
        print("Welcome to Concentration!")

    def endScreen(self, board):
        board.show(self.end)

    def gameComplete(self, board):
        for line in board.lineList:
            for i in range(board.cols):
                if line[i] == " 0 ":
                    self.end = True
                else:
                    self.end = False

    def Select(self, deck_of_cards, board): #this initializes 2 coordinates that you choose
        a = list(string.ascii_lowercase)
        self.coordinate1 = Coordinate(deck_of_cards, board) # ['a', '1'] 
        if self.coordinate1.allowed == False:
            return self.Select(deck_of_cards, board)
        self.selection1 = self.coordinate1.coordinates
        self.numcol1 = self.coordinate1.col
        self.numrow1 = self.coordinate1.row
        print("You have selected the > {} <".format(self.coordinate1.name))

        self.coordinate2 = Coordinate(deck_of_cards, board)
        if self.coordinate2.allowed == False:
            return self.Select(deck_of_cards, board)
        self.selection2 = self.coordinate2.coordinates
        self.numcol2 = self.coordinate2.col
        self.numrow2 = self.coordinate2.row
        print("You have selected the > {} <".format(self.coordinate2.name))
        print("\n")
        print("Your selections were: the {} and the {}.".format(self.coordinate1.name, self.coordinate2.name))

    def check(self):
        self.coordinate1.name.split(" of ") #['2','Spades']
        self.coordinate2.name.split(" of ")
        if self.coordinate1.name[0] == self.coordinate2.name[0]:
            self.match = True
            return True
        else:
            self.match = False
            return False

    def memory(self):
        if self.match == True:
            print("Congrats! {} and {} are pairs!".format(self.coordinate1.name, self.coordinate2.name))
            print("your previous selections were:")
            for line in self.memoryList:
                print(line)
            print("\n")
        else:
            previous = "{} at {}, {} at {}".format(self.coordinate1.name, self.coordinate1.coordinates, self.coordinate2.name, self.coordinate2.coordinates)
            self.memoryList.append(previous)
            print("Unfortunately, {} and {} are not pairs.\n".format(self.coordinate1.coordinates, self.coordinate2.coordinates))
            print("Try again, your previous selections were:")
            for line in self.memoryList:
                print(line)
            print("\n")

    def cheat(self, deck_of_cards):
        layout = deck_of_cards.deckGrid()


        self.skip = True

    def run(self):
        self.startScreen()
        deck_of_cards = Deck()
        print("Initializing...")
        #deck_of_cards.shuffle()
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
            self.Select(deck_of_cards, board)
            self.check()
            if self.match == True:
                board.progress(self.match,self.numrow1,self.numcol1)
                board.progress(self.match,self.numrow2,self.numcol2)
                self.memory()
            else:
                board.progress(self.match,self.numrow1,self.numcol1)
                self.memory()

            self.gameComplete(board)

        if self.end == True:
            board.progress(self.match,self.numrow1,self.numcol1)
            print("Congratulations! You have won the game!")
            print("Exiting...")

game = Game()
game.run()

# test = Deck()
# test.deckGrid()
# test.show()

