import pygame
from Vector import Vector
from Player import Player

#initialize pygame and set the display
pygame.init()
screen = pygame.display.set_mode((800, 600))
#set the clock for framerate purposes
clock = pygame.time.Clock()
#boolean for stopping the game
done = False

#starting position and velocity of the player
startPos = (Vector)(100,100)
startVel = (Vector)(0,0)

#Initial creation of the player
player1 = (Player)(startPos,startVel,30)
player1.draw(screen,clock)

#gameplay loop
while not done:
        #Check events for the quit action
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True      
        #update the player's location and draw the player
        player1.update()
        player1.draw(screen, clock)
     

        