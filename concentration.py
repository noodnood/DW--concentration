import numpy as np
import random
import string

class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = "{} of {}".format(self.rank, self.suit)

    def show(self):
        print("{} of {}".format(self.rank, self.suit))

class Deck():
    def __init__(self): 
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        num = list(range(2,11))
        pictures = ["Jack", "Queen", "King"]
        ranks = ["Ace"]
        #wholeDeck = [Card(0, "Joker").value]*4
        wholeDeck = []
        ranks += num + pictures
        #wholeDeck = []
        for s in list(range(4)):
            for i in list(range(13)):
                card = Card(str(ranks[i]), suits[s])
                wholeDeck.append(card.value)
        self.deck = wholeDeck

    def deckGrid(self):
        rows = 4
        cols = 13
        return np.array(self.deck).reshape(rows, cols)

    def shuffle(self):
        random.shuffle(self.deck)
        print("Shuffling...\nShuffling complete! \nThe game is starting now!")
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

    def progress(self):
        newLine = ""
        sep = "  "
        newlineList = []

        print(self.header1)
        print("\n")

        for row in range(self.rows):
            newLine = sep.join(self.lineList[row])
            
            print(" {:<4}".format(self.rowHeader[row]) + newLine)
            print("\n")

            eachRow = newLine.split("  ")
            newlineList.append(eachRow)

        self.lineList = newlineList

    def build(self, match, rowNum=1, colNum=1):
        newLine = ""
        sep = "  "
        newlineList = []
        if match == True:
            self.lineList[rowNum][colNum] = "\'{}\'".format(chr(9608))
        for row in range(self.rows):
            newLine = sep.join(self.lineList[row])
            eachRow = newLine.split("  ")
            newlineList.append(eachRow)
        self.lineList = newlineList

    def create(self, end=False): #end = Boolean
        line = ""
        entry = "\'?\'"
        if end == True:
            entry = "\'{}\'".format(chr(9608))
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
        coordinates = input("Please enter a coordinate (c4 etc):\n>>>") #of the form a1, b1 etc
        selection = list(coordinates) # ['a', '1']
        invalid = "Invalid input, please ensure your row number is a number between 1 and {} and your column is an alphabet from a to {}".format(board.rows,a[board.cols-1])
        self.bypass = False

        if coordinates == "end":
            self.bypass = True
        else:
            if len(coordinates) !=2 or coordinates == "" or selection[0] not in a or selection[1] == "" or selection[1].isdigit() == False:
                self.allowed = False
                print(invalid)

            else:
                row = int(selection[1]) 
                row -= 1
                col = int(a.index(selection[0]))
                self.coordinates = coordinates # 'a1'
                self.row = row
                self.col = col        
                if self.row < 0 or self.row >= board.rows or self.col >= board.cols:
                    self.allowed = False
                    print(invalid)
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
        self.cardMap = {}
        self.rankDict= {}
        self.cheats = "Not activated"

    def startScreen(self):
        print("Welcome to Concentration!")
        print("Initializing...")

    def isComplete(self, board):
        for line in board.lineList:
            for i in range(board.cols):
                if line[i] == " {} ".format(chr(9608)):
                    self.end = True
                else:
                    self.end = False
        if self.end == True:
            print("Congratulations! You have won the game!")
            print("Exiting...")

    def select(self, deck_of_cards, board): #this initializes 2 coordinates that you choose
        self.coordinate1 = Coordinate(deck_of_cards, board) # ['a', '1'] 
        if self.coordinate1.bypass == True:
            self.cheat(deck_of_cards)
            return
        else:
            if self.coordinate1.allowed == False:
                return self.select(deck_of_cards, board)
            self.numcol1 = self.coordinate1.col
            self.numrow1 = self.coordinate1.row
            print("You have selected the > {} <".format(self.coordinate1.name))

        self.coordinate2 = Coordinate(deck_of_cards, board)
        if self.coordinate2.bypass == True:
            self.cheat(deck_of_cards)
            return
        else:
            if self.coordinate2.allowed == False:
                return self.select(deck_of_cards, board)
            self.numcol2 = self.coordinate2.col
            self.numrow2 = self.coordinate2.row
            print("You have selected the > {} <".format(self.coordinate2.name))
            
            print("\n")
            print("Your selections were: the {} at > {} < and the {} at > {} <.\n".format(self.coordinate1.name, self.coordinate1.coordinates, self.coordinate2.name, self.coordinate2.coordinates))

    def check(self):
        if self.cheats =="Activated":
            return
        else:
            if self.coordinate1.name == self.coordinate2.name:
                print("Please choose 2 different coordinates!")
                self.match = False
            else:
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
            print("Your previous selections were:")
            for line in self.memoryList:
                print(line)
            print("\n")
        else:
            previous = "{:>15} at {} | {:<} at {}".format(self.coordinate1.name, self.coordinate1.coordinates, self.coordinate2.name, self.coordinate2.coordinates)
            self.memoryList.append(previous)
            print("Unfortunately, {} and {} are not pairs.\n".format(self.coordinate1.coordinates, self.coordinate2.coordinates))
            print("Try again, your previous selections were:")
            for line in self.memoryList:
                print(line)
            print("\n")

    def cheat(self, deck_of_cards):
        arr = deck_of_cards.deckGrid()
        rankDict = {}
        cardMap = {}
        for card in deck_of_cards.deck:     
            result = np.where(arr == card)
            location = list(zip(result[0], result[1]))
            cardMap[card] = location[0]
            rank = card.split(" of ")
            if rank[0] not in rankDict:
                rankDict[rank[0]] = [cardMap[card]]
            else:
                rankDict[rank[0]] += [cardMap[card]]
        self.cardMap = cardMap # card : (a,b)
        self.rankDict = rankDict # rank : [(a,b),(c,d)...]
        self.cheats = "Activated"

    def get_key(self, val): 
        for card, location in self.cardMap.items(): 
            if val == location: 
                return card 

    def selfsolver(self, board):
        for rank in self.rankDict.keys(): ##cheats activated
            self.match = True
            coor = self.rankDict[rank]
            i = 0
            j = 1
            a = list(string.ascii_lowercase)
            
            while i < 3: 
                coordinate1 = a[coor[i][1]] 
                coordinate1 += str(int(coor[i][0] + 1))    
                coordinate2 = a[coor[j][1]] 
                coordinate2 += str(int(coor[j][0] + 1))      
                board.build(self.match,coor[i][0],coor[i][1])
                board.build(self.match,coor[j][0],coor[j][1])
                
                print("Your selections were: the {} at > {} < and the {} at > {} <.\n".format(self.get_key(coor[i]), coordinate1, self.get_key(coor[j]), coordinate2))
                board.progress()
                i += 2
                j += 2

    def run(self):
        self.startScreen()
        deck_of_cards = Deck()
        inp = input("The cards has not been shuffled.\nWould you like to shuffle the cards? (Y/N) \n>>>")
        if inp.lower() == "y":
            deck_of_cards.shuffle()
            print("\n")
        else:
            print("Alright then, the game is starting now!")
            print("\n")
        board = Board()
        board.create()

        while self.end == False:
            self.select(deck_of_cards, board)
            if self.cheats == "Activated":
                break

            self.check()
            if self.match == True:
                board.build(self.match,self.numrow1,self.numcol1)
                board.build(self.match,self.numrow2,self.numcol2)
                board.progress()
                self.memory()
            else:
                board.progress()
                self.memory()

            self.isComplete(board)

        if self.cheats == "Activated":
            self.selfsolver(board)
            self.end == True        
        
        print("Congratulations! You have won the game!")
        print("Exiting...")

game = Game()
game.run()
