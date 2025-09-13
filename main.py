import pygame

# Initialises Pygame
pygame.init()

clock = pygame.time.Clock()

# game window
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("The last Shelter TD")

# game
while True:
    
    clock.tick(60) # FPS

    # event handler
    for event in pygame.event.get():

        # quit
        if event.type == pygame.QUIT:
            run = False

pygame.quit()