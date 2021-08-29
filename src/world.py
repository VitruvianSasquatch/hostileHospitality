import os
import sys
import pygame

from construct import *

class World: 


	def __init__(self, size):
		self.width, self.height = size
		self.constructGrid =  [[None for j in range(0, self.height)] for i in range(0, self.width)]

		self.viewOffset = (0, 0) #Pixels


	def draw(self, window, tileSize):
		surface = pygame.Surface((tileSize*self.width, tileSize*self.height))
		drawBackground(surface, (0, 128,0))

		for i in range(0, self.width):
			for j in range(0, self.height):
				if self.constructGrid[i][j]:
					centre = (tileSize*i + tileSize//2, tileSize*j + tileSize//2)

					if type(self.constructGrid[i][j]) is Fence:
						pygame.draw.circle(surface, self.constructGrid[i][j].colour, centre, tileSize//3)
						for dx in range(-1, 2):
							for dy in range(-1, 2):
								if not (dx == 0 and dy == 0):
									if self.isInBounds((i+dx, j+dy)) and self.isCollision((i+dx, j+dy)):
										edge = (centre[0] + dx*tileSize//2, centre[1] + dy*tileSize//2)
										thickness = (tileSize//4 if dx*dy == 0 else tileSize//3)
										#thickness = tileSize//4
										pygame.draw.line(surface, self.constructGrid[i][j].getColour(), centre, edge, thickness)
					
					elif type(self.constructGrid[i][j] is TownCentre):
						tempSurface = pygame.Surface((tileSize*self.width, tileSize*self.height))
						tempSurface.set_colorkey((0, 0, 0))
						tempSurface.fill((0, 0, 0))
						tempSurface.set_alpha(70)
						pygame.draw.circle(tempSurface, self.constructGrid[i][j].colour, centre, (tileSize//2) + tileSize*self.constructGrid[i][j].effectRange)
						surface.blit(tempSurface, (0, 0))


					
					else:
						rect = pygame.Rect(tileSize*i, tileSize*j, tileSize, tileSize)
						pygame.draw.rect(surface, self.constructGrid[i][j].getColour(), rect)
			
		window.blit(surface, self.viewOffset)

	def getConstructType(self, classType):
		dungheaps = [[cell for cell in line if type(cell) is classType] for line in self.constructGrid]
		return sum(dungheaps, [])

	def isInBounds(self, position):
		x, y = position
		return (0 <= x < self.width and 0 <= y < self.height)


	# Places construct, returns whatever is overwritten
	def placeConstruct(self, construct, position):
		if self.isInBounds(position):
			x, y = position
			oldConstruct = self.constructGrid[x][y]
			self.constructGrid[x][y] = construct
			return oldConstruct
		return None


	def getCollisionGrid(self):
		return [[(False if self.constructGrid[i][j] is None else self.constructGrid[i][j].getCollisionType()) for j in range(0, self.height)] for i in range(0, self.width)]


	def isCollision(self, position):
		
		if self.isInBounds(position):
			x, y = position
			if self.constructGrid[x][y] is None:
				return False
			else:
				return self.constructGrid[x][y].isCollision()
		else:
			return True #Outside bounds, collides as keepout


	def getCollisionWeight(self, position):
		
		if self.isInBounds(position):
			x, y = position
			if self.constructGrid[x][y] is not None:
				return self.constructGrid[x][y].getCollisionWeight()
			else:
				return 0
		else:
			return float("inf") #Outside bounds, collides as keepout


	def getCoordinate(self, queryPosition, tileSize):
		x = (queryPosition[0] - self.viewOffset[0]) // tileSize
		y = (queryPosition[1] - self.viewOffset[1]) // tileSize
		return (int(x),int(y))


	def moveViewOffset(self, delta):
		x = self.viewOffset[0] + delta[0]
		y = self.viewOffset[1] + delta[1]
		self.viewOffset = (x, y)
		#TODO: saturate and return whether it banded. 


	def writeToFile(self, filename):
		with open(filename, 'w+') as file:
			file.write("{},{}\n".format(self.width, self.height))
			for y in range(self.height):
				newLine = ""
				for x in range(self.width):
					if self.constructGrid[x][y] is None:
						newLine += ' ,' 
						continue
					newLine += str(self.constructGrid[x][y].id) + ','
				file.write(newLine[:-1]+"\n")
		print("ConstructGrid written to {}".format(filename))

	def readfromFile(self, filename):
		with open(filename, 'r') as file:
			width, height = file.readline()[:-1].split(',')
			lines = file.readlines()
		print("Read {} new width/height ({},{})\n".format(filename, width, height))

		self.width, self.height = int(width), int(height)
		self.ConstructGrid = [[None for j in range(0, self.height)] for i in range(0, self.width)]

		for y,line in enumerate(lines):
			for x,value in enumerate(line.split(',')[:-1]): #Strip newline character off
				if value == ' ':
					continue
				if int(value) in CONSTRUCT_FROMID:
					if int(value) == 3: # AoE Special Case
						newConstruct = CONSTRUCT_FROMID[int(value)](x,y) 
					else:
						newConstruct = CONSTRUCT_FROMID[int(value)]()
					self.placeConstruct(newConstruct, (x,y))
					continue
				newConstruct =  Construct((100,100,100), int(value))
				self.placeConstruct(newConstruct, (x,y))
				




def drawBackground(surface, colour):
	background = surface.copy()
	background.fill(colour)
	surface.blit(background, (0, 0))