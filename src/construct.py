import os
import sys
import pygame



class Construct:

	def __init__(self, colour):
		self.colour = colour
		self.collisionWeight = 1
	
	def getColour(self):
		return self.colour

	def isCollision(self):
		return True

	def getCollisionWeight(self):
		return self.collisionWeight
		#TODO: Add other collision types, like 50% chance of noticing for pit traps. 
		#return name of item hit


class Aoe(Construct):

	def __init__(self, colour, position, effectRange):
		Construct.__init__(self, colour)
		self.position = position
		self.effectRange = effectRange

	def isInRange(self, testPosition):
		dx = self.position[0] - testPosition[0]
		dy = self.position[1] - testPosition[1]
		return self.effectRange**2 >= dx**2 + dy**2

	def getCentre(self):
		return self.position

class Fence(Construct):

	def __init__(self):
		Construct.__init__(self, CONSTRUCT_COLOURS[Fence])

	def __str__(self):
		return "fence"

class PitTrap(Construct):

	def __init__(self):
		Construct.__init__(self, CONSTRUCT_COLOURS[PitTrap])
		self.isFull = False
		self.collisionWeight = 0

	def isCollision(self):
		return False

	def getColour(self):
		if self.isFull:
			return (255, 0, 0)
		else:
			return self.colour

	def __str__():
		return "pit_trap"

	def stepOn(self, enemy):
		if not self.isFull:
			self.isFull = True
			return enemy
		else:
			return None


class TownCentre(Aoe):
	def __init__(self, position):
		Aoe.__init__(self, CONSTRUCT_COLOURS[TownCentre], position, 1)
		self.citizenPatience = 50 #TODO: tune value
		self.damageFlash = 0

	def isCollision(self):
		return False

	def setRangeFromDifficulty(self, difficulty):
		self.effectRange = 1+ difficulty/2

	def invade(self, enemy):
		#Ignore enemy type for now
		self.citizenPatience -= 1
		self.damageFlash = 10
	
	def isAbandoned(self):
		return self.citizenPatience <= 0

class DungHeap(Aoe): 
	def __init__(self, position):
		Aoe.__init__(self, CONSTRUCT_COLOURS[DungHeap], position, 2)

	def __str__(self):
		return "dung"





CONSTRUCT_COLOURS = {
	Fence: (128, 64, 16), 
	PitTrap: (0, 75, 0),
	TownCentre: (255, 180, 0), 
	DungHeap: (70, 80, 0)
}
CONSTRUCT_FROMID = {
	1 : Fence,
	2 : PitTrap,
	3 : DungHeap,
}
CONSTRUCT_NAME = {
	1 : "Fence",
	2 : "Pit Trap",
	3 : "Dung Heap"
}
CONSTRUCT_COST = {
	1 : 1,
	2 : 1,
	3 : 3
}