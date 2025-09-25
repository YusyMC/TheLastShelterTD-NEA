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


def getFont(size):
    return pygame.font.Font("assets/fonts/gameFont.otf", size)


def mainMenu(): # main menu screen
    while True:
        screen.blit(assets.menuBG, (0, 0))

        menuMousePos = pygame.mouse.get_pos()
        menuText = getFont(50).render("The Last", True, "#ff0000")
        menuRect = menuText.get_rect(center=(150, 100))
        buttonBackboardRect = assets.buttonBackboard.get_rect(center=(150, 360))

        playBUTTON = Button(image=pygame.image.load("assets/buttonTest.png"), xPos=150, yPos=250, textInput="PLAY", font=getFont(50), baseColor="#ffffff", hoverColor="green")
        optionsBUTTON = Button(image=pygame.image.load("assets/buttonTest.png"), xPos=150, yPos=400, textInput="OPTIONS", font=getFont(50), baseColor="#ffffff", hoverColor="green")
        quitBUTTON = Button(image=pygame.image.load("assets/buttonTest.png"), xPos=150, yPos=550, textInput="EXIT", font=getFont(50), baseColor="#ffffff", hoverColor="green")

        screen.blit(assets.buttonBackboard, buttonBackboardRect) # button backboard
        screen.blit(menuText, menuRect) # menu text

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