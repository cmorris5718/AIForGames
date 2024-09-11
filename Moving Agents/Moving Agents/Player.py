from Vector import Vector
from Constants import Constants
import pygame

class Player:
    
    #constructor for player class
    def __init__(self,position,initialSpeed,size):
        self.position = position
        self.velocity = (Vector)(0,0)
        self.speed = initialSpeed
        self.size = size
        self.center = self.calculateCenter()
        self.currentTarget = None
        self.hasHitCurrentTarget = False

    def __str__(self):
        return ('Player Position: ' + str(self.position) + ' Player Velocity: ' + str(self.velocity) + ' Player Size: ' + str(self.size) + ' Player Center: ' + str(self.center))

    def calculateCenter(self):
        centerPos = (Vector)(self.position.x, self.position.y)
        centerPos.x += self.size/2
        centerPos.y += self.size/2
        return centerPos
    
    def draw(self,screen):
        #draw the player
        pygame.draw.rect(screen, Constants.Player_Color, pygame.Rect(self.position.x, self.position.y, self.size, self.size))

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
        dirVec = dirVec.normalize()
        dirVec = dirVec.scale(self.speed)
        
        #Setting velocity vector
        self.velocity = dirVec
        
        #adding velocity to position
        self.position += self.velocity

        #checking to see if tagged the enemy
        dist = abs((self.currentTarget.position - self.position).length())
        #if distance is below a threshold then you've hit your target
        #NOTE: This will be changed later
        if(dist < 5):
            self.hasHitCurrentTarget = True
        
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
                dist = (val.position - self.position).length()
                if(abs(dist) < minDist):
                    closestEnemy = val
                    minDist = abs(dist)

        #return the closest enemy
        return closestEnemy

        

    


        





