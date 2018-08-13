'''
Lap Nguyen
CS 386
Due Date 11/12/15
Description:This program contains the class for drawing and containing the game state
'''
import pygame
from pygame.locals import *
import random
WHITE = (255,255,255)
BROWN = (255, 228, 196)
GREEN = (0,255,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
class Game:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((640,480),0,32)
        pygame.display.set_caption("Mancala!")
        self._clock = pygame.time.Clock()
        self._basicFont = pygame.font.SysFont(None, 48)
    #This method handles the drawing for the menu screen and creates
    #the necessary fields for the redrawing the menu if needed
    def Menu(self):
        #texts
        self._screen.fill(BLACK)
        mancala = self._basicFont.render('Mancala!', True, BLACK, BLUE)
        text = self._basicFont.render('PlayGame', True, BLACK, BLUE)
        tutorialBox = self._basicFont.render('Tutorial', True, BLACK, BLUE)
        quitBox = self._basicFont.render('Quit Game', True, BLACK, BLUE)
        
        mancalaRect = mancala.get_rect()
        mancalaRect.centerx = self._screen.get_rect().centerx 
        mancalaRect.centery = self._screen.get_rect().centery - 100
        #blit texts to center
        textRect = text.get_rect()
        textRect.centerx = self._screen.get_rect().centerx
        textRect.centery = self._screen.get_rect().centery
        
        tutorialRect = tutorialBox.get_rect()
        tutorialRect.centerx = self._screen.get_rect().centerx
        tutorialRect.centery = self._screen.get_rect().centery + 50

        quitRect = quitBox.get_rect()
        quitRect.centerx = self._screen.get_rect().centerx
        quitRect.centery = self._screen.get_rect().centery + 100
        
        self._screen.blit(mancala,mancalaRect)
        self._screen.blit(text,textRect)
        self._screen.blit(tutorialBox,tutorialRect)
        self._screen.blit(quitBox,quitRect)
        self._MenuBox = [textRect,tutorialRect,quitRect]
        pygame.display.flip()
    #this method only sets up the tutorial items
    def Tutorial(self):
        self._head = 0
        self._tutorialimg = ["goal.jpg","moves.jpg","counterclockwise.jpg","stores.jpg","collect.jpg"]
        self.nextTut()
    #this method only moves to the next item in the tutorial and returns whether or not the
    #tutorial has finished
    def nextTut(self):
        self._screen.fill(WHITE)
        img = pygame.image.load(self._tutorialimg[self._head]).convert()
        self._screen.blit(img,(0,0))
        self._head+= 1
        pygame.display.update()
        if self._head == 5:
            return True
        else:
            return False
    #getter for MenuBox - used to check for clickbox collisions
    def getMenuBox(self):
        return self._MenuBox
    #this method is used to initialize all fields for the game methods
    # and the initial board draw must be called before all the other game methods below
    def Begin(self):
        self._screen.fill(WHITE)
        #rects to draw shapes
        boarditem = pygame.Rect(0,100,640,230)
        store = pygame.Rect(10,130, 50,160)
        store2 = pygame.Rect(580,130,50,160)
        #fields to store the board state
        self._board = [boarditem,store,store2] # board and stores
        self._circletop = [(110+(x*85),160) for x in range(6)] # circles at top
        self._circlebot = [(110+(x*85),265) for x in range(6)] # circles at bottom
        self._circleClick = [] # stores rects for clicking on circles
        self._circleTopDraw = [] #rects for ensuring same appearance on the top
        self._animTop = [] #inscribes a smaller rect inside of the circles to ensure
        self._animBot = [] #seeds in the the circles
        #create rects for clickboxes for the user
        for x in self._circlebot:
            i = pygame.Rect(0,0,80,80)
            i.center = x
            self._circleClick.append(i)
        for x in self._circletop:
            i = pygame.Rect(0,0,80,80)
            i.center = x
            self._circleTopDraw.append(i)
        #animation boxes smaller squares inside circles
        for i,j in zip(self._circletop,self._circlebot):
            k = pygame.Rect(0,0,50,50)
            m = pygame.Rect(0,0,50,50)
            k.center = i
            self._animTop.append(k)
            m.center = j
            self._animBot.append(m)
        self._tempStor1 = pygame.Rect(580,175,50,50)
        self._tempStor2 = pygame.Rect(13,170,50,50)

        #creating the initial board state
        self._boardPieces = []
        #create seeds for the bottom half           
        for i,j in zip(range(7),self._animBot):
            temp = []
            for k in range(4):
                x = random.randint(j.x,j.x+j.w)
                y = random.randint(j.y,j.y+j.h)
                temp.append((x,y))
            self._boardPieces.append(temp)
        self._boardPieces.append([])
        #create seeds for the top half
        tempRev = list(reversed(self._animTop))
        for i,j in zip(range(7,13),tempRev):
            temp = []
            for k in range(4):
                x = random.randint(j.x,j.x+j.w)
                y = random.randint(j.y,j.y+j.h)
                temp.append((x,y))
            self._boardPieces.append(temp)
        self._boardPieces.append([])   
        self.redraw()
        pygame.display.update() # update the screen to the user
    #this method redraws the entire state of the board
    def redraw(self):
        pygame.draw.rect(self._screen,BROWN,self._board[0])
        pygame.draw.ellipse(self._screen,WHITE,self._board[1])
        pygame.draw.ellipse(self._screen,WHITE,self._board[2])    
        for x,y in zip(self._circletop,self._circlebot):
            pygame.draw.circle(self._screen,WHITE,x,40)
            pygame.draw.circle(self._screen,WHITE,y,40)
            tempLength = len(self._boardPieces)
        #seed draw
        for i in range(tempLength):
            circleItems = len(self._boardPieces[i])
            for j in range(circleItems):
                pygame.draw.circle(self._screen,GREEN,self._boardPieces[i][j],10,1)
        #textboxes
        self._text = []
        #blit boxes
        for i in self._boardPieces:
            self._text.append(self._basicFont.render(str(len(i)), True, BLACK,WHITE))                
        for i,j in zip(self._text[0:7],self._circleClick):
            self._screen.blit(i,j.center)
        for i,j in zip(self._text[7:13],self._circleTopDraw[::-1]):
            self._screen.blit(i,j.center)         
        self._screen.blit(self._text[6],self._board[2])
        self._screen.blit(self._text[13],self._board[1])
    #this method returns the list of the click boxes for the circles
    def getCircleClick(self):
        return self._circleClick
    #this method returns the list of the board pieces
    def getBoardPieces(self):
        return self._boardPieces
    #this method determines whether or not the game has ended
    def Clear(self):
        Clear = False
        for i in self._boardPieces[:6]:
            if len(i) > 0:
                Clear = False
                break
        else:
            Clear = True
        if Clear == False:
            for i in self._boardPieces[7:13]:
                if len(i) > 0:
                    Clear = False
                    break
            else:
                Clear = True
        return Clear
    #this method returns the score
    def tally(self):
        x,y = 0,0
        for i in range(7):
          x += len(self._boardPieces[i])
          y += len(self._boardPieces[i+7])
        return x,y
    #this method moves each seed to stone
    #pos is where the stone was picked value must be in 0-13
    #store is the opposing player's store must be a 6 or 13
    #and returns the position of the where the last stone is
    #to process what move can be done
    def move(self,pos,store):
        seeds = len(self._boardPieces[pos]) #obtain seeds
        i = 0
        while self._boardPieces[pos] != []:
            i = i + 1
            nextPos = (pos + i) % 14
            while nextPos == store:
                i = i + 1
                nextPos = (pos + i) % 14
            nextBox = pygame.Rect(0,0,0,0)
            #area to get the box
            if nextPos == 6:
                nextBox = self._tempStor1
            elif nextPos == 13:
                nextBox = self._tempStor2
            elif nextPos > 6:
                nextBox = self._animTop[abs(12-nextPos)]
            else:
                nextBox = self._animBot[nextPos]
            self.newCircle(nextBox,nextPos,pos)
        self.redraw()
        pygame.display.update()
        return nextPos
    #this method draws the circle as it moves
    def newCircle(self,nextBox,nextPos,pos):
        newX = random.randint(nextBox.x,nextBox.x+nextBox.w)
        newY = random.randint(nextBox.y,nextBox.y+nextBox.h)
        newLoc = (newX,newY)
        oldLoc = self._boardPieces[pos].pop()
        while oldLoc != newLoc:
            if oldLoc[0] != newX:
                if oldLoc[0] > newX:
                    oldLoc = (oldLoc[0]-1,oldLoc[1])
                else:
                    oldLoc = (oldLoc[0]+1,oldLoc[1])
            else:
                if oldLoc[1] < newY:
                    oldLoc = (oldLoc[0],oldLoc[1]+1)
                else:
                    oldLoc = (oldLoc[0],oldLoc[1]-1)
            self.redraw()
            pygame.draw.circle(self._screen,RED,oldLoc,10,1)
            pygame.display.update()
        self._boardPieces[nextPos].append(newLoc)
    #this method display a text to know if a player gets an extra turn
    def Extra(self):
        text = self._basicFont.render("You get an Extra Turn!", True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.centerx = 200 
        textRect.centery = 50
        self._screen.blit(text,textRect)
        self.redraw()
        pygame.display.update()
        pygame.time.delay(200)

    #this method display a text to know which player's
    #turn it is
    def turnFill(self,human):
        self._screen.fill(WHITE)
        txt =""
        if human:
            txt = "Your Turn"
        else:
            txt = "Opponent's Turn"
        #blit texts to center
        text = self._basicFont.render(txt, True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.centerx = 200 
        textRect.centery = 400
        self._screen.blit(text,textRect)
        self.redraw()
        pygame.display.update()
        pygame.time.delay(200)
    #this method moves all of the seeds to a store in a collect move
    #pos value must be 0-13
    #store value must be 6 or 13 and is the store for the player
    def collect(self,pos,store):
        while self._boardPieces[pos] != []:
            nextBox = pygame.Rect(0,0,0,0)
            #area to get the box
            if store == 6:
                nextBox = self._tempStor1
            elif store == 13:
                nextBox = self._tempStor2
            #make in a new spot
            self.newCircle(nextBox,store,pos)
        self.redraw()
        pygame.display.update()
    #this method draws the end game to screen
    def End(self):
        self._screen.fill(WHITE)
        text = 'End of Game! - '
        if self.tally()[0] > self.tally()[1]:
            text+="You Win"
        elif self.tally()[0] <self.tally()[1]:
            text+="You Lose"
        else:
            text+="TIE"
        text = self._basicFont.render(text, True, BLACK, WHITE)
        score = self._basicFont.render(str(self.tally()[0])+"-"+str(self.tally()[1]), True, BLACK, WHITE)
        close = self._basicFont.render("Click anywhere to close", True, BLACK, WHITE)

        textRect = text.get_rect()
        textRect.centerx = self._screen.get_rect().centerx
        textRect.centery = self._screen.get_rect().centery
        
        scorerect = score.get_rect()
        scorerect.centerx = self._screen.get_rect().centerx
        scorerect.centery = self._screen.get_rect().centery + 50

        closerect = close.get_rect()
        closerect.centerx = self._screen.get_rect().centerx
        closerect.centery = self._screen.get_rect().centery + 100
        
        self._screen.blit(text,textRect)
        self._screen.blit(score,scorerect)
        self._screen.blit(close,closerect)
        pygame.display.update()
        
