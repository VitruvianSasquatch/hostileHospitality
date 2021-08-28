import os
import sys
import pygame

from construct import *
from ui import *
from world import *
from enemy import *

WINDOW_DIMENSIONS = (1280, 960)
TILESIZE = 64


class GameManager:
	def __init__(self):
		self.isRunning = True

		self.isPaused = False
		self.isEditing = True



def main():
	pygame.init()
	window = pygame.display.set_mode(WINDOW_DIMENSIONS)
	pygame.display.set_caption("Hostile Hospitality")
	clock = pygame.time.Clock()


	initInput()

	#Setup UI
	buildMenu = BuildMenu((790, 840))

	# Ensure map all fits on one screen
	mapWidth, mapHeight = WINDOW_DIMENSIONS
	mapWidth //= TILESIZE
	mapHeight //= TILESIZE
	world = World((mapWidth, mapHeight))

	placeDefaultMap(world)

	enemies = [Enemy("RED", (0, i)) for i in range(4, 9)]
	enemies.extend([Enemy("BLUE", (mapWidth-1, i)) for i in range(4, 9)])

	for enemy in enemies:
		enemy.moveToDistant((6, 8), world)



	gameManager = GameManager() #Simplifies input passing
	
	while gameManager.isRunning:
		dt = clock.tick(60) / 1000

		# Handle inputs
		
		handleInputs(gameManager, world, buildMenu)

		world.draw(window, TILESIZE)

		if gameManager.isPaused:
			width, height = WINDOW_DIMENSIONS
			thickness = width // 10
			pygame.draw.rect(window, (200, 200, 200), (width//3, height//6, thickness, 2*height//3))
			pygame.draw.rect(window, (200, 200, 200), (2*width//3, height//6, thickness, 2*height//3))
			pass

		else:

			if gameManager.isEditing:
				gridCursorPosition = world.getCoordinate(pygame.mouse.get_pos(), TILESIZE)
				if not buildMenu.getFocused(): 
					#Draw cursor highlight
					x = gridCursorPosition[0] * TILESIZE
					y = gridCursorPosition[1] * TILESIZE
					pygame.draw.rect(window, (200, 200, 200), (x, y, TILESIZE, TILESIZE), 5)

				buildMenu.draw(window)

			else:
				for enemy in enemies:
					enemy.update(dt)
					enemy.draw(window, TILESIZE)


		pygame.display.flip()

	pygame.quit()
	# implicit exit()



def placeDefaultMap(world):
	world.placeConstruct(Fence(), (5, 4))
	world.placeConstruct(Fence(), (6, 5))
	world.placeConstruct(Fence(), (6, 6))
	world.placeConstruct(Fence(), (6, 7))
	world.placeConstruct(Fence(), (7, 8))



def initInput():
	pygame.mouse.set_visible(True)
	
	#TODO: Decide on and implement keyboard input options



def handleInputs(gameManager, world, buildMenu):

	for event in pygame.event.get():

		if (event.type == pygame.QUIT):
			gameManager.isRunning = False

		elif event.type == pygame.MOUSEMOTION:
			buildMenu.handleMouseMotion(event.pos)

		elif (event.type == pygame.MOUSEBUTTONDOWN):
			if buildMenu.handleMouseDown(event.pos): # buildMenu.mouseEvent passes if it handled event
				continue
			if buildMenu.getSelection() in CONSTRUCT_FROMID:
				newConstruct = CONSTRUCT_FROMID[buildMenu.getSelection()]
				world.placeConstruct(newConstruct, world.getCoordinate(pygame.mouse.get_pos(), TILESIZE))

		elif (event.type == pygame.KEYDOWN):
			if (event.key == pygame.K_p):
				gameManager.isPaused = not gameManager.isPaused
			elif (event.key == pygame.K_SPACE):
				gameManager.isEditing = not gameManager.isEditing








main()