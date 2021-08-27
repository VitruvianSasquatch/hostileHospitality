import os
import sys
import pygame


class World:	


	def __init__(self, size):
		self.width, self.height = size
		self.constructGrid =  [[None for j in range(0, self.height)] for i in range(0, self.width)]


	def draw(self, window, tileSize, viewWindowOffset):
		background = pygame.Surface(window.get_size()).convert()
		background.fill((0, 128, 0)) # Placeholder green background, likely remove when tiling is written


		x, y = viewWindowOffset
		for i in range(0, self.width):
			for j in range(0, self.height):
				rect = pygame.Rect(x+tileSize*i, y+tileSize*j, x+(tilesize+1)*i, y+(tileSize+1)*j)
				pygame.draw.rect(background, self.constructGrid[i][j].colour, rect)
		
		window.blit(background, (0, 0))
		



	# Places construct, returns whatever is overwritten
	def placeObject(self, construct, position):
		x, y = position
		oldConstruct = constructGrid[x][y]
		constructGrid[x][y] = construct
		return oldConstruct
