import pygame
from Constants import Constants
from Enemy import Enemy
from Player import Player
from Vector import Vector

#initialize pygame and setting screen size
pygame.init()
display = pygame.display.set_mode((Constants.Screen_Width,Constants.Screen_Height))
#setting display caption
pygame.display.set_caption('Moving Agents')

#setting clock
clock = pygame.time.Clock()

#Creating the player object
playerChar = (Player)(Constants.Player_Initial_Spawn,Constants.Player_Speed,Constants.Player_Size)

enemyVec = (Vector)(100,100)


#creating enemy for testing
enemyChar = (Enemy)(enemyVec,10,1)
enemyChar2 = (Enemy)((Vector)(450,450),10,1)
enemyList = [enemyChar,enemyChar2]

exit = False

while not exit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        
    #Clears display
    display.fill(Constants.Background_Color)

    playerChar.update(enemyList)
    enemyChar.update(playerChar)

    enemyChar.draw(display)
    enemyChar2.draw(display)
    playerChar.draw(display)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()