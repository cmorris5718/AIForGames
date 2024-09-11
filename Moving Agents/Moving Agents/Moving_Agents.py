import pygame
import random
from Constants import Constants
from Enemy import Enemy
from Player import Player
from Vector import Vector
from Agent import Agent

#initialize pygame and setting screen size
pygame.init()
display = pygame.display.set_mode((Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT))
#setting display caption
pygame.display.set_caption('Moving Agents')

#setting clock
clock = pygame.time.Clock()

spawnLoc = (Vector)(260,260)

#Creating the player object
playerChar = (Player)(Constants.Player_Initial_Spawn,Constants.Player_Speed,Constants.Player_Size)
enemyChar = (Enemy)(spawnLoc,Constants.Enemy_Speed,Constants.Enemy_Size)
enemyChar2 = (Enemy)(spawnLoc,Constants.Enemy_Speed,Constants.Enemy_Size)
enemyChar3 = (Enemy)(spawnLoc,Constants.Enemy_Speed,Constants.Enemy_Size)

enemyList = [enemyChar,enemyChar2]
'''
for i in range(Constants.Enemy_Spawn_Count):
    #Getting random spawn location
    xLoc = random.randint(0,Constants.SCREEN_WIDTH)
    yLoc = random.randint(0,Constants.SCREEN_HEIGHT)

    #Vector for that location
    spawnLoc = (Vector)(xLoc,yLoc)

    #Spawning enemy at random location
    enemyChar = (Enemy)(spawnLoc,Constants.Enemy_Size,Constants.Enemy_Size)

    enemyList.append(enemyChar)
'''

exit = False

while not exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        
    #Clears display
    display.fill(Constants.Background_Color)
    
    playerChar.update(enemyList)
    enemyChar.update(playerChar)
    enemyChar3.update(playerChar)
    #enemyChar2.update(playerChar)
    '''
    for val in enemyList:
        val.update(playerChar)
    '''
    playerChar.draw(display)
    enemyChar.draw(display)
    enemyChar2.draw(display)
    enemyChar3.draw(display)
    '''
    for val in enemyList:
        val.draw(display)
    '''
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()