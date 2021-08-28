import os
import sys
import pygame

from construct import *
from ui import *
from world import *
from enemy import *

WINDOW_DIMENSIONS = (1280, 960)
TILESIZE = 64


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

	enemy = Enemy("RED", (9, 4))
	enemy.moveToDistant((6, 8))



	isGameRunning = True
	isEditing = True
	
	while isGameRunning:
		dt = clock.tick(60) / 1000

		# Handle inputs
		
		isGameRunning = handleInputs(world, buildMenu)

		world.draw(window, TILESIZE)

		if isEditing:
			gridCursorPosition = world.getCoordinate(pygame.mouse.get_pos(), TILESIZE)
			if True:#not buildMenuHasMouseFocus(buildMenu): 
				#Draw cursor highlight
				x = gridCursorPosition[0] * TILESIZE
				y = gridCursorPosition[1] * TILESIZE
				pygame.draw.rect(window, (200, 200, 200), (x, y, TILESIZE, TILESIZE), 5)

			buildMenu.draw(window)

		else:
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



def buildMenuHasMouseFocus(buildMenu):
	position = pygame.mouse.get_pos()
	return (position[0] > buildMenu.position[0] or position[1] < buildMenu.position[1])


def handleInputs(world, buildMenu):
	isGameRunning = True

	for event in pygame.event.get():

		if (event.type == pygame.QUIT):
			isGameRunning = False

		if event.type == pygame.MOUSEMOTION:
			pass

		elif (event.type == pygame.MOUSEBUTTONDOWN):
			buildMenu.mouseEvent(event.pos)
			# buildMenu.mouseEvent returns True if it handled the event					

	
	return isGameRunning





main()