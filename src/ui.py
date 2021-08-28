import os
import sys
import pygame

BUILDMENU_DIMENSIONS = (500,120)
BUTTON_COLOURS = [
	(0,0,0),
	(128, 64, 16),
	(255,0,0)
]

class BuildMenu:

	def __init__(self, position):
		self.position = position
		self.uiSurface = pygame.Surface((0,0))
		self.selection = None
		self.isFocused = False

		self.buttonRects = []
		self.updateSurface(BUILDMENU_DIMENSIONS)

	def getSelection(self):
		'''
		Gets current selection 
		returns None if nothing selected
		'''
		return self.selection

	def updateSurface(self, dimensions):
		newSurface = pygame.Surface(dimensions)
		newSurface.fill((20,20,20))

		self.buttonRects = [
			pygame.Rect(10, 10, 100, 100),
			pygame.Rect(120, 10, 100, 100),
			pygame.Rect(230, 10, 100, 100)
		]

		# Draw buttons
		pygame.draw.rect(newSurface, BUTTON_COLOURS[0], self.buttonRects[0])
		pygame.draw.rect(newSurface, BUTTON_COLOURS[1], self.buttonRects[1])
		pygame.draw.rect(newSurface, BUTTON_COLOURS[2], self.buttonRects[2])

		# Draw preview (-1 for unselected)
		if self.selection is None:
			pygame.draw.rect(newSurface, (40, 40, 40), (400, 10, 50, 50))
		else:
			pygame.draw.rect(newSurface, BUTTON_COLOURS[self.selection], (400, 10, 50, 50))

		self.uiSurface = newSurface

	def draw(self, window):
		window.blit(self.uiSurface, self.position)

	def getFocused(self):
		return self.isFocused

	def handleMouseMotion(self, point):
		self.isFocused = pygame.Rect(self.position, self.uiSurface.get_size()).collidepoint(point)

	def handleMouseDown(self, point):
		if self.isFocused:
			self.selection = None
			for i,collider in enumerate(self.buttonRects):
				if collider.move(self.position).collidepoint(point):
					self.selection = i
			self.updateSurface(BUILDMENU_DIMENSIONS)
			return True
		else:
			return False
	

