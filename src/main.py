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

		self.waveNumber = 0



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

	enemies = []


	gameManager = GameManager() #Simplifies input passing
	
	while gameManager.isRunning:
		dt = clock.tick(60) / 1000

		# Handle inputs
		
		handleInputs(gameManager, world, enemies, buildMenu)

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
					enemy.update(dt, world)
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

	world.placeConstruct(DungHeap((3, 7)), (3, 7))
	world.placeConstruct(DungHeap((10, 7)), (10, 7))


def initInput():
	pygame.mouse.set_visible(True)
	
	#TODO: Decide on and implement keyboard input options



def handleInputs(gameManager, world, enemies, buildMenu):

	for event in pygame.event.get():

		if (event.type == pygame.QUIT):
			gameManager.isRunning = False

		elif event.type == pygame.MOUSEMOTION:
			buildMenu.handleMouseMotion(event.pos)

		elif (event.type == pygame.MOUSEBUTTONDOWN):
			if gameManager.isEditing:
				if buildMenu.handleMouseDown(event.pos): # buildMenu.mouseEvent passes if it handled event
					continue
				if buildMenu.getSelection() in CONSTRUCT_FROMID:
					coordinates = world.getCoordinate(pygame.mouse.get_pos(), TILESIZE)
					if buildMenu.getSelection() == 3: # If dungheap
						newConstruct = CONSTRUCT_FROMID[3](coordinates)
					else:
						newConstruct = CONSTRUCT_FROMID[buildMenu.getSelection()]()
					world.placeConstruct(newConstruct, coordinates)

		elif (event.type == pygame.KEYDOWN):
			if (event.key == pygame.K_p):
				gameManager.isPaused = not gameManager.isPaused
			elif (event.key == pygame.K_SPACE):
				gameManager.isEditing = not gameManager.isEditing 

				# Create list of AoE's from constructGrid
				#dungheapList = world.getConstructType(DungHeap) #                                                    <----------------------------------------------------------- dungheap
			
				if not gameManager.isEditing: #We are now at war!
					gameManager.waveNumber += 1
					
					while enemies != []:
						enemies.pop() #Inefficient, but otherwise doesn't overwrite reference

					numEnemies = 2+gameManager.waveNumber
					startY = world.height//2 - numEnemies//2
					for i in range(0, numEnemies):
						enemies.append(Enemy("RED", startY+i, world))
						enemies.append(Enemy("BLUE", startY+i, world))

					for enemy in enemies:
						enemy.moveToDistant(enemy.finalDestination, world)
				







main()