import os
import sys
import pygame


class Construct:

	def __init__(self, colour):
		self.colour = colour

	def getCollisionType(self):
		return True
		#TODO: Add other collision types, like 50% chance of noticing for pit traps. 