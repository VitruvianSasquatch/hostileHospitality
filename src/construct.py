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

	def __str__():
		return "pit_trap"


class TownCentre(Aoe):
	def __init__(self, position):
		Aoe.__init__(self, CONSTRUCT_COLOURS[TownCentre], position, 0)
		self.citizenPatience = 50 #TODO: tune value

	def isCollision(self):
		return False

	def setRangeFromDifficulty(self, difficulty):
		self.effectRange = difficulty/2

	def invade(self, enemy):
		#Ignore enemy type for now
		self.citizenPatience -= 1
	
	def isAbandoned(self):
		return self.citizenPatience <= 0

class DungHeap(Aoe): 
	def __init__(self, position):
		Aoe.__init__(self, CONSTRUCT_COLOURS[DungHeap], position, 2)

	def __str__(self):
		return "dung"





CONSTRUCT_COLOURS = {
	Fence: (128, 64, 16), 
	PitTrap: (255, 0, 0),
	TownCentre: (255, 180, 0), 
	DungHeap: (70, 80, 0)
}

CONSTRUCT_FROMID = {
	1 : Fence,
	2 : PitTrap,
	3 : DungHeap,
}