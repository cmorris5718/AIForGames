from Vector import Vector
import pygame
import random

class Enemy:
    def __init__(self,spawnPosition,enemySize,initialSpeed):
        self.position = spawnPosition
        self.velocity = (Vector)(0,0)
        self.speed = initialSpeed
        self.size = enemySize
        self.center = self.calculateCenter()

    def __str__(self):
        return ('Enemy Position: ' + str(self.position) + ' Enemy Velocity: ' + str(self.velocity) + ' Enemy Size: ' + str(self.size) + ' Enemy Center: ' + str(self.center))

    def calculateCenter(self):
        centerPos = (Vector)(self.position.x, self.position.y)
        centerPos.x += self.size/2
        centerPos.y += self.size/2
        return centerPos

    def draw(self,screen):
        #draw the enemy
        pygame.draw.rect(screen,(0,255,0),pygame.Rect(self.position.x,self.position.y,self.size,self.size))

    def update(self,player):
        #calculate if the player is within alert range
        dist = abs((self.position - player.position).length())
        print(dist)
        if(dist < 200):
            self.flee(player)
        else:
            self.wander()

        #adding velocity to position to move the enemy
        self.position += self.velocity

    def flee(self,player):
        #calculate direction to run in
        dirVec = self.position - player.position
        dirVec = dirVec.normalize()
        dirVec = dirVec.scale(self.speed)

        #set velocity to calculated vector
        self.velocity = dirVec
 

    def wander(self):
        #add a small random to both X and Y velocity
        self.velocity.x += random.uniform(-0.3,0.3)
        self.velocity.y += random.uniform(-0.3,0.3)

        #renormalize the velocity
        self.velocity = self.velocity.normalize()

        #scale to speed
        self.velocity = self.velocity.scale(self.speed)
        


