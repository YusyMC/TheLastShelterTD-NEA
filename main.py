import pygame
import sys
from button import Button
from PIL import Image, ImageFilter


# Initialise's Pygame
pygame.init()

clock = pygame.time.Clock()

# menu background
imgBG = Image.open("assets/placeholderBG.jpg")
blurredBG = imgBG.filter(ImageFilter.GaussianBlur(radius=5))

mode = blurredBG.mode
size = blurredBG.size
data = blurredBG.tobytes()

menuBG = pygame.image.fromstring(data, size, mode)

# game window
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The last Shelter TD")
menuBG = pygame.transform.scale(menuBG, (1280,720)) # sets menu background to 1280x720 to fit screen

""" #ALL TEST FOR BUTTON
# Button test Config
buttonSurface = pygame.image.load("assets/buttonTest.png")
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
    
    screen.blit(menuBG,(0,0))
    button.changeColor(pygame.mouse.get_pos())
    button.update(screen)
    pygame.display.update()
"""

# https://github.com/baraltech/Menu-System-PyGame/blob/main/main.py

def getFont(size):
    return pygame.font.Font("assets/fonts/gameFont.otf")



def mainMenu(): # main menu screen
    while True:
        screen.blit(menuBG, (0, 0))

        menuMousePos = pygame.mouse.get_pos()
        menuText = get_font(100).render("Main Menu", True, "#ffffff")
        menuRect = menuText.get_rect(center=(640, 100))


pygame.quit()