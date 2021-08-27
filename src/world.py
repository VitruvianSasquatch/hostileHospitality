import os
import sys
import pygame

from construct import *

class World:	


	def __init__(self, size):
		self.width, self.height = size
		self.constructGrid =  [[None for j in range(0, self.height)] for i in range(0, self.width)]


	def draw(self, window, tileSize, viewWindowOffset):
		background = pygame.Surface(window.get_size()).convert()
		solidGreen = window.copy()
		solidGreen.fill((0,128,0))
		background.blit(solidGreen, viewWindowOffset)
		#background.fill((0, 128, 0)) # Placeholder green background, likely remove when tiling is written


		x, y = viewWindowOffset
		for i in range(0, self.width):
			for j in range(0, self.height):
				if self.constructGrid[i][j]:
					rect = pygame.Rect(x+tileSize*i, y+tileSize*j, tileSize, tileSize)
					pygame.draw.rect(background, self.constructGrid[i][j].colour, rect)
		
		window.blit(background, (0, 0))
		



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

	def getCoordinate(self, position, tileSize, viewWindowOffset):
		x = (position[0] - viewWindowOffset[0]) // tileSize
		y = (position[1] - viewWindowOffset[1]) // tileSize
		return (int(x),int(y))