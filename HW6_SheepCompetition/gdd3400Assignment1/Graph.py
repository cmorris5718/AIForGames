import Constants
import Node
import pygame
import Vector

from pygame import *
from Vector import *
from Node import *
from enum import Enum

class SearchType(Enum):
	BREADTH = 0
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
		point.x = max(0, min(point.x, Constants.WORLD_WIDTH - 1))
		point.y = max(0, min(point.y, Constants.WORLD_HEIGHT - 1))

		# Return the node that corresponds to this point
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
		# Create the queue
		queue = [startNode]
		#Set is visited and cost 
		startNode.isVisited = True
		startNode.costFromStart = 0
		while len(queue) > 0:
			#Sort the queue
			queue.sort(key=lambda node : node.costFromStart)
			#Get the next node from the queue
			currentNode = queue.pop(0)
			#Set explored to true
			currentNode.isExplored = True
			
			#check if end node
			if(currentNode is endNode):
				return self.buildPath(currentNode)

			#add the neighbors of the currentNode
			for neighbor in currentNode.neighbors:
				# Check if neighbor is a valid node
				if(neighbor.isWalkable):
					#Set the weight
					cost = self.setWeight(currentNode, neighbor)		
					if(cost < neighbor.costFromStart):
						#If new weight is less than previous weight assign new node
						neighbor.costFromStart = cost
						neighbor.backNode = currentNode
					#If the neighbor isn't in the queue add it to the queue
					if not neighbor.isVisited:
						queue.append(neighbor)
						neighbor.isVisited = True
						neighbor.backNode = currentNode

		# Return empty path indicating no path was found
		return []

	# Returns cost for nodes based on if it's NSEW movement or diagonal movement
	def setWeight(self, startNode, endNode):
		#Check if the movement is diagonal
		if(startNode.x == endNode.x or startNode.y == endNode.y):
			return startNode.costFromStart + 1
		else:
			#The movement is diagonal if we made it to this point so set distance to be root 2 or 1.41
			return startNode.costFromStart + 1.41

	def findPath_AStar(self, start, end):
		""" A Star Search """
		print("A_STAR")
		self.reset()

		#Create the start and end nodes 
		startNode = self.getNodeFromPoint(start)
		endNode = self.getNodeFromPoint(end)
		# Create the queue
		queue = [startNode]
		#Set initial cost
		startNode.isVisited = True
		startNode.costFromStart = 0
		while len(queue) > 0:
			#Sort the queue
			queue.sort(key=lambda node : node.cost)

			#Get the next item in the queue
			currentNode = queue.pop(0)
			currentNode.isExplored = True
			#Set cost to end based on theoretical cost
			currentNode.costToEnd = self.costToEnd(currentNode, endNode)
			
			#Check if we're the end node 
			if(currentNode is endNode):
				return self.buildPath(currentNode)
			
			# Check neighbors
			for neighbor in currentNode.neighbors:
				#Check if neighbor is a valid node
				if(neighbor.isWalkable):
					# Calculate the start and end costs
					startCos = self.setWeight(currentNode, neighbor)
					endCos = self.costToEnd(neighbor, endNode)
					#Create the totale cost
					totalCos = startCos + endCos
					#IF total cost is less then the current cost to get to the node set new cost aned backpointer
					if(totalCos < neighbor.cost):
						neighbor.costFromStart = startCos
						neighbor.costToEnd = endCos
						neighbor.cost = totalCos;
						if(currentNode is not startNode):
							neighbor.backNode = currentNode
					#If not in the queue add to the queue
					if not neighbor.isVisited:
						queue.append(neighbor)
						neighbor.isVisited = True

	# Calculates and returns a theoretical cost to the end assumes that all distances are 1 to underestimate
	def costToEnd(self, current, end):
		currVec = Vector(current.x, current.y)
		endVec = Vector(end.x, end.y)
		distVec = endVec - currVec
		return distVec.length()

	def findPath_BestFirst(self, start, end):
		""" Best First Search """
		print("BEST_FIRST")
		self.reset()
		
		# create start and end nodes
		startNode = self.getNodeFromPoint(start)
		endNode = self.getNodeFromPoint(end)
		#create the queue
		queue = [startNode]
		startNode.isVisited = True
		while len(queue) > 0:
			#Sort the queue
			queue.sort(key=lambda node : node.costToEnd)
			#check the next node in the queue
			currentNode = queue.pop(0)
			currentNode.isExplored = True
			currentNode.costToEnd = self.costToEnd(currentNode,endNode)
			
			#check if at the end
			if(currentNode is endNode):
				return self.buildPath(currentNode)
			
			#check neighbors for a lower cost and set backnode
			for neighbor in currentNode.neighbors:
				if(neighbor.isWalkable):
					cost = self.costToEnd(neighbor, endNode)
					if(cost < neighbor.costToEnd):
						neighbor.costToEnd = cost
						neighbor.backNode = currentNode
					#If neighbor not in queue add to the queue
					if not neighbor.isVisited:
						queue.append(neighbor)
						neighbor.isVisited = True
						neighbor.backNode = currentNode

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)