from Vector import Vector
from Constants import Constants
import pygame
import math

###############################
#
# Cameron Morris
# 10/5/2024
# cmorris@uccs.edu
#
#Agent Parent Class
###############################

class Agent:
    #constructor for agent class
    def __init__(self,position,initialSpeed,size,image, turn):
        self.position = position
        self.velocity = (Vector)(0,0)
        self.speed = initialSpeed
        self.size = size
        self.center = self.calculateCenter()
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        self.appliedForce = (Vector) (0,0)
        self.angle = -45
        self.image = image
        self.surf = pygame.transform.rotate(self.image, self.angle)
        self.turn = turn
        
    #draws a rectangle representing the agent 
    def draw(self, screen, color):
        #drawing the agent
        self.angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x)) - 90
        self.surf = pygame.transform.rotate(self.image, self.angle)

        #calculating the upper left corner
        upperCorner = (Vector)(self.center.x - self.surf.get_width() / 2, self.center.y - self.surf.get_height() / 2)
        screen.blit(self.surf, [upperCorner.x, upperCorner.y])

        #drawing the agent's velocity line
        endPos = (Vector)(self.center.x + self.velocity.x * 2, self.center.y + self.velocity.y * 2)
        pygame.draw.line(screen,Constants.Velocity_Line_Color,(self.center.x, self.center.y),(endPos.x, endPos.y),Constants.Line_Thickness)

    #updates the position of the agent
    def update(self):
        #calculating the forces from the boundary
        self.calculateBoundaryForces()

        #normalizing and scaling applied force
        self.appliedForce = self.appliedForce.normalize()

        diffVec = self.appliedForce - self.velocity.normalize()

        if(diffVec.length() < self.turn):
            print('')
            #setting velocity
            self.velocity = self.appliedForce
        else:
            print('')
            diffVec = diffVec.normalize()
            diffVec = diffVec.scale(self.turn)
            self.velocity = self.velocity.normalize() + diffVec


        #scaling velocity by speed
        self.velocity = self.velocity.scale(self.speed)

        #adding velocity to position
        self.position += self.velocity  

        #checking the bounds
        self.checkBounds()

        #recalculate centers
        self.center = self.calculateCenter()

        #Calculating the rect of this agent
        self.calculateBoundingRec()
        self.rect = self.rect.move(self.center.x - self.surf.get_width() / 2, self.center.y - self.surf.get_height() / 2)


    #normalizes and scales a vector to the proper speed per agent
    def setSpeedVec(self,vec):
        
        #normalize the vector
        vec = vec.normalize()       

        #scale by the speed
        vec = vec.scale(self.speed)        

        return vec

    #calculates the center of the given agent
    def calculateCenter(self):
        #set centerPos to initial position and add half the size
        centerPos = (Vector)(self.position.x, self.position.y)
        centerPos.x += self.size/2
        centerPos.y += self.size/2

        #return the center vector
        return centerPos

    def calculateBoundingRec(self):
        self.rect = self.surf.get_bounding_rect()

    #Checks if there's  collision between two input agents
    def checkAgentCollision(self, otherRect):
        selfRect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)
        return pygame.Rect.colliderect(selfRect, otherRect)

    #method to clamp the agents to the screen
    def checkBounds(self):
        #Checks if the left side of the square is off the left side of the screen and adjusts accordingly
        if(self.position.x < 0):
            self.position.x = 0
        #Checks if the right side of the square is off the right side of the screen and adjusts accordingly
        elif(self.position.x > Constants.SCREEN_WIDTH - self.size):
            self.position.x = Constants.SCREEN_WIDTH - self.size
        #checks if the top of the square is off the top of the screen and adjusts accordingly
        if(self.position.y < 0):
            self.position.y = 0
        #checks if the bottom of the square is off the bottom of the screen and adjusts accordingly
        elif(self.position.y > Constants.SCREEN_HEIGHT - self.size):
            self.position.y = Constants.SCREEN_HEIGHT - self.size

    #returns the distance between two agents
    def distBetweenAgents(self, other):
         dist = abs((self.position - other.position).length())
         return dist

    #calculates new rect
    def calcRect(self):
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        
    def calculateBoundaryForces(self):
        forceVec = (Vector)(0,0)
        if(self.position.x < Constants.Boundary_Threshhold):
            #we are by the left boundary
            #adjusting forceVec to have positive X value
            forceVec.x = abs(self.position.x - Constants.Boundary_Threshhold)
        elif(self.position.x > Constants.SCREEN_WIDTH - Constants.Boundary_Threshhold):
            #we are by the right boundary
            #adjusting forceVec to have negative X value
            forceVec.x = Constants.SCREEN_WIDTH - Constants.Boundary_Threshhold - self.position.x
        if(self.position.y < Constants.Boundary_Threshhold):
            #We are by the top boundary
            #Making forceVec have a negative Y value
            forceVec.y = -(self.position.y - Constants.Boundary_Threshhold)
        elif(self.position.y > Constants.SCREEN_HEIGHT - Constants.Boundary_Threshhold):
            #We are by the bottom boundary
            forceVec.y = self.position.y - Constants.SCREEN_HEIGHT - Constants.Boundary_Threshhold

        #scaling total boundary force by the weight
        forceVec = forceVec.scale(Constants.Boundary_Force_Weight)

        #Adding calculated force to applied forces
        self.appliedForce += forceVec
        


