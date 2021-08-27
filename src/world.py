import os
import sys
import pygame


class World:

	def __init__(self):
		pass

	def draw(self, window):
		background = pygame.Surface(window.get_size()).convert()
		background.fill((0, 128, 0)) # Placeholder green background, likely remove when tiling is written
		window.blit(background, (0, 0))