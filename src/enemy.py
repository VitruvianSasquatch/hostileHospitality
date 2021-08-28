import os
import sys
import pygame

import math
import random

from world import *
import pathing

TEAM_COLOURS = {"RED": (255, 0, 0), "BLUE": (0, 0, 255)}

BOUNCE_FREQ = 3
BOUNCE_AMP = 0.2 #Tiles

class Enemy:

	def __init__(self, team, position):
		self.team = team
		self.position = position
		self.colour = TEAM_COLOURS[self.team]
		self.health = 1
		self.damage = 1
		self.moveQueue = []
		self.moveSpeed = 1 #full moves per second
		self.destination = self.position

		self.timeElapsedThisMove = 0
		self.drawPosition = self.position
		self.animPhase = random.uniform(0, 1/BOUNCE_FREQ)


	#Returns whether it should be deleted
	def takeDamage(self, damage):
		self.health -= damage
		return health <= 0


	def isBetweenPositions(self):
		return self.position != self.destination


	def moveToDistant(self, destination, world):
		#self.moveQueue = pathing.walk_direct(self.position, destination)[1:] #Remove first entry, which is current location
		self.moveQueue = pathing.bfs_path(self.position, destination, world)[1:] #Remove first entry, which is current location
		if self.moveQueue != []:
			self.moveToAdjacent(self.moveQueue[0])


	def moveToAdjacent(self, destination):
		if abs(self.position[0] - destination[0]) <= 1 and abs(self.position[1] - destination[1]) <= 1: #Is adjacent?
			self.timeElapsedThisMove = 0
			self.destination = destination


	def update(self, dt, world):
		if self.moveQueue == []:
			self.drawPosition = self.position #Ensure no float error and do nothing
		elif self.isBetweenPositions():

			self.timeElapsedThisMove += dt
			fractionMoved = self.timeElapsedThisMove*self.moveSpeed
			if fractionMoved >= 1: #Finished movement
				self.position = self.destination
				self.drawPosition = self.position
				self.moveQueue = self.moveQueue[1:] #remove first element, as now done
			else:
				drawX = self.position[0] + (self.destination[0] - self.position[0]) * fractionMoved
				drawY = self.position[1] + (self.destination[1] - self.position[1]) * fractionMoved
				self.drawPosition = (drawX, drawY)
		
		else: #finished current move, but there are still some in queue
			self.moveToAdjacent(self.moveQueue[0])


	def draw(self, surface, tileSize):
		drawX, drawY = self.drawPosition
		drawY -= BOUNCE_AMP*abs(math.sin(math.pi*BOUNCE_FREQ*(self.timeElapsedThisMove + self.animPhase))) #Add bounce - pi rather than 2pi because of abs
		topLeft = drawX*tileSize, drawY*tileSize
		topRight = (drawX+1)*tileSize, drawY*tileSize
		bottom = drawX*tileSize + tileSize//2, (drawY+1)*tileSize
		pygame.draw.polygon(surface, self.colour, (topLeft, topRight, bottom))




#TODO: Flesh out if even worth it. 
class EliteEnemy(Enemy):
	def __init__(self, team, position):
		super(self).__init(self, team, position)
		self.health = 3
		self.damage = 2
