import os
import sys
import pygame

BUILDMENU_DIMENSIONS = (500,120)
PLAYERSTATS_DIMENSIONS = (150, 80)
BUTTON_COLOURS = [
	(70, 80, 0),
	(128, 64, 16),
	(0,75, 0)
]
BUTTON_MAPPING = {
	None : None,
	0 : 3, # Aoe
	1 : 1, # Fence
	2 : 2  # Wall
}
BUTTON_COSTS = {
	0 : 1,
	1 : 1,
	2 : 1
}

class BuildMenu:

	def __init__(self, position):
		self.position = position
		self.uiSurface = pygame.Surface((0,0))
		self.selection = None
		self.isFocused = False

		self.buttonRects = []
		self.updateSurface(BUILDMENU_DIMENSIONS)

		self.mainFont = pygame.font.SysFont('Arial', 24, bold = True)

	def getSelection(self):
		'''
		Gets current selection 
		returns None if nothing selected
		'''
		return BUTTON_MAPPING[self.selection]

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
			text = self.mainFont.render("Cost: "+str(BUTTON_COSTS[1]), True, (255,255,255), (20,20,20))
			textX, textY = self.mainFont.size("Cost: "+str(BUTTON_COSTS[1]))
			newSurface.blit(text, (425 - textX//2, 80 - textY//2))

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
	

class PlayerStats:

	def __init__(self, position, money, health):
		self.position = position
		self.uiSurface = pygame.Surface((0,0))
		self.isFocused = False

		self.mainFont = pygame.font.SysFont('Arial', 24, bold = True)

		self.update(money, health)

	def update(self, money=None, health=None):
		if money is not None:
			self.money = money
		if health is not None:
			self.health = health
		self.updateSurface()

	def updateSurface(self):
		money = self.money
		health = self.health
		newSurface = pygame.Surface(PLAYERSTATS_DIMENSIONS)
		newSurface.fill((40,40,40))

		#healthX, healthY = self.mainFont.size(Health: "+str(health))
		healthText = self.mainFont.render("Health: "+str(health), True, (255,255,255), (40,40,40))
		newSurface.blit(healthText, (20,10))

		#fundsX, fundsY = self.mainFont.size("Funds: "+str(money))
		fundsText = self.mainFont.render("Funds: "+str(money), True, (255,255,255), (40,40,40))
		newSurface.blit(fundsText, (20, 44))

		self.uiSurface = newSurface

	def draw(self, window):
		window.blit(self.uiSurface, self.position)

	def handleMouseMotion(self, point):
		self.isFocused = pygame.Rect(self.position, self.uiSurface.get_size()).collidepoint(point)


