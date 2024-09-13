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
        self.currentEnemyIndex = 0

    #string method for class
    def __str__(self):
        return ('Player Position: ' + str(self.position) + ' Player Velocity: ' + str(self.velocity) + ' Player Size: ' + str(self.size) + ' Player Center: ' + str(self.center))
    
    #method to draw the player
    def draw(self,screen):
        #draw the player
        super().draw(screen,Constants.Player_Color)
        #draw the line to the target
        pygame.draw.line(screen, Constants.Flee_Line_Color, (self.center.x, self.center.y), (self.currentTarget.center.x, self.currentTarget.center.y), Constants.Line_Thickness)

    #method to update the position and behavior of the player
    def update(self,enemyList):
        #if player has no target find the closest enemy without any filters
        if(self.currentTarget == None):
            self.findNextEnemy(enemyList)
        #if the player has hit it's current target find the closest enemy that's not
        #the one that's just been hit
        elif(self.hasHitCurrentTarget):
            #self.currentTarget = self.findClosestEnemy(enemyList,self.currentTarget)
            self.findNextEnemy(enemyList)
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


    #iterate through list of enemies tagging them one by one
    def findNextEnemy(self,enemyList):
        #setting proper index
        self.currentEnemyIndex += 1
        if(self.currentEnemyIndex == len(enemyList)):
            self.currentEnemyIndex = 0

        #setting target as enemy
        self.currentTarget = enemyList[self.currentEnemyIndex]

    #method to find the closest enemy from the given list
    #can exclude an enemy to avoid constantly hovering over a currently colliding enemy
    #Was using this but player and multiple enemies could get stuck in a corner so switched
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

        

    


        





