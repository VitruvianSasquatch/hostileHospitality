import pygame

WIDTH = 800 # VGA standard as default
HEIGHT = 600 

def main():
	window = pygame.display.set_mode((WIDTH, HEIGHT))

	ticks = 0

	isGameRunning = True
	while isGameRunning:

		# Handle inputs
		for event in pygame.event.get():
			isGameRunning = handleEvent(event) # I can't remember how to pass references in Python

		print(ticks)
		ticks += 1
		pygame.display.flip()

	pygame.quit()
	# implicit return 0



def handleEvent(event):
	if (event.type == pygame.QUIT):
		print("Exiting")
		return False # isGameRunning
	else:
		return True # FIXME: Pass state by reference


main()