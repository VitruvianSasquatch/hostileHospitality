import os
import sys
import pygame

from construct import *

class World: 


	def __init__(self, size):
		self.width, self.height = size
		self.constructGrid =  [[None for j in range(0, self.height)] for i in range(0, self.width)]


	def draw(self, window, tileSize):
		surface = pygame.Surface((tileSize*self.width, tileSize*self.height))
		drawBackground(surface, (0, 128,0))

		for i in range(0, self.width):
			for j in range(0, self.height):
				if self.constructGrid[i][j]:
					rect = pygame.Rect(tileSize*i, tileSize*j, tileSize, tileSize)
					pygame.draw.rect(surface, self.constructGrid[i][j].colour, rect)
		
		return surface
		



	# Places construct, returns whatever is overwritten
	def placeConstruct(self, construct, position):
		x, y = position
		if (x < self.width and y < self.height):
			oldConstruct = self.constructGrid[x][y]
			self.constructGrid[x][y] = construct
			return oldConstruct
		return None


	def getCollisionGrid(self):
		return [[(False if self.constructGrid[i][j] is None else self.constructGrid[i][j].getCollisionType()) for j in range(0, self.height)] for i in range(0, self.width)]

	def isCollision(self, position):
		if self.constructGrid[i][j] is not None:
			return self.constructGrid[i][j].getCollisionType()
		else:
			return False


	def getCoordinate(self, queryPosition, tileSize, viewOffset):
		x = (queryPosition[0] - viewOffset[0]) // tileSize
		y = (queryPosition[1] - viewOffset[1]) // tileSize
		return (int(x),int(y))


def drawBackground(surface, colour):
	background = surface.copy()
	background.fill(colour)
	surface.blit(background, (0, 0))