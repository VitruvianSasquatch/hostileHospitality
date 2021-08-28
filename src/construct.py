import os
import sys
import pygame



class Construct:

	def __init__(self, colour, id=None):
		self.colour = colour
		self.id = id

	def getCollisionType(self):
		return True
		#TODO: Add other collision types, like 50% chance of noticing for pit traps. 


class Aoe(Construct):

	def __init__(self, colour, position, effectRange):
		Construct.__init__(self, colour)
		self.position = position
		self.effectRange = effectRange

	def isInRange(self, testPosition):
		dx = self.position[0] - testPosition[0]
		dy = self.position[1] - testPosition[1]
		return self.effectRange**2 >= dx**2 + dy**2





class Fence(Construct):

	def __init__(self):
		Construct.__init__(self, CONSTRUCT_COLOURS[Fence])


class PitTrap(Construct):

	def __init__(self):
		Construct.__init__(self, CONSTRUCT_COLOURS[PitTrap])


class TownCentre(Aoe):
	def __init__(self, position):
		Aoe.__init__(CONSRUCT_COLOUR[TownCentre], position, 7)
	

class DungHeap(Aoe):
	def __init__(self, position):
		Aoe.__init__(CONSRUCT_COLOUR[DungHeap], position, 2)




CONSTRUCT_COLOURS = {
	Fence: (128, 64, 16), 
	PitTrap: (255, 0, 0),
	TownCentre: (255, 180, 0), 
	DungHeap: (70, 80, 0)
}

CONSTRUCT_FROMID = {
	1 : Fence(),
	2 : PitTrap()
}