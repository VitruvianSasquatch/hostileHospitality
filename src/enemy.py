import os
import sys
import pygame

from world import *
#from pathing import *

TEAM_COLOURS = {"RED": (255, 0, 0), "BLUE": (0, 0, 255)}


class Enemy:

	def __init__(self, team, position):
		self.team = team
		self.position = position
		self.colour = TEAM_COLOURS[self.team]
		self.health = 1
		self.damage = 1
		self.moveSpeed = 1 #full moves per second
		self.timeSpentMoving = 0
		self.destination = self.position


	#Returns whether it should be deleted
	def takeDamage(self, damage):
		self.health -= damage
		return health <= 0


	def isMoving(self)
		return self.position == self.destination

	def move(self, destination):
		self.destination = destination


	def draw(self, surface, tileSize, dt):
		self.timeSpentMoving += dt
		fractionMoved = self.timeSpentMoving*self.moveSpeed
		if fractionMoved >= 1: #Finished movement
			self.position = self.destination
			drawX, drawY = self.position[0], self.position[1]
		else:
			print("Animating")
			drawX = self.position[0] + (self.destination[0] - self.position[0]) * fractionMoved
			drawY = self.position[1] + (self.destination[1] - self.position[1]) * fractionMoved
		
		topLeft = drawX*tileSize, drawY*tileSize
		topRight = (drawX+1)*tileSize, drawY*tileSize
		bottom = drawX*tileSize + tileSize//2, (drawY+1)*tileSize
		pygame.draw.polygon(surface, self.colour, (topLeft, topRight, bottom))





class EliteEnemy(Enemy):
	def __init__(self, team, position):
		super(self).__init(self, team, position)
		self.health = 3
		self.damage = 2
