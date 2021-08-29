import os
import sys
import pygame

import math
import random

from world import *
from construct import *

import pathing

TEAM_COLOURS = {"RED": (255, 0, 0), "BLUE": (0, 0, 255)}

BOUNCE_FREQ = 3
BOUNCE_AMP = 0.2 #Tiles

class Enemy:

	def __init__(self, team, spawnY, world):
		blueBaseCol = world.width-1
		redBaseCol = 0

		self.team = team
		if self.team == "RED":
			self.position = (redBaseCol, spawnY)
		elif self.team == "BLUE":
			self.position = (blueBaseCol, spawnY)

		self.colour = TEAM_COLOURS[self.team]
		self.health = 1
		self.damage = 1
		self.moveQueue = []
		self.moveSpeed = 1 #full moves per second
		self.destination = self.position

		self.timeElapsedThisMove = 0
		self.drawPosition = self.position
		self.animPhase = random.uniform(0, 1/BOUNCE_FREQ)

		if self.team == "RED":
			self.finalDestination = (blueBaseCol, world.height//2)
		elif self.team == "BLUE":
			self.finalDestination =(redBaseCol, world.height//2)

		self.moveToDistant(self.finalDestination, world)
		#self.moveToEdge(self.finalDestination[1], world)

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


	def moveToEdge(self, destColumn, world):
		self.moveQueue = pathing.bfs_path_to_side(self.position, destColumn, world)[1:]
		if self.moveQueue != []:
			self.moveToAdjacent(self.moveQueue[0])


	def moveToAdjacent(self, destination):
		if abs(self.position[0] - destination[0]) <= 1 and abs(self.position[1] - destination[1]) <= 1: #Is adjacent?
			self.timeElapsedThisMove = 0
			self.destination = destination


	def isAtFinalDestination(self):
		return self.position == self.finalDestination


	def update(self, dt, world):
		if self.moveQueue == []:
			self.drawPosition = self.position #Ensure no float error and do nothing
			self.moveToDistant(self.finalDestination, world)
			#self.moveToEdge(self.finalDestination[1], world)
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
		
		else: #finished current move animation, but there are still some in queue
			for dungHeap in world.getConstructType(DungHeap):
				if dungHeap.isInRange(self.position):
					x, y = -1, -1
					while world.isCollision((x, y)): #Make sure a path is findable - out of bounds will collide
						x, y = dungHeap.getCentre()
						angle = random.uniform(0, 2*math.pi)
						x += int(2*dungHeap.effectRange*math.cos(angle))
						y += int(2*dungHeap.effectRange*math.sin(angle))
						x = max(0, x); x = min(world.width-1, x);
						y = max(0, y); y = min(world.height-1, y);
					self.moveToDistant((x, y), world) #TODO: TEST ME!

			for townCentre in world.getConstructType(TownCentre):
				if townCentre.isInRange(self.position):
					townCentre.invade(self)

			self.moveToAdjacent(self.moveQueue[0])


	def draw(self, surface, tileSize):
		drawX, drawY = self.drawPosition
		drawY -= BOUNCE_AMP*abs(math.sin(math.pi*BOUNCE_FREQ*(self.timeElapsedThisMove + self.animPhase))) #Add bounce - pi rather than 2pi because of abs
		
		topLeft = drawX*tileSize, drawY*tileSize
		topRight = (drawX+1)*tileSize, drawY*tileSize
		bottom = drawX*tileSize + tileSize//2, (drawY+1)*tileSize
		pygame.draw.polygon(surface, self.colour, (topLeft, topRight, bottom))

		r = min(255, self.colour[0]+64)
		g = min(255, self.colour[1]+64)
		b = min(255, self.colour[2]+64)
		topLeft = topLeft[0]+tileSize/4.5, topLeft[1]+tileSize//6
		topRight = topRight[0]-tileSize/4.5, topRight[1]+tileSize//6
		bottom = bottom[0], bottom[1]-tileSize/3.5
		pygame.draw.polygon(surface, (r, g, b), (topLeft, topRight, bottom))




#TODO: Flesh out if even worth it. 
class EliteEnemy(Enemy):
	def __init__(self, team, position):
		super(self).__init(self, team, position)
		self.health = 3
		self.damage = 2
