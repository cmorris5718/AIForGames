from Vector import Vector
from Constants import Constants
import pygame

class Agent:
    #constructor for agent class
    def __init__(self,position,initialSpeed,size):
        self.position = position
        self.velocity = (Vector)(0,0)
        self.speed = initialSpeed
        self.size = size
        self.center = self.calculateCenter()
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        
    #draws a rectangle representing the agent 
    def draw(self, screen, color):
        #drawing the agent
        pygame.draw.rect(screen, color, self.rect)

        #drawing the agent's velocity line
        endPos = (Vector)(self.center.x + self.velocity.x, self.center.y + self.velocity.y)
        pygame.draw.line(screen,Constants.Velocity_Line_Color,(self.center.x, self.center.y),(endPos.x, endPos.y),Constants.Line_Thickness)

    #updates the position of the agent
    def update(self):
        #adding velocity to position
        self.position += self.velocity  

        #checking the bounds
        self.checkBounds()

        #recalculate centers
        self.center = self.calculateCenter()

        #Calculating the rect of this agent
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)


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


