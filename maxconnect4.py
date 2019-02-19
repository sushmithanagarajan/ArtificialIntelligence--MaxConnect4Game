#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

# Student Name : Sushmitha Nagarajan
# Student ID : 1001556348
# This program explains the game states, scoreboard, inputs from command lines passes them to functions, prints output in cmd

# import the necessary packages
import sys
import os
from MaxConnect4Game import *
import time
from copy import copy
import random
import sys
import copy

infinity = float('inf')
child_node_present = True
utility_list = {}
score_list = []
game_state = 0
depth_limited_search = 0
depth = 0
score_list_from_alpha_beta = []
depth_line = 0
a1 = 0
b1 = 0


def interactiveGamePlay(currentGame,next_chance,depth,inFile):
    # calculate the time here
    start_time = time.time()
    if next_chance == "human-next":
# check if the piece is full or not
        while currentGame.checkPieceCountForInteractiveGame() != 42:
            print "Its humans turn now"
            userMove = input("Enter the column number [1-7] where you would like to play in this game: ")
            # usermoves are calculated with this limit
            if not 0 < userMove < 8:
                print "Invalid column number!"
                continue
                # if it is not the current game reduce the usermove -1 and keep playing
            if not currentGame.playPiece(userMove - 1):
                print "This column is full now cant fit more!"
                continue
# get the input file here
            if os.path.exists("input.txt"):
                currentGame.gameFile = open(inFile, 'r')
            try:
                # open the human txt if not
                currentGame.gameFile = open("human.txt", 'w')
                print "You have made a move at column this - "+str(userMove)
                # print the gameboard to file
                # close the gamefile
                # close the gameboard after getting information
                currentGame.printGameBoardToFile()
                currentGame.printGameBoard()
                currentGame.gameFile.close()
                # check if the board is equal to 42
                if(currentGame.checkPieceCountForInteractiveGame() == 42):
                    print "Game Over all moves done"
                    break
                    # computer game board moves
                else:
                    # checks the turn for current game and decides who is playing
                    print "Computer will think "+str(depth)+" steps ahead and make a move"
                    if currentGame.currentTurn == 1:
                        currentGame.currentTurn = 2
                    elif currentGame.currentTurn == 2:
                        currentGame.currentTurn = 1
                        # trigger the play with that depth in ai play method in the adjacent game
                    currentGame.aiPlay(int(depth))
                    #goes to the gamefile here and opens them
                    currentGame.gameFile = open("computer.txt", 'w')
                    # when the human is playing here
                    print "Computer has made a move at column " + str(currentGame.computer_column+1)
                    currentGame.printGameBoardToFile()
                    currentGame.printGameBoard()
                    # game board is true or false here and count the score
                    currentGame.countScore()
                    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
                    currentGame.gameFile.close()
            except Exception,e:
                print e
        # next chance if computer plays here the interactive game
    elif next_chance == "computer-next":
        currentGame.aiPlay(int(depth))
        #goes to the aiplay to calculate the depth
        currentGame.gameFile = open("computer.txt", 'w')
        print "Computer has made  move at column " + str(currentGame.computer_column+1)
        currentGame.printGameBoardToFile()
        currentGame.gameFile.close()
        currentGame.printGameBoard()
        # current game being called on gameboard game score
        currentGame.countScore()
        print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
        # interactive play mode
        interactiveGamePlay(currentGame,"human-next",depth,inFile)
#goes to the piece count check for interactive game
    if currentGame.checkPieceCountForInteractiveGame() == 42:    # Board is full or not>
        print 'BOARD FULL\n\nGame Over!\n'
    print 'Game state after each move is:'
    currentGame.printGameBoard()
    currentGame.countScore()
    #count score for the currentgame
    # game to score calculation in the current score
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    # compare players score if 1 on 2
    if currentGame.player1Score > currentGame.player2Score:
        print "Player 1 WINS"
    # compare if player 2 wins or not
    elif currentGame.player2Score > currentGame.player1Score:
        print "Player 2 WINS"
        # check if it is a tie or not
        # current game player score here
    elif currentGame.player1Score == currentGame.player2Score:
        print "Its a TIE no wins here"
        # calculate the stop time
    stop_time = time.time()
    execution_time = stop_time - start_time
    # find the difference in time and display them
    print "Exceution time"
    print execution_time

# define onemove game
def oneMoveGame(currentGame, depth):
    start_time = time.time()
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)
    currentGame.aiPlay(depth)  # Make a move (only random is implemented)
    print 'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()
    print "Time take for the computers decision is"
    stop_time = time.time()
    total_time = stop_time - start_time
    print "execution time"
    print total_time
    # print the total time take for execution from start of the function to end of it

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]
    next_chance = argv[3]
    depth = argv[4]
    depth = int(depth)

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game()  # Create a game object

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
        # open a game input file in read mode
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")
        # this creates the exception if file is not readable or reachable

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        if currentGame.currentTurn == 1:

            print "Player Number of player : "+str(1)
            print "COMPUTER is playing as : "+str(2)
        elif currentGame.currentTurn == 2:
            print "Player Number of player is : "+str(2)
            print "COMPUTER is playing as  : "+str(1)
        interactiveGamePlay(currentGame,next_chance,depth,inFile)  # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame, depth)  # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)