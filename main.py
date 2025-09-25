import pygame
import sys
from button import Button
import assets


# Initialise's Pygame
pygame.init()

# game window
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The last Shelter TD")

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
    return pygame.font.Font("assets/fonts/gameFont.otf", size)


def mainMenu(): # main menu screen
    while True:
        screen.blit(assets.menuBG, (0, 0))

        menuMousePos = pygame.mouse.get_pos()
        menuText = getFont(100).render("Main Menu", True, "#ffffff")
        menuRect = menuText.get_rect(center=(640, 100))

        playBUTTON = Button(image=pygame.image.load("assets/buttonTest.png"), xPos=640, yPos=250, textInput="PLAY", font=getFont(75), baseColor="#ffffff", hoverColor="green")
        optionsBUTTON = Button(image=pygame.image.load("assets/buttonTest.png"), xPos=640, yPos=400, textInput="OPTIONS", font=getFont(75), baseColor="#ffffff", hoverColor="green")
        quitBUTTON = Button(image=pygame.image.load("assets/buttonTest.png"), xPos=640, yPos=550, textInput="EXIT", font=getFont(75), baseColor="#ffffff", hoverColor="green")

        screen.blit(menuText, menuRect)

        for button in [playBUTTON, optionsBUTTON, quitBUTTON]:
            button.changeColor(menuMousePos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playBUTTON.checkForInput(menuMousePos):
                    return 0 #placeholder TODO: play functions
                if optionsBUTTON.checkForInput(menuMousePos):
                    return 0 #placeholder TODO: option function
                if quitBUTTON.checkForInput(menuMousePos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
mainMenu()