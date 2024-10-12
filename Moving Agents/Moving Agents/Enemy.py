from math import cos
from math import sin
from Vector import Vector
from Agent import Agent
from Constants import Constants
import pygame
import random

###############################
#
# Cameron Morris
# 10/12/2024
# cmorris@uccs.edu
#
#Enemy Class Child of Agent
###############################


class Enemy(Agent):
    #constructor for the enemy
    def __init__(self,spawnPosition,enemySize,initialSpeed, image):
        super().__init__(spawnPosition,enemySize,initialSpeed,image, Constants.Enemy_Turn_Radius)
        self.surf
        self.neighbors = []

    def __str__(self):
        return ('Enemy Position: ' + str(self.position) + ' Enemy Velocity: ' + str(self.velocity) + ' Enemy Size: ' + str(self.size) + ' Enemy Center: ' + str(self.center))


    def draw(self,screen,player):
        #draw the enemy
        super().draw(screen,Constants.Enemy_Color)

        #draw neighbor lines
        if(Constants.DEBUG_NEIGHBORS):
            self.drawNeighborLines(screen)

        #draw fleeing lying if fleeing
        if(self.drawTargetLine):
            pygame.draw.line(screen,Constants.Flee_Line_Color,(self.center.x, self.center.y),(player.center.x,player.center.y),Constants.Line_Thickness)
        

    def update(self,player):
        #calculate if the player is within alert range
        dist = self.distBetweenAgents(player)
        if(dist < Constants.Enemy_Detection_Dist):
            self.flee(player)
        else:
            self.drawTargetLine = False

        self.calcHerdForces()

        #calling parent update
        super().update()

    def flee(self,player):
        #calculate direction to run in
        dirVec = self.position - player.position

        #normalizing the direction
        dirVec = dirVec.normalize()

        #scaling by the weight
        self.appliedForce += dirVec.scale(Constants.Enemy_Flee_Force_Weight * int(Constants.ENABLE_DOG))
        if(Constants.DEBUG_DOG_INFLUENCE):
            self.drawTargetLine = True
        else:
            self.drawTargetLine = False

    def calcHerdForces(self):
        alignmentVec = (Vector)(0,0)
        cohesionVec = (Vector)(0,0)
        separationVec = (Vector)(0,0)
        for agent in self.neighbors:
            #Add neighbors direction to alignmentVec
            alignmentVec += agent.velocity
            #add position to cohesion
            cohesionVec += agent.position
            #add distance to separation 
            separationVec += (agent.position - self.position)
        #calculate the average
        val = len(self.neighbors)
        alignmentVec.x /= val
        alignmentVec.y /= val
        cohesionVec.x /= val
        cohesionVec.y /= val
        separationVec.x /= val
        separationVec.y /= val
        #scale separation vec by -1
        separationVec.x *= -1
        separationVec.y *= -1
        #normalize all vectors
        alignmentVec = alignmentVec.normalize()
        cohesionVec = cohesionVec.normalize()
        separationVec = separationVec.normalize()

        #scaling by weights
        alignmentVec = alignmentVec.scale(Constants.Alignment_Force_Weight * int(Constants.ENABLE_ALIGNMENT))
        cohesionVec = cohesionVec.scale(Constants.Cohesion_Force_Weight * int(Constants.ENABLE_COHESION))
        separationVec = separationVec.scale(Constants.Seperation_Force_Weight * int(Constants.ENABLE_SEPARATION))

        #applying the force
        self.appliedForce += alignmentVec + cohesionVec + separationVec

    def drawNeighborLines(self, screen):
        for agent in self.neighbors:
            pygame.draw.line(screen,Constants.Neighbor_Line_Color,(self.center.x, self.center.y), (agent.center.x, agent.center.y), 1)



    # def wander(self): 
    #     #set draw target line to false since not fleeing
    #     self.drawTargetLine = False

    #     dirVec = (Vector) (self.velocity.x, self.velocity.y)

    #     #add a small random to both X and Y velocity
    #     dirVec.x += random.uniform(-Constants.Enemy_Random_Wander_Factor,Constants.Enemy_Random_Wander_Factor)
    #     dirVec.y += random.uniform(-Constants.Enemy_Random_Wander_Factor,Constants.Enemy_Random_Wander_Factor)

    #     #normalizing dirVec
    #     dirVec.normalize()

    #     #Scaling by the wegith
    #     self.appliedForce = dirVec.scale(Constants.Enemy_Wander_Force_Weight)

        


