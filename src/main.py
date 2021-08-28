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


	viewOffset = (0, 0)

	isGameRunning = True
	while isGameRunning:
		dt = clock.tick(60) / 1000

		# Handle inputs
		for event in pygame.event.get():
			isGameRunning = handleEvent(event, buildMenu)

		enemy.update(dt)

		window.blit(world.draw(window, TILESIZE), viewOffset)
		enemy.draw(window, TILESIZE)
		buildMenu.draw(window)
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


def handleEvent(event, buildMenu):
	if (event.type == pygame.QUIT):
		print("Exiting")
		return False

	elif (event.type == pygame.MOUSEBUTTONDOWN):
		buildMenu.mouseEvent(event.pos)
		# buildMenu.mouseEvent returns True if it handled the event					

	return True





main()