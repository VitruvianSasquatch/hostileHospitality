import os
import sys
import pygame

WINDOW_DIMENSIONS = (800, 600) # VGA standard as default

def main():
	pygame.init()
	window = pygame.display.set_mode(WINDOW_DIMENSIONS)
	pygame.display.set_caption("Hostile Hospitality")


	initInput()

	world = World()

	ticks = 0

	isGameRunning = True
	while isGameRunning:

		# Handle inputs
		for event in pygame.event.get():
			isGameRunning = handleEvent(event) # I can't remember how to pass references in Python

		ticks += 1

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



class World:

	def __init__(self):
		pass

	def draw(self, window):
		background = pygame.Surface(window.get_size()).convert()
		background.fill((0, 128, 0)) # Placeholder green background, likely remove when tiling is written
		window.blit(background, (0, 0))

		





main()