from pygame.draw import line
from Vector import Vector
import pygame

class Player:
    #constructor
    def __init__(self,position, velocity, size):
        self.position = position
        self.velocity = velocity
        self.size = size

    def draw(self,screen,clock):
        #fills screen with black
        screen.fill((0, 0, 0))

        #draw the player
        pygame.draw.rect(screen, (0,128,255), pygame.Rect(self.position.x, self.position.y, self.size, self.size))

        #Calculating the center position of the player square
        centerPos = (Vector)(self.position.x, self.position.y)
        centerPos.x += self.size / 2
        centerPos.y += self.size / 2

        #Scaling velocity to calculate end point of line
        scaledVel = self.velocity.scale(self.size)

        #End point of the line
        endPos = (Vector)(centerPos.x + scaledVel.x, centerPos.y + scaledVel.y)
        
        #drawing the line using calculated center position and end position
        pygame.draw.line(screen,(255,0,255),(centerPos.x, centerPos.y),(endPos.x, endPos.y),3)

        #flip and increment clock
        pygame.display.flip()
        clock.tick(60)

    def update(self):
        #getting inputs
        pressed = pygame.key.get_pressed()

        #processing for vertical input
        if pressed[pygame.K_w]: self.velocity.y -= 1
        elif pressed[pygame.K_s]: self.velocity.y += 1
        else: self.velocity.y = 0

        #processing for horizontal input
        if pressed[pygame.K_a]: self.velocity.x -= 1
        elif pressed[pygame.K_d]: self.velocity.x += 1
        else: self.velocity.x = 0

        #normalize velocity
        Vector.normalize(self.velocity)

        #adjust player position based on normalized velocity
        self.position += self.velocity
        




