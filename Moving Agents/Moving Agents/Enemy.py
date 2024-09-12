from Vector import Vector
from Agent import Agent
from Constants import Constants
import pygame
import random

class Enemy(Agent):
    #constructor for the enemy
    def __init__(self,spawnPosition,enemySize,initialSpeed):
        super().__init__(spawnPosition,enemySize,initialSpeed)

    def __str__(self):
        return ('Enemy Position: ' + str(self.position) + ' Enemy Velocity: ' + str(self.velocity) + ' Enemy Size: ' + str(self.size) + ' Enemy Center: ' + str(self.center))


    def draw(self,screen):
        #draw the enemy
        super().draw(screen,Constants.Enemy_Color)
        

    def update(self,player):
        #calculate if the player is within alert range
        dist = self.distBetweenAgents(player)
        if(dist < Constants.Enemy_Detection_Dist):
            self.flee(player)
        else:
            self.wander()

        #calling parent update
        super().update()

    def flee(self,player):
        #calculate direction to run in
        dirVec = self.position - player.position
        self.velocity = self.setSpeedVec(dirVec)
        self.drawTargetLine = True
 

    def wander(self): 
        
        #add a small random to both X and Y velocity
        self.velocity.x += random.uniform(-Constants.Enemy_Random_Wander_Factor,Constants.Enemy_Random_Wander_Factor)
        self.velocity.y += random.uniform(-Constants.Enemy_Random_Wander_Factor,Constants.Enemy_Random_Wander_Factor)
        
        #lmao square snorted some coke with this method
        #NOTE UNCOMMENT THESE LINES OF CODE TO SEE THE SQUARES DO A FUNNY :)
        #I WROTE THESE LINES OF CODE AT LIKE 4AM BECAUSE I THOUGHT IT MIGHT BE FUNNY
        #self.velocity.x = random.uniform(-Constants.Enemy_Random_Wander_Factor,Constants.Enemy_Random_Wander_Factor)
        #self.velocity.y = random.uniform(-Constants.Enemy_Random_Wander_Factor,Constants.Enemy_Random_Wander_Factor)

        #calling parent method to normalize and set velocity to proper speed
        self.velocity = self.setSpeedVec(self.velocity)
        


