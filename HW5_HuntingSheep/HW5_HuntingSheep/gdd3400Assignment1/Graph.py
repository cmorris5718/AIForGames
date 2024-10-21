from re import L
from tkinter import CURRENT
import Constants
import Node
import pygame
import Vector

from pygame import *
from Vector import *
from Node import *
from enum import Enum

class SearchType(Enum):
	DJIKSTRA = 1
	A_STAR = 2
	BEST_FIRST = 3

class Graph():
	def __init__(self):
		""" Initialize the Graph """
		self.nodes = []			# Set of nodes
		self.obstacles = []		# Set of obstacles - used for collision detection

		# Initialize the size of the graph based on the world size
		self.gridWidth = int(Constants.WORLD_WIDTH / Constants.GRID_SIZE)
		self.gridHeight = int(Constants.WORLD_HEIGHT / Constants.GRID_SIZE)

		# Create grid of nodes
		for i in range(self.gridHeight):
			row = []
			for j in range(self.gridWidth):
				node = Node(i, j, Vector(Constants.GRID_SIZE * j, Constants.GRID_SIZE * i), Vector(Constants.GRID_SIZE, Constants.GRID_SIZE))
				row.append(node)
			self.nodes.append(row)

		## Connect to Neighbors
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				# Add the top row of neighbors
				if i - 1 >= 0:
					# Add the upper left
					if j - 1 >= 0:		
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j - 1]]
					# Add the upper center
					self.nodes[i][j].neighbors += [self.nodes[i - 1][j]]
					# Add the upper right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j + 1]]

				# Add the center row of neighbors
				# Add the left center
				if j - 1 >= 0:
					self.nodes[i][j].neighbors += [self.nodes[i][j - 1]]
				# Add the right center
				if j + 1 < self.gridWidth:
					self.nodes[i][j].neighbors += [self.nodes[i][j + 1]]
				
				# Add the bottom row of neighbors
				if i + 1 < self.gridHeight:
					# Add the lower left
					if j - 1 >= 0:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j - 1]]
					# Add the lower center
					self.nodes[i][j].neighbors += [self.nodes[i + 1][j]]
					# Add the lower right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j + 1]]

	def getNodeFromPoint(self, point):
		""" Get the node in the graph that corresponds to a point in the world """
		return self.nodes[int(point.y/Constants.GRID_SIZE)][int(point.x/Constants.GRID_SIZE)]

	def placeObstacle(self, point, color):
		""" Place an obstacle on the graph """
		node = self.getNodeFromPoint(point)

		# If the node is not already an obstacle, make it one
		if node.isWalkable:
			# Indicate that this node cannot be traversed
			node.isWalkable = False		

			# Set a specific color for this obstacle
			node.color = color
			for neighbor in node.neighbors:
				neighbor.neighbors.remove(node)
			node.neighbors = []
			self.obstacles += [node]

	def reset(self):
		""" Reset all the nodes for another search """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].reset()

	def buildPath(self, endNode):
		""" Go backwards through the graph reconstructing the path """
		path = []
		node = endNode
		while node is not 0:
			node.isPath = True
			path = [node] + path
			node = node.backNode

		# If there are nodes in the path, reset the colors of start/end
		if len(path) > 0:
			path[0].isPath = False
			path[0].isStart = True
			path[-1].isPath = False
			path[-1].isEnd = True
		return path

	def findPath_Breadth(self, start, end):
		""" Breadth Search """
		print("BREADTH")
		self.reset()

		# TODO: Implement Breadth-first Search
		# Create start and end nodes
		startNode = self.getNodeFromPoint(start)
		endNode = self.getNodeFromPoint(end)
		
		# create a queue 
		queue = [startNode]
		startNode.isVisited = True
		while len(queue) > 0:
			# Get the current node
			currentNode = queue.pop(0)
			currentNode.isExplored = True
			
			#check if current node is the end node
			if(currentNode is endNode):
				return self.buildPath(currentNode)
				
			# If we're not at the end add the neighbors of the current node
			for neighbor in currentNode.neighbors:
				if(neighbor.isWalkable and neighbor.isVisited == False):
					queue.append(neighbor)
					neighbor.backNode = currentNode
					neighbor.isVisited = True

		# Return empty path indicating no path was found
		return []

	def findPath_Djikstra(self, start, end):
		""" Djikstra's Search """
		print("DJIKSTRA")
		self.reset()

		# TODO: Implement Djikstra's Search
		startNode = self.getNodeFromPoint(start)
		endNode = self.getNodeFromPoint(end)
		queue = [startNode]
		startNode.isVisited = True
		startNode.cost = 0
		while len(queue) > 0:
			#Sort the queue
			queue.sort(key=lambda node : node.cost)
			currentNode = queue.pop(0)
			currentNode.isExplored = True
			
			#check if end node
			if(currentNode is endNode):
				return self.buildPath(currentNode)

			#add the neighbors of the currentNode
			for neighbor in currentNode.neighbors:
				if(neighbor.isWalkable):
					cost = self.setWeight(currentNode, neighbor)		
					if(cost < neighbor.cost):
						neighbor.cost = cost
						neighbor.backNode = currentNode
					if not neighbor.isVisited:
						queue.append(neighbor)
						neighbor.isVisited = True

		# Return empty path indicating no path was found
		return []
	
	def setWeight(self, startNode, endNode):
		#Check if the movement is diagonal
		if(startNode.x != endNode.x and startNode.y != endNode.y):
			#If not diagonal then set cost to 1
			return startNode.cost + 1
		else:
			#The movement is diagonal if we made it to this point so set distance to be root 2 or 1.41
			return startNode.cost + 0.75
			

	def findPath_AStar(self, start, end):
		""" A Star Search """
		print("A_STAR")
		self.reset()

		

			
		# TODO: Implement A Star Search
		
		# Return empty path indicating no path was found
		return []

	def costToEnd(self, current, end):
		currVec = Vector(current.x, current.y)
		endVec = Vector(end.x, end.y)
		distVec = endVec - currVec
		return distVec.length()

	def findPath_BestFirst(self, start, end):
		""" Best First Search """
		print("BEST_FIRST")
		self.reset()
		

		startNode = self.getNodeFromPoint(start)
		endNode = self.getNodeFromPoint(end)
		queue = [startNode]
		startNode.isVisited = True
		while len(queue) > 0:
			queue.sort(key=lambda node : node.costToEnd)
			currentNode = queue.pop(0)
			currentNode.isExplored = True
			currentNode.costToEnd = self.costToEnd(currentNode,endNode)
			
			if(currentNode is endNode):
				return self.buildPath(currentNode)
			
			for neighbor in currentNode.neighbors:
				if(neighbor.isWalkable):
					cost = self.costToEnd(neighbor, endNode)
					if(cost < neighbor.costToEnd):
						neighbor.costToEnd = cost
						neighbor.backNode = currentNode
					if not neighbor.isVisited:
						queue.append(neighbor)
						neighbor.isVisited = True

		# TODO: Implement Best First Search
		
		# Return empty path indicating no path was found
		return []

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)