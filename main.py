import pygame
import sys
from button import Button


# Initialise's Pygame
pygame.init()

clock = pygame.time.Clock()

# game window
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("The last Shelter TD")


# Button Config
buttonSurface = pygame.image.load("assets/button.png")
buttonScale = pygame.transform.scale(buttonSurface, (400, 150))

button = Button(buttonScale, 250, 250, "Click")


# game
while True:
    
    clock.tick(60) # FPS

    # event handler
    for event in pygame.event.get():

        # quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Button Registered")
    
    screen.fill("white")
    button.changeColor(pygame.mouse.get_pos())
    button.update(screen)
    pygame.display.update()


# https://github.com/baraltech/Menu-System-PyGame/blob/main/main.py

def mainMenu(): # main menu screen

    return None

pygame.quit()