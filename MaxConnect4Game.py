# Student Name : Sushmitha Nagarajan
# Student ID : 1001556348
# import all the necessary packages
from copy import copy
import random
import sys
import copy
#import numpy as np
from datetime import time
import time
import os
import sys
import parser
import json

#global variables being declared here
#they could be changed locally to get game info
infinity = float('inf')
child_node_present = True
utility_list = {}
score_list = []
score_board = []
game_state = 0
depth_limited_search = 0
depth = 0
score_list_from_alpha_beta = []
depth_line = 0
end_of_file = 0
consecutiveCount = 0

#Class maxconnect4game of connecting 4 strikes and see who wons
# this class contains the actual logic on how the game victory is decided on both the modes
class maxConnect4Game:
    def __init__(self):
        # initialise all these values on the start of the game to be used inside the game
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.score = 0
        self.iwon = 0
        self.computerwon = 0
        self.humanwon = 0
        self.currentgamestate = 0
        self.gamestatenow = []
        self.computer_column = None
        random.seed()
#this method checks for every single piece in the board the streak and state of each piece and helps to place it
    def checkthisplease(self, state, color, streak):
        consecutive_count1 =0
        count = 0
        # for every thing in the board
        for i in range(6):
            # 6 rows is the limit for piece check
            for j in range(7):
                # out of range of 7 columns and 6 rows
                if state[i][j] == color:
                    # check it  starts at (i, j) in a vertical aspect
                    count += self.verticalcheckhere(i, j, state, streak)
                    # perform check on horizontal check here
                    count += self.horizontalcheckhere(i, j, state, streak)
                    # perform check ona diagonal level to find matches on the piece placed
                    count += self.diagonalcheckhere(i, j, state, streak)
        # return the total sum here
        return count

    # Count the pieces of game being played until now and decide the function
    def eval_function(self,state):
        """ Simple heuristic to evaluate board configurations
            We keep the max limit as 9999
            We also keep a min limit of -9999 to calculate againsta  standard
            Heuristic to evaluvate board configurations according to the game state
            Utility calculation to check against the two three consecutive pieces towards a four pace by the player and the opponenet
        """
        b1_color = 0
        a1_color = 0
        a1 = 0
        stateofgame = 0
        a1 = state
        if self.currentTurn == 1:
            o_color = 2
        elif self.currentTurn == 2:
            o_color = 1
        a1 = state
        fours = self.checkthisplease(state,self.currentTurn, 4)
        #check if 4 are together
        threes = self.checkthisplease(state, self.currentTurn, 3)
       #checks if three are together
        twos = self.checkthisplease(state,self.currentTurn, 2)
        #checks if two are together
        d1_color = 0
        oponent_fours = self.checkthisplease(state, o_color, 4)
        e1_color =0
        #check about opponent three together pieces
        oponent_threes = self.checkthisplease(state, o_color, 3)
        c1_color = 0
        #check about opponents two together pieces
        oponent_twos = self.checkthisplease(state, o_color, 2)
        return (fours * 10 + threes * 5 + twos * 2)- (oponent_fours *10 + oponent_threes * 5 + oponent_twos * 2)
        # It compares the heuristics at every level and calculates the utility value for the program

#vertically check if anything is getting along for a 4 staright connection
    def verticalcheckhere(self, row, col, state, streak):
        count = 0
        verticality = 0
        consecutiveCount = 0
        z1 = 0
        z1 = 76
        for i in range(row, 6):
            if state[i][col] == state[row][col]:
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    # horizontally check if anything is getting along for a 4 staright connection
    def horizontalcheckhere(self, row, col, state, streak):
        count = 0
        consecutiveCount = 0
        currstate = 0
        for j in range(col, 7):
            if state[row][j] == state[row][col]:
                consecutiveCount += 1
            else:
                break
        l1 = 0
        l1 = state
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

#check the piece count for every game in the game boarde in a n interactive game
    def checkPieceCountForInteractiveGame(self):
        return sum(1 for row in self.gameBoard for piece in row if piece)

# diagonally check if the pieces go along for a max connect 4 pieces together
    def diagonalcheckhere(self, row, col, state, streak):
        count = 0
        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        #if(count ==0):
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented otherwise its not a match
        if consecutiveCount >= streak:
            total += 1
        # check for diagonals with negative slope and gradient calculation where streak < consecutive count
        consecutiveCount = 0
        j = col
        #check within the range of values here now
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented based on the range to make it available for the next game
        if consecutiveCount >= streak:
            total += 1
        return total


#this method checks the game state position in a max connect 4 game
    def checkforgamestateposition(self):
        self.currentgamestate = issubclass(1 for row in self.gameBoardes for piece in row if piece)


# check piece count in the game board for bothe the game modes
    def checkPieceCount(self):
        #sums every item in the game board for a piece and row and calculate the total piece count
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print 'Game Board   '
        print ' ---****------'
        for i in range(6):
            print ' |'
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        # print the game state for visual representation in console
        print ' ----****------'

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            # prints the game joins the string in row and col
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))
        # write the game file here with help of current turn

# find who wins the game with this extra method whcich only prints the value of winner and who it is
    def identifywhowongame(self):
        for row in self.gameBoard:
            self.write(''.map(str(col) for col in row) + '\r\n')
        self.write('%s\r\n' % str(self.currentTurnofgameinthis))

    # find who wins the game with this extra method whcich only prints the value of winner and who it is
    def identifywholosegame(self):
        for row in self.gameBoard:
            self.write(''.map(str(col) for col in row) + '\r\n')
        self.write('%s\r\n' % str(self.currentTurnofgame))


    # Place value of piece in a column here
    def playPiece(self, column):
        #print column
        if not self.gameBoard[0][column]:
            # the game board range goes here
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    #this gameboard helps to plavce the piece in a column here
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1

#check how the piece works here are as follows
    def checkPiece(self, column,opponent):
        # print column
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                #range of game board in a for loop to calculate against those columns
                if not self.gameBoard[i][column]:
                    # game board to decide here
                    self.gameBoard[i][column] = opponent
                    self.pieceCount += 1
                    return 1

    # The minimax algorithm.
    def minimax(self,current_node):
        current_state = copy.deepcopy(current_node)
        for i in range(0,6,1):
            # do deep copy of the current state and then perform changes
            if self.playPiece(i) != None:
                if self.pieceCount == 42:
                    self.gameBoard = copy.deepcopy(current_state)
                    return i
                #this calculates the min max whose utility and who has to play next here
                # this is totally based on these values of utility or they get updated accordingly
                else:
                    utility_list[i] = (self.min_value(self.gameBoard))
                    self.gameBoard = copy.deepcopy(current_state)

       #max util value for a list of utility values it can pick from
        max_util_value =  max([i for i in utility_list.values()])
        for i in range(0,6,1):
            # could be in this range
            if i in utility_list:
        	    if utility_list[i] == max_util_value:
        	    	utility_list.clear()
        	    	return i



# this method calculates the min value of current node
    def min_value(self,current_node):
        parent_node = copy.deepcopy(current_node)
        if self.currentTurn == 1:
            opponent = 2
        elif self.currentTurn == 2:
            opponent =1
        v = infinity
        track_of_child_nodes = []
        for j in range(0,6,1):
            current_state = self.checkPiece(j,opponent)
            if current_state != None:
                # check the piece value of a game here
                track_of_child_nodes.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(parent_node)
# make the changes
        if track_of_child_nodes == []:
            self.countScore1(self.gameBoard)
            return self.player1Score - self.player2Score
        else:
            for child in track_of_child_nodes:
                self.gameBoard = copy.deepcopy(child)
                v = min(v,self.max_value(child))
            return v
# method of max value
    def max_value(self,current_node):
        parent_node = copy.deepcopy(current_node)
        v = -infinity
        track_of_child_nodes = []
        for j in range(0,6,1):
            current_state = self.playPiece(j)
            if current_state != None:
                track_of_child_nodes.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(parent_node)
        if track_of_child_nodes == []:
            self.countScore1(self.gameBoard)
            return self.player1Score - self.player2Score
        else:
            max_score_list = []
            for child in track_of_child_nodes:

                self.gameBoard = copy.deepcopy(child)
                v = max(v, self.min_value(child))

            return v



    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0;
        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1

    def countScore1(self,state):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in state:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1
        # Check diagonally
        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1


    #normal minimax with change in methods :tentative
    def alpha_beta_decision(self, current_node):
        current_state = copy.deepcopy(current_node)
        for i in range(0, 6, 1):
            if self.playPiece(i) != None:
                # print self.gameBoard
                if self.pieceCount == 42:
                    self.gameBoard = copy.deepcopy(current_state)
                    return i
                else:
                    v = self.minValue(self.gameBoard,-infinity,infinity)
                    utility_list[i] = v
                    self.gameBoard = copy.deepcopy(current_state)
        #return max(utility_list, key=utility_list.get)
        max_util_value =  max([i for i in utility_list.values()])
        #print utility_list
        for i in range(0,6,1):
            if i in utility_list:
        	    if utility_list[i] == max_util_value:
        	    	utility_list.clear()
        	    	return i


#determines the max value of a function based on the alpha beta values
    def maxValue(self, current_node,alpha,beta):
        parent_node = copy.deepcopy(current_node)
        v = -infinity
        #keeps track of child
        track_of_child_nodes = []
        for j in range(0, 6, 1):
            current_state = self.playPiece(j)
            if current_state != None:
                # print the game board in the child nodes
                track_of_child_nodes.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(parent_node)
# if the child nodes are zero difference of two scores would be similar
        if track_of_child_nodes == []:
            self.countScore1(self.gameBoard)
            return self.player1Score - self.player2Score
        else:
            max_score_list = []
            for child in track_of_child_nodes:
                self.gameBoard = copy.deepcopy(child)
                v = max(v, self.minValue(child,alpha,beta))
                if v >= beta:
                    return v
                alpha = max(alpha,v)
            return v
# min value of node is computed here
    def minValue(self, current_node,alpha,beta):
        parent_node = copy.deepcopy(current_node)
        if self.currentTurn == 1:
            opponent = 2
        elif self.currentTurn == 2:
            opponent = 1

        v = infinity
        track_of_child_nodes = []
        for j in range(0, 6, 1):
            current_state = self.checkPiece(j, opponent)
            if current_state != None:
                track_of_child_nodes.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(parent_node)

        if track_of_child_nodes == []:

            self.countScore1(self.gameBoard)
            return self.player1Score - self.player2Score
        else:
            for child in track_of_child_nodes:

                self.gameBoard = copy.deepcopy(child)
                v = min(v, self.maxValue(child,alpha,beta))
                if v <= alpha:
                    return v
                beta = min(beta,v)

            return v

    def aiPlay(self, depth):
        randColumn = self.depth_limited_alpha_beta_pruning(self.gameBoard, depth)
        self.computer_column = randColumn
        result = self.playPiece(randColumn)
        if not result:
            print "No Result"
        else:
            if self.currentTurn == 1:
                self.currentTurn = 2
            elif self.currentTurn == 2:
                self.currentTurn = 1



    def depth_limited_minValue(self, current_node, alpha, beta,maxDepth):
        small_node = 0
        small_node = current_node
        maxval = 9999
        minval = -9999
		# makes a deep copy to check against them
        parent_node = copy.deepcopy(current_node)
        if self.currentTurn == 1:
            opponent = 2
        elif self.currentTurn == 2:
            opponent = 1

        v = infinity
        track_of_child_nodes = []
        for j in range(0, 7, 1):
            current_state = self.checkPiece(j, opponent)
            if current_state != None:
                track_of_child_nodes.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(parent_node)

        if track_of_child_nodes == [] or maxDepth == 0:
            # print "this is the final score for minimum"
            self.countScore1(self.gameBoard)
            return self.eval_function(self.gameBoard)
        else:
            for child in track_of_child_nodes:
                self.gameBoard = copy.deepcopy(child)
                v = min(v, self.depth_limited_maxValue(child, alpha, beta,maxDepth-1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

    def depth_limited_maxValue(self, current_node, alpha, beta, maxDepth):
        parent_node = copy.deepcopy(current_node)
        small_node = 0
        small_node = parent_node
        maxval = 9999
        minval = -9999
        v = -infinity
        track_of_child_nodes = []
        trak_of_nodes = []
        for j in range(0, 7, 1):
            current_state = self.playPiece(j)
            if current_state != None:
                #If current state of child nodes is less than no value do this
                track_of_child_nodes.append(self.gameBoard)
                #evaluvate the game board here
                self.gameBoard = copy.deepcopy(parent_node)
        if track_of_child_nodes == [] or maxDepth == 0:
            #if the child node is empty and depth if not zero check here
            self.countScore1(self.gameBoard)
            return self.eval_function(self.gameBoard)
        else:
            # for every element of child calculate and check against beta values
            for child in track_of_child_nodes:
                # deep copy the game board before changing the values
                self.gameBoard = copy.deepcopy(child)
                # max of these factors should be calculated
                v = max(v, self.depth_limited_minValue(child, alpha, beta,maxDepth-1))
                #check against a beta score
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            #return the value of this function depth limited max value
            return v

        def depthlimitedwithallchharacteristics(currentnode, child_node, parent_node):
            small_node = 0
            small_node = current_node
            maxval = 9999
            minval = -9999
            parent_node = copy.deepcopy(current_node)
            if self.currentTurn == 1:
                opponent = 2
            elif self.currentTurn == 2:
                opponent = 1

            v = infinity
            track_of_child_nodes = []
            for j in range(0, 7, 1):
                current_state = self.checkPiece(j, opponent)
                if current_state != None:
                    track_of_child_nodes.append(self.gameBoard)
                    self.gameBoard = copy.deepcopy(parent_node)

                # return the value of this function depth limited max value
                return v

            # Depth limited Search
            def depth_limited_alpha_beta_pruning(self, current_node, maxDepth):
                current_state = copy.deepcopy(current_node)
                for i in range(0, 7, 1):
                    if self.playPiece(i) != None:
                        # print self.gameBoard
                        if self.pieceCount == 42 or maxDepth == 0:
                            self.gameBoard = copy.deepcopy(current_state)
                            return i

                        else:

                            v = self.depth_limited_minValue(self.gameBoard, -infinity, infinity, maxDepth - 1)
                            utility_list[i] = v
                            self.gameBoard = copy.deepcopy(current_state)
                max_util_value = max([i for i in utility_list.values()])
                for i in range(0, 7, 1):
                    if i in utility_list:
                        if utility_list[i] == max_util_value:
                            utility_list.clear()
                            return i

    def whoisthewinnerforgame(self):
        minvalues = -9999
        maxvalues = 9999
        column = 0
		# self tuen of the current game decides who is the current tuen
        if self.currentTurn == 1:
            opponent_bad = 2
        elif self.currentTurn == 2:
            opponent_win = 1
			# check the range of game in the column
            for i in range(0, 7, 1):
                if self.playPiece(i) != None:
                    # print self.gameBoard
                    if self.pieceCount == 42 or self.currentTurn == 0:
                        opponent_bad = 1
                        if not self.gameBoard[i][column]:
                            self.gameBoard[i][column] = opponent_bad
                            self.pieceCount += 1
