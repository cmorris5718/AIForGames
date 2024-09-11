from Vector import Vector
from Constants import Constants
from Agent import Agent
import pygame

class Player(Agent):
    
    #constructor for player class
    def __init__(self,position,initialSpeed,size):
        #calling parent constructor
        super().__init__(position,initialSpeed,size)
        #Attributes for determining who current target is
        self.currentTarget = None
        self.hasHitCurrentTarget = False

    #string method for class
    def __str__(self):
        return ('Player Position: ' + str(self.position) + ' Player Velocity: ' + str(self.velocity) + ' Player Size: ' + str(self.size) + ' Player Center: ' + str(self.center))
    
    #method to draw the player
    def draw(self,screen):
        #draw the player
        pygame.draw.rect(screen, Constants.Player_Color, pygame.Rect(self.position.x, self.position.y, self.size, self.size))

    #method to update the position and behavior of the player
    def update(self,enemyList):
        #if player has no target find the closest enemy without any filters
        if(self.currentTarget == None):
            self.currentTarget = self.findClosestEnemy(enemyList)
        #if the player has hit it's current target find the closest enemy that's not
        #the one that's just been hit
        elif(self.hasHitCurrentTarget):
            self.currentTarget = self.findClosestEnemy(enemyList,self.currentTarget)
            self.hasHitCurrentTarget = False

        #Calculating the direction towards an enemy
        dirVec = self.currentTarget.position - self.position

        #using parent method to scale vector to proper speed
        dirVec = self.setSpeedVec(dirVec)

        #Setting velocity vector
        self.velocity = dirVec
        
        #calling parent update method
        super().update()
        #checking for collisions
        if(self.checkAgentCollision(pygame.Rect(self.currentTarget.position.x, self.currentTarget.position.y, self.currentTarget.size, self.currentTarget.size ))):
            self.hasHitCurrentTarget = True

    #method to find the closest enemy from the given list
    #can exclude an enemy to avoid constantly hovering over a currently colliding enemy
    def findClosestEnemy(self,enemyList,excludedEnemy = None):
        #setting variables and minDist to irrationally large value
        closestEnemy = None
        minDist = 100000

        #checking for closest enemy
        for val in enemyList:
            #Ignore the excludedEnemy
            if(val is excludedEnemy):
                pass
            else:
                #calculate the distance between player and enemy
                dist = self.distBetweenAgents(val)
                if(abs(dist) < minDist):
                    closestEnemy = val
                    minDist = abs(dist)

        #return the closest enemy
        return closestEnemy

        

    


        





