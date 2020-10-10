import pygame
import numpy as np
import time 

class engine_game:
    """
    Coordinates all the game logic with pygame
    """

    def draw_text(self,surface, text, size, x,y):
        """
        Draws marker and generations in screen
        """
        font=pygame.font.SysFont("serif", size)
        text_surface=font.render(text, True, (220,20,60))
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        surface.blit(text_surface,text_rect)

    def __init__(self, numCells_X, numCells_Y):
        """
        Inits the game with some parameters
        """
        pygame.init()

        pygame.display.set_caption("Juego de la vida - Curso Python - Alejandro")

        self.width, self.height=800,800 #game screen
        self.screen = pygame.display.set_mode((self.height, self.width))

        self.background_color =25,25,25
        self.screen.fill(self.background_color)

        self.numCells_X, self.numCells_Y= numCells_X,numCells_Y #num cells

        self.dimensionCW=self.width/self.numCells_X
        self.dimensionCH=self.height/self.numCells_Y

        self.gameStatus=np.zeros((self.numCells_X, self.numCells_Y))

        self.paused =False
        self.endGame=False

        self.numGen=0
        self.num_living_cells=0

        #Check automata, commmented, just for tests
        self.gameStatus[21, 21] = 1
        self.gameStatus[22, 22] = 1
        self.gameStatus[22, 23] = 1
        self.gameStatus[21, 23] = 1
        self.gameStatus[20, 23] = 1
    
    def getGameStatus(self):
        """
        Returns copy of gameStatus variable that contains the matrix with all the cells
        """    
        return self.gameStatus.copy()

    def setGameStatus(self, gmSt):
        """
        Sets gameStatus to computed gameStatus, must be called before run too see updates in grid
        """
        self.gameStatus=np.copy(gmSt)
    
    def getPaused(self):
        """
        Returns paused variable that informs if the game is paused
        """
        return self.paused

    def drawBlocks(self):
        """
        Just flush and then draws the game mesh with gameStatus in mind
        """
        self.screen.fill(self.background_color)
        for y in range(0, self.numCells_X):
            for x in range(0, self.numCells_Y):
                #blocks is each square 
                self.blocks=[((x)*self.dimensionCW,y*self.dimensionCH),
                    ((x+1)*self.dimensionCW, y*self.dimensionCH),
                    ((x+1)*self.dimensionCW, (y+1)*self.dimensionCH),
                    ((x)*self.dimensionCW, (y+1)*self.dimensionCH)]
                #Draw a square in each space with corresponding color
                if self.gameStatus[x,y]==0:
                    pygame.draw.polygon(self.screen, (128, 128, 128), self.blocks, width=1)
                else:
                    pygame.draw.polygon(self.screen, (255, 255, 255), self.blocks, width=0)
                    self.num_living_cells+=1
   
    def hasFinished(self):
        """
        Returns True when user clicks end button
        """
        return self.endGame

    def run(self):
        """
        Must be called to update with every interaction of the game
        """
        time.sleep(0.01)
        if not self.paused:
            self.numGen+=1
        events=pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.paused=not self.paused
            mouseClick=pygame.mouse.get_pressed()
            if sum(mouseClick)>0:
                posX,posY=pygame.mouse.get_pos()
                clickedX,clickedY=int(np.floor(posX/self.dimensionCW)),int(np.floor(posY/self.dimensionCH))
                self.gameStatus[clickedX,clickedY]= not self.gameStatus[clickedX,clickedY]
            if event.type == pygame.QUIT:
                self.endGame = True
        self.num_living_cells=0
        self.drawBlocks()

        self.draw_text(self.screen, "Vivos: "+str(self.num_living_cells)+" - Generación: "+str(self.numGen),25,150,10)
        pygame.display.flip()

    
