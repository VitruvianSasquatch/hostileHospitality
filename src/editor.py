import os
import sys
import pygame
from pygame.constants import BUTTON_RIGHT
from pygame.image import save

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
WORLDFILE = "mapfile.csv"

def main():
	pygame.init()
	window = pygame.display.set_mode(WINDOW_DIMENSIONS)
	pygame.display.set_caption("Hostile Hospitality: Map editor")
	pygame.font.init()
	clock = pygame.time.Clock()

	pygame.mouse.set_visible(True)

	# Ensure map all fits on one screen
	mapWidth, mapHeight = WINDOW_DIMENSIONS
	mapWidth //= TILESIZE
	mapHeight //= TILESIZE
	world = World((mapWidth, mapHeight))

	# Font setup
	mainFont = pygame.font.SysFont('Arial', 24, bold = True)
	#mainFont = pygame.font.Font(defaultFontPath, 24)

	# Setup map scroll coordinates
	viewOffset = [0,0]
	worldOffsetDt = [0,0]

	# Setup selection coordinates
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
				currentCoords = world.getCoordinate(event.pos, TILESIZE)

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

				elif (event.pos[0] > 1180 and event.pos[1] > 910):
					world.toFile(WORLDFILE)

					world.fromFile(WORLDFILE)

				else:
					newConstruct = Construct(BLOCK_COLOURS[currentBlock], currentBlock)
					coord = world.getCoordinate(event.pos, TILESIZE)
					world.placeConstruct(newConstruct, coord)

			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == BUTTON_RIGHT:
				if (event.pos[0] <= 280 and event.pos[1] >= 480):
					pass
				elif (event.pos[0] > 1180 and event.pos[1] > 910):
					pass
				else:
					coord = world.getCoordinate(event.pos, TILESIZE)
					world.placeConstruct(None, coord)

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

		viewOffsetDt = (int(worldOffsetDt[0] * dt * 200), int(worldOffsetDt[1] * dt * 200))
		viewOffset = (viewOffset[0] + viewOffsetDt[0], viewOffset[1] + viewOffsetDt[1])
		world.moveViewOffset(viewOffsetDt)

		window.fill((0,0,0))
		world.draw(window, TILESIZE)

		if (currentCoords != (-1, -1)):
			x = currentCoords[0] * TILESIZE + viewOffset[0]
			y = currentCoords[1] * TILESIZE + viewOffset[1]
			pygame.draw.rect(window, (200, 200, 200), (x, y, TILESIZE, TILESIZE), 5)
		
		# Current Coordinate Readout
		pygame.draw.rect(window, (40,40,40), (0,0,200,50))
		xyTextSurface = mainFont.render("x: {}    y = {}".format(currentCoords[0], currentCoords[1]), True, (240,240,240), (40,40,40))
		window.blit(xyTextSurface, (20, (50 - xyTextSurface.get_height()) / 2))

		# Selection menu
		pygame.draw.rect(window, (40, 40, 40), (0, 480, 280, 480))
		pygame.draw.rect(window, BLOCK_COLOURS[0], (5, 485, 270, 120))
		pygame.draw.rect(window, BLOCK_COLOURS[1], (5, 605, 270, 120))
		pygame.draw.rect(window, BLOCK_COLOURS[2], (5, 720, 270, 120))
		pygame.draw.rect(window, BLOCK_COLOURS[3], (5, 840, 270, 120))

		# Save Button
		pygame.draw.rect(window, (40,40,40), (1180, 910, 100, 50)) 
		saveSurface = mainFont.render("Save", True, (240,240,240), (40,40,40))
		window.blit(saveSurface, (1220, 910 + (50 - saveSurface.get_height()) / 2))

		pygame.display.flip()

	pygame.font.quit()
	pygame.quit()	

main()