import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound("output.mp3")
player =  sound.play()

while player.get_busy():
	pygame.time.wait(100)
