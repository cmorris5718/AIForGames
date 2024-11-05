from Constants import *
from pygame import *
from random import *
from Vector import *
from Agent import *
from Sheep import *
from Dog import *
from Graph import *
from Node import *
from GameState import *

class StateMachine:
	""" Machine that manages the set of states and their transitions """

	def __init__(self, startState):
		""" Initialize the state machine and its start state"""
		self.__currentState = startState
		self.__currentState.enter()

	def getCurrentState(self):
		""" Get the current state """
		return self.__currentState

	def update(self, gameState):
		""" Run the update on the current state and determine if we should transition """
		nextState = self.__currentState.update(gameState)

		# If the nextState that is returned by current state's update is not the same
		# state, then transition to that new state
		if nextState != None and type(nextState) != type(self.__currentState):
			self.transitionTo(nextState)

	def transitionTo(self, nextState):
		""" Transition to the next state """
		self.__currentState.exit()
		self.__currentState = nextState
		self.__currentState.enter()

	def draw(self, screen):
		""" Draw any debugging information associated with the states """
		self.__currentState.draw(screen)

class State:
	def enter(self):
		""" Enter this state, perform any setup required """
		print("Entering " + self.__class__.__name__)
		
	def exit(self):
		""" Exit this state, perform any shutdown or cleanup required """
		print("Exiting " + self.__class__.__name__)

	def update(self, gameState):
		""" Update this state, before leaving update, return the next state """
		print("Updating " + self.__class__.__name__)

	def draw(self, screen):
		""" Draw any debugging info required by this state """
		pass

			   
class FindSheepState(State):
	""" This is an example state that simply picks the first sheep to target """
	def enter(self):
		super().enter()
		self.time = time.get_ticks()

	def update(self, gameState):
		""" Update this state using the current gameState """
		super().update(gameState)
		dog = gameState.getDog()

		# Pick a random sheep
		dog.setTargetSheep(gameState.getHerd()[0])

		# if((time.get_ticks() - self.time) / 1000 > 15):
		# 	return Charge()
		if(dog.path == None):
			return
		if(len(dog.path) > 0):
			return FindSheepState()

		# You could add some logic here to pick which state to go to next
		# depending on the gameState
		#Calculate new target path
		penOpenCenter = Vector(520,312)
		target = dog.getTargetSheep().center
		directionAwayFromPen = penOpenCenter - target
		directionAwayFromPen = directionAwayFromPen.normalize()
		directionAwayFromPen = directionAwayFromPen.scale(Constants.GRID_SIZE * 4)
		target = target - directionAwayFromPen
		node = gameState.getGraph().getNodeFromPoint(target)
		attempts = 0
		while(node.isWalkable == False and attempts < 10):
			target = target - Vector(Constants.GRID_SIZE, Constants.GRID_SIZE)
			node = gameState.getGraph().getNodeFromPoint(target)
			attempts = attempts + 1

		if(attempts == 10):
			return Charge()

		dog.calculatePathToNewTarget(target)


		return FindSheepState()

class Idle(State):
	""" This is an idle state where the dog does nothing """

	def update(self, gameState):
		super().update(gameState)
		
		# Do nothing
		if len(gameState.getHerd()) > 0:
			return FindSheepState()
		else:
			return Idle()

class Charge(State):

	def enter(self):
		self.time = time.get_ticks()

	def update(self, gameState):
		super().update(gameState)

		dog = gameState.getDog()
		dog.calculatePathToNewTarget(dog.getTargetSheep().center)

		if((time.get_ticks() - self.time) / 1000 > 5):
			return Idle()
		else:
			return Charge()