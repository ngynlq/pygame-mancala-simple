'''
Lap Nguyen
CS 386
Due Date 11/12/15
Description:This program manages the rules of the mancala
'''
import pygame
from pygame.locals import *
from sys import exit
import random
import mancala
#this function closes the program
def terminate():
    pygame.quit()
    exit()
#main function
def main():
    pygame.init()
    game = mancala.Game()
    game.Menu() #menu and tutorial control
    Mode = "Menu"
    onGoingMenu = True
    while onGoingMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and Mode == "Menu":
                box = game.getMenuBox()
                if box[0].collidepoint(pygame.mouse.get_pos()):
                    onGoingMenu = False
                    break
                elif box[1].collidepoint(pygame.mouse.get_pos()):
                    Mode = "Tutorial"
                    game.Tutorial()
                elif box[2].collidepoint(pygame.mouse.get_pos()):
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and Mode =="Tutorial":
                done = game.nextTut()
                if done == True:
                    Mode = "Menu"
                    game.Menu()
            pygame.display.update()
    #game control
    onGoingGame = True
    humanPlayer = True
    game.Begin()
    random.seed()
    game.turnFill(humanPlayer)

    while onGoingGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if humanPlayer:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    CircleBoxes = game.getCircleClick()
                    for i in CircleBoxes:
                        x = CircleBoxes.index(i)
                        if i.collidepoint(pygame.mouse.get_pos()) and len(game.getBoardPieces()[x]) != 0:
                            lastplace = game.move(x,13)
                            if lastplace != 6:
                                humanPlayer = not humanPlayer
                                game.turnFill(humanPlayer)
                            else:
                                game.Extra()
                            if lastplace < 6 and len(game.getBoardPieces()[lastplace])==1:
                                game.collect(abs(12-lastplace),6)
            else:
                pick = []
                for i in game.getBoardPieces()[7:13]:
                    if len(i) > 0:
                        pick.append(game.getBoardPieces().index(i))
                if pick != []:
                    lastplace = game.move(random.choice(pick),6)
                    if lastplace != 13:
                        humanPlayer = not humanPlayer
                        game.turnFill(humanPlayer)
                    else:
                        game.Extra()
                    if lastplace > 6 and len(game.getBoardPieces()[lastplace])==1:
                         game.collect(abs(12-lastplace),13)
            if game.Clear(): #check for end of game
                onGoingGame = False
    game.End()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == MOUSEBUTTONDOWN:
                terminate()
if __name__ == "__main__":
    main()
