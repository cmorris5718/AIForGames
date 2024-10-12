import pygame
import random
import math
from Constants import Constants
from Enemy import Enemy
from Player import Player
from Vector import Vector
from Agent import Agent

###############################
#
# Cameron Morris
# 10/5/2024
# cmorris@uccs.edu
#
# Main class of magical abilities and techniques
###############################

def handleDebugging():        
    # Handle the Debugging for Forces
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYUP:

            # Toggle Dog Influence
            if event.key == pygame.K_1:
                Constants.ENABLE_DOG = not Constants.ENABLE_DOG
                print("Toggle Dog Influence", Constants.ENABLE_DOG)

            # Toggle Alignment Influence
            if event.key == pygame.K_2: 
                Constants.ENABLE_ALIGNMENT = not Constants.ENABLE_ALIGNMENT
                print("Toggle Alignment Influence", Constants.ENABLE_ALIGNMENT)

            # Toggle Separation Influence
            if event.key == pygame.K_3: 
                Constants.ENABLE_SEPARATION = not Constants.ENABLE_SEPARATION
                print("Toggle Separation Influence", Constants.ENABLE_SEPARATION)

            # Toggle Cohesion Influence
            if event.key == pygame.K_4: 
                Constants.ENABLE_COHESION = not Constants.ENABLE_COHESION
                print("Toggle Cohesion Influence", Constants.ENABLE_COHESION)

            # Toggle Boundary Influence
            if event.key == pygame.K_5: 
                Constants.ENABLE_BOUNDARIES = not Constants.ENABLE_BOUNDARIES
                print("Toggle Boundary Influence", Constants.ENABLE_BOUNDARIES)

            # Toggle Dog Influence Lines
            if event.key == pygame.K_6: 
                Constants.DEBUG_DOG_INFLUENCE = not Constants.DEBUG_DOG_INFLUENCE
                print("Toggle Dog Influence Lines", Constants.DEBUG_DOG_INFLUENCE)
    
            # Toggle Velocity Lines
            if event.key == pygame.K_7: 
                Constants.DEBUG_VELOCITY = not Constants.DEBUG_VELOCITY
                print("Toggle Velocity Lines", Constants.DEBUG_VELOCITY)

            # Toggle Neighbor Lines
            if event.key == pygame.K_8: 
                Constants.DEBUG_NEIGHBORS = not Constants.DEBUG_NEIGHBORS
                print("Toggle Neighbor Lines", Constants.DEBUG_NEIGHBORS)

            # Toggle Boundary Force Lines
            if event.key == pygame.K_9: 
                Constants.DEBUG_BOUNDARIES = not Constants.DEBUG_BOUNDARIES
                print("Toggle Boundary Force Lines", Constants.DEBUG_BOUNDARIES)

            # Toggle Bounding Box Lines
            if event.key == pygame.K_0: 
                Constants.DEBUG_BOUNDING_RECTS = not Constants.DEBUG_BOUNDING_RECTS
                print("Toggle Bounding Box Lines", Constants.DEBUG_BOUNDING_RECTS)

def calcNeighbors(herd):
    #To iterate through each member of the herd
    for agent in herd:
        #set list to be an empty list
        agent.neighbors = []
        #Comparing the current member to all other members of the herd
        for otherAgent in herd:
            #Compare the position and add neighbor if within threshold
            distVal = (agent.position - otherAgent.position).length()
            if(distVal < Constants.Neighbor_Distance_Criteria):
                agent.neighbors.append(otherAgent)


#initialize pygame and setting screen size
pygame.init()
display = pygame.display.set_mode((Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT))
#setting display caption
pygame.display.set_caption('Moving Agents')

#getting the images
sheepImage = pygame.image.load('sheep.png')
dogImage = pygame.image.load('dog.png')

print(math.degrees(math.atan2(-5,5)))

#setting clock
clock = pygame.time.Clock()

spawnLoc = (Vector)(260,260)
spawnLoc2 = (Vector)(600,300)

#Creating the player object
playerChar = (Player)(Constants.Player_Initial_Spawn,Constants.Player_Speed,Constants.Player_Size,dogImage)


enemyList = []

for i in range(Constants.Enemy_Spawn_Count):
    #Getting random spawn location
    xLoc = random.randint(0,Constants.SCREEN_WIDTH)
    yLoc = random.randint(0,Constants.SCREEN_HEIGHT)

    #Vector for that location
    spawnLoc = (Vector)(xLoc,yLoc)

    #Spawning enemy at random location
    enemyChar = (Enemy)(spawnLoc,Constants.Enemy_Speed,Constants.Enemy_Size,sheepImage)

    enemyList.append(enemyChar)

playerChar.update(enemyList)
exit = False

while not exit:
    #handles debugging
    handleDebugging()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    
    

    #Checks for neighbors
    calcNeighbors(enemyList)

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

