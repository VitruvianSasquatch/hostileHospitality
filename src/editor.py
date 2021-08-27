import os
import sys
import pygame

from construct import *
from world import *

'''
Stand alone map editor
Uses the same base settings as main.py
'''

WINDOW_DIMENSIONS = (1280, 960) # VGA standard as default
TILESIZE = 64
BLOCK_COLOURS = [
	(255,0,0),
	(0, 200, 0),
	(128, 128, 128),
	(50, 50, 200)
]

def main():
	pygame.init()
	window = pygame.display.set_mode(WINDOW_DIMENSIONS)
	pygame.display.set_caption("Hostile Hospitality: Map editor")
	clock = pygame.time.Clock()

	pygame.mouse.set_visible(True)

	# Ensure map all fits on one screen
	mapWidth, mapHeight = WINDOW_DIMENSIONS
	mapWidth //= TILESIZE
	mapHeight //= TILESIZE
	world = World((mapWidth, mapHeight))

	worldOffset = [0,0]
	worldOffsetDt = [0,0]

	currentBlock = 0
	currentCoords = (-1, -1)

	isGameRunning = True
	while isGameRunning:
		dt = clock.tick(60) / 1000

		# Handle inputs
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				isGameRunning = False

			if event.type == pygame.MOUSEMOTION:
				if (event.pos[0] > 280 or event.pos[1] < 480):
					currentCoords = (-1, -1)
				currentCoords = world.getCoordinate(event.pos, TILESIZE, worldOffset)

			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
				if (event.pos[0] <= 280 and event.pos[1] >= 480):
					# Block Selection Menu
					if (event.pos[1] < 600):
						currentBlock = 0
					elif (event.pos[1] < 720):
						currentBlock = 1
					elif (event.pos[1] < 840):
						currentBlock = 2
					elif (event.pos[1] <= 960):
						currentBlock = 3
					else:
						print("Mouse out of bounds x: "+event.pos[0])
				else:
					newConstruct = Construct(BLOCK_COLOURS[currentBlock])
					coord = world.getCoordinate(event.pos, TILESIZE, worldOffset)
					world.placeConstruct(newConstruct, coord)

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					worldOffsetDt[0] += 1
				elif event.key == pygame.K_RIGHT:
					worldOffsetDt[0] += -1
				elif event.key == pygame.K_UP:
					worldOffsetDt[1] += 1
				elif event.key == pygame.K_DOWN:
					worldOffsetDt[1] += -1
			
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					worldOffsetDt[0] += -1
				elif event.key == pygame.K_RIGHT:
					worldOffsetDt[0] += 1
				elif event.key == pygame.K_UP:
					worldOffsetDt[1] += -1
				elif event.key == pygame.K_DOWN:
					worldOffsetDt[1] += 1

		worldOffset[0] += worldOffsetDt[0] * dt * 200
		worldOffset[1] += worldOffsetDt[1] * dt * 200

		world.draw(window, TILESIZE, worldOffset)

		if (currentCoords != (-1, -1)):
			x = currentCoords[0] * TILESIZE + worldOffset[0]
			y = currentCoords[1] * TILESIZE + worldOffset[1]
			pygame.draw.rect(window, (200, 200, 200), (x, y, TILESIZE, TILESIZE), 5)
		
		pygame.draw.rect(window, (40, 40, 40), (0, 480, 280, 480))
		pygame.draw.rect(window, BLOCK_COLOURS[0], (5, 485, 270, 120))
		pygame.draw.rect(window, BLOCK_COLOURS[1], (5, 605, 270, 120))
		pygame.draw.rect(window, BLOCK_COLOURS[2], (5, 720, 270, 120))
		pygame.draw.rect(window, BLOCK_COLOURS[3], (5, 840, 270, 120))


		pygame.display.flip()

	pygame.quit()

main()