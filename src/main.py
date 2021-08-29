import os
import sys
import pygame

from construct import *
from pathing import calculatePathingArray
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

		self.timeScaling = 1

		self.waveNumber = 0
		self.isGameLost = False



def main():
	pygame.init()
	window = pygame.display.set_mode(WINDOW_DIMENSIONS)
	pygame.display.set_caption("Hostile Hospitality")
	clock = pygame.time.Clock()


	mainFont = pygame.font.SysFont('Arial', 24, bold = True)
	bigFont = pygame.font.SysFont('Arial', 200, bold = True)

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

	townCentre = world.getConstructType(TownCentre)[0] #For efficiency

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

		elif gameManager.isGameLost:
			width, height = WINDOW_DIMENSIONS

			xyTextSurface = bigFont.render("Defeat :'(", True, (128, 0, 0))
			window.blit(xyTextSurface, ((width-xyTextSurface.get_width())//2, (height-xyTextSurface.get_height())//2))
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

			else: #At war!
				if gameManager.timeScaling != 1:
					dt *= gameManager.timeScaling
					#Draw something?

				if townCentre.isAbandoned():
					gameManager.isGameLost = True

				for enemy in enemies:

					enemy.update(dt, world)
					enemy.draw(window, TILESIZE)
					if enemy.isAtFinalDestination():
						enemies.remove(enemy)
				
				if enemies == []: #All either dead or off-screen
					gameManager.isEditing = True
					townCentres = world.getConstructType(TownCentre)
					for townCentre in townCentres:
						townCentre.setRangeFromDifficulty(gameManager.waveNumber) #Increase for next round
				
		


		pygame.display.flip()

	pygame.quit()
	# implicit exit()



def placeDefaultMap(world):
	centre = (world.width//2, world.height//2)
	world.placeConstruct(TownCentre(centre), centre)


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

			elif (event.key == pygame.K_f):
				gameManager.timeScaling = 5

			elif (event.key == pygame.K_SPACE):
				if gameManager.isEditing: #Can only toggle when editing, otherwise must wait for wave to finish. 
					gameManager.isEditing = not gameManager.isEditing 

				#We are now at war: gameManager.isEditing == False
					gameManager.waveNumber += 1
					
					while enemies != []:
						enemies.pop() #Inefficient, but otherwise doesn't overwrite reference

					width, height = world.getSize()
					redPath = calculatePathingArray((width - 1, height//2), world)
					bluePath = calculatePathingArray((0, height//2), world)

					numEnemies = 2+gameManager.waveNumber
					startY = world.height//2 - numEnemies//2
					for i in range(0, numEnemies):
						enemies.append(Enemy("RED", startY+i, world, redPath))
						enemies.append(Enemy("BLUE", startY+i, world, bluePath))
					
		elif (event.type == pygame.KEYUP):
			if (event.key == pygame.K_f):
				gameManager.timeScaling = 1





main()