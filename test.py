import pygame
import os

pygame.mixer.init()

os.chdir(os.path.join(os.getcwd(), 'alphabet/'))

for file in os.listdir():
	print(file)
	i = input()
	if i != "y":
		continue
	sound = pygame.mixer.Sound(file)
	sound.set_volume(1)
	playing = sound.play()
	while playing.get_busy():
		pygame.time.wait(100)

