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


class Fence(Construct):

	def __init__(self):
		Construct.__init__(self, CONSTRUCT_COLOURS[Fence])


class PitTrap(Construct):

	def __init__(self):
		Construct.__init__(self, CONSTRUCT_COLOURS[PitTrap])


CONSTRUCT_COLOURS = {Fence: (128, 64, 16), 
					 PitTrap: (255, 0, 0)}