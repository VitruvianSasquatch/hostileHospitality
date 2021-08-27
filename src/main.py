import os
import sys
import pygame

from world import *

WINDOW_DIMENSIONS = (800, 600) # VGA standard as default


def main():
	pygame.init()
	window = pygame.display.set_mode(WINDOW_DIMENSIONS)
	pygame.display.set_caption("Hostile Hospitality")
	clock = pygame.time.Clock()


	initInput()

	world = World()


	isGameRunning = True
	while isGameRunning:
		dt = clock.tick(60)

		# Handle inputs
		for event in pygame.event.get():
			isGameRunning = handleEvent(event) # I can't remember how to pass references in Python

		world.draw(window)
		pygame.display.flip()

	pygame.quit()
	# implicit return 0


def initInput():
	pygame.mouse.set_visible(True)
	
	#TODO: Decide on and implement keyboard input options


def handleEvent(event):
	if (event.type == pygame.QUIT):
		print("Exiting")
		return False # isGameRunning
	else:
		return True #FIXME: Pass state by reference








main()