import pygame
import random
from Constants import Constants
from Enemy import Enemy
from Player import Player
from Vector import Vector
from Agent import Agent

###############################
#
# Cameron Morris
# 9/13/2024
# cmorris@uccs.edu
#
# Main class of magical abilities and techniques
###############################

#initialize pygame and setting screen size
pygame.init()
display = pygame.display.set_mode((Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT))
#setting display caption
pygame.display.set_caption('Moving Agents')

#setting clock
clock = pygame.time.Clock()

spawnLoc = (Vector)(260,260)
spawnLoc2 = (Vector)(600,300)

#Creating the player object
playerChar = (Player)(Constants.Player_Initial_Spawn,Constants.Player_Speed,Constants.Player_Size)


enemyList = []

for i in range(Constants.Enemy_Spawn_Count):
    #Getting random spawn location
    xLoc = random.randint(0,Constants.SCREEN_WIDTH)
    yLoc = random.randint(0,Constants.SCREEN_HEIGHT)

    #Vector for that location
    spawnLoc = (Vector)(xLoc,yLoc)

    #Spawning enemy at random location
    enemyChar = (Enemy)(spawnLoc,Constants.Enemy_Speed,Constants.Enemy_Size)

    enemyList.append(enemyChar)

playerChar.update(enemyList)
exit = False

while not exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        
    #Clears display
    display.fill(Constants.Background_Color)
    
    playerChar.update(enemyList)
    
    for val in enemyList:
        val.update(playerChar)
    
    playerChar.draw(display)
    for val in enemyList:
        val.draw(display,playerChar)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()