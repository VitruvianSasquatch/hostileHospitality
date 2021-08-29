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

		self.money = 6 #Or farmers, or biomass, who cares

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

	dustClouds = [] #Unimportant


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

			#Finish animation, as will eventually complete and disappear. 
			for dustCloud in dustClouds:
				if (not dustCloud.draw(window, TILESIZE, dt)):
					dustClouds.remove(dustCloud)


			if gameManager.isEditing:
				moneyCount = mainFont.render(f"Remaining: ${gameManager.money}", True, (200, 200, 200))
				window.blit(moneyCount, (0, WINDOW_DIMENSIONS[1]-moneyCount.get_height()))

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


				for dungPosition in world.getConstructTypeLocs(DungHeap):
					if townCentre.isInRange(dungPosition):
						world.constructGrid[dungPosition[0]][dungPosition[1]] = None
						dustClouds.append(DustCloud(dungPosition))



				for enemy in enemies:
					opponent = enemy.testCombat(enemies)
					if opponent is not None:
						#Combat!
						dustClouds.append(DustCloud(enemy.position))
						dustClouds.append(DustCloud(opponent.position))
						enemies.remove(enemy)
						enemies.remove(opponent)

					justDied = enemy.update(dt, world)
					if justDied:
						dustClouds.append(DustCloud(enemy.position))
						enemies.remove(enemy)

					enemy.draw(window, TILESIZE)
					if enemy.isAtFinalDestination():
						dustClouds.append(DustCloud(enemy.position))
						enemies.remove(enemy)
				


				if enemies == []: #All either dead or off-screen
					gameManager.isEditing = True
					gameManager.money += 2*gameManager.waveNumber
					pitTraps = world.getConstructType(PitTrap)
					for pitTrap in pitTraps:
						pitTrap.isFull = False

					for townCentre in world.getConstructType(TownCentre):
						townCentre.setRangeFromDifficulty(gameManager.waveNumber) #Increase for next round
				
		


		pygame.display.flip()

	pygame.font.quit() # Handle before primary exit
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
					if gameManager.money > 0:
						gameManager.money -= 1
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
					redPath = calculatePathingArray(world.blueBase, world)
					bluePath = calculatePathingArray(world.redBase, world)

					dungheaps = world.getConstructType(DungHeap)
					for dungheap in dungheaps:
						x,y = dungheap.getCentre()
						pathing.floodFillAvoid((x,y), 2, redPath)
						pathing.floodFillAvoid((x,y), 2, bluePath)

					numEnemies = 2+gameManager.waveNumber
					startY = world.height//2 - numEnemies//2
					for i in range(0, numEnemies):
						enemies.append(Enemy("RED", (world.redBase[0], startY+i), world, redPath))
						enemies.append(Enemy("BLUE", (world.blueBase[0], startY+i), world, bluePath))
					
		elif (event.type == pygame.KEYUP):
			if (event.key == pygame.K_f):
				gameManager.timeScaling = 1




class DustCloud:
	def __init__(self, position):
		self.position = position
		self.t = 0.5


	def draw(self, window, tileSize, dt):
		self.t += dt
		x, y = self.position
		centre = x*tileSize + tileSize//2, y*tileSize +tileSize//2
		centres = [((tileSize//4)*math.sin(6*(self.t*i + 20)), (tileSize//4)*math.cos(6*(self.t*i + 20))) for i in range(1, 8)]
		for point in centres:
			movedCentre = centre[0] + point[0], centre[1] + point[1]
			pygame.draw.circle(window, (200, 200, 200), movedCentre, tileSize/4)
		
		return not self.t > 0.9



main()