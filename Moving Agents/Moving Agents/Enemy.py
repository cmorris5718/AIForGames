from Vector import Vector
from Agent import Agent
from Constants import Constants
import pygame
import random

###############################
#
# Cameron Morris
# 10/5/2024
# cmorris@uccs.edu
#
#Enemy Class Child of Agent
###############################


class Enemy(Agent):
    #constructor for the enemy
    def __init__(self,spawnPosition,enemySize,initialSpeed, image):
        super().__init__(spawnPosition,enemySize,initialSpeed,image, Constants.Enemy_Turn_Radius)
        self.surf

    def __str__(self):
        return ('Enemy Position: ' + str(self.position) + ' Enemy Velocity: ' + str(self.velocity) + ' Enemy Size: ' + str(self.size) + ' Enemy Center: ' + str(self.center))


    def draw(self,screen,player):
        #draw the enemy
        super().draw(screen,Constants.Enemy_Color)

        #draw fleeing lying if fleeing
        if(self.drawTargetLine):
            pygame.draw.line(screen,Constants.Flee_Line_Color,(self.center.x, self.center.y),(player.center.x,player.center.y),Constants.Line_Thickness)
        

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

        #normalizing the direction
        dirVec = dirVec.normalize()

        #scaling by the weight
        self.appliedForce = dirVec.scale(Constants.Enemy_Flee_Force_Weight)

        #normalizing the applied force
        self.appliedForce = self.appliedForce.normalize()

        self.drawTargetLine = True
 

    def wander(self): 
        #set draw target line to false since not fleeing
        self.drawTargetLine = False

        dirVec = (Vector) (self.velocity.x, self.velocity.y)

        #add a small random to both X and Y velocity
        dirVec.x += random.uniform(-Constants.Enemy_Random_Wander_Factor,Constants.Enemy_Random_Wander_Factor)
        dirVec.y += random.uniform(-Constants.Enemy_Random_Wander_Factor,Constants.Enemy_Random_Wander_Factor)

        #normalizing dirVec
        dirVec.normalize()

        #Scaling by the wegith
        self.appliedForce = dirVec.scale(Constants.Enemy_Wander_Force_Weight)

        


