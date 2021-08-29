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

	def __init__(self, team, position, world, pathArray):
		self.position = position
		self.team = team

		self.colour = TEAM_COLOURS[self.team]
		self.health = 1
		self.damage = 1
		self.moveSpeed = 1 #full moves per second
		self.destination = self.position
		self.prevPosition = None
		self.pathArray = pathArray

		self.timeElapsedThisMove = 0
		self.drawPosition = self.position
		self.animPhase = random.uniform(0, 1/BOUNCE_FREQ)

		self.destination = pathing.nextPosition(self.position, self.pathArray, world)
		if self.team == "RED":
			self.finalDestination = world.blueBase
		elif self.team == "BLUE":
			self.finalDestination = world.redBase

		#self.moveToDistant(self.finalDestination, world)
		#self.moveToEdge(self.finalDestination[1], world)

	#Returns whether it should be deleted
	def testCombat(self, enemies):
		for enemy in enemies:
			if enemy.team != self.team:
				if self.position == enemy.position or self.destination == enemy.position:
					return enemy
		return None

	def isBetweenPositions(self):
		return self.position != self.destination

	def isAtFinalDestination(self):
		return self.position == self.finalDestination

	def update(self, dt, world):

		if self.isBetweenPositions():

			self.timeElapsedThisMove += dt
			fractionMoved = self.timeElapsedThisMove*self.moveSpeed
			if fractionMoved >= 1: #Finished movement
				self.position = self.destination
				self.drawPosition = self.position
			else:
				drawX = self.position[0] + (self.destination[0] - self.position[0]) * fractionMoved
				drawY = self.position[1] + (self.destination[1] - self.position[1]) * fractionMoved
				self.drawPosition = (drawX, drawY)
		
		else: #finished current move animation, but there are still some in queue
			self.timeElapsedThisMove = 0
			self.prevPosition = self.destination
			self.destination = pathing.nextPosition(self.position, self.pathArray, world)

			for trapPosition in world.getConstructTypeLocs(PitTrap):
				if self.position == trapPosition:
					victim = world.constructGrid[trapPosition[0]][trapPosition[1]].stepOn(self)
					if victim is not None:
						return True
						

			if self.destination == self.prevPosition:
				if self.pathArray[self.position[0]][self.position[1]] is not None:
					self.pathArray[self.position[0]][self.position[1]] += 1


			for townCentre in world.getConstructType(TownCentre):
				if townCentre.isInRange(self.position):
					townCentre.invade(self)
		
		return False #Did not die



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
