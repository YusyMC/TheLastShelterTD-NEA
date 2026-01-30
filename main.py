import pygame
import sys
from button import Button # Imports Button class from button.py
import assets # Imports assets.py
from assets import loadImage


# Initialise's Pygame
pygame.init()

# Game window
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The last Shelter TD")

# Function to get the custom game font at different sizes
def getFont(size):
    return pygame.font.Font("assets/fonts/gameFont.otf", size)

# main menu screen function
def mainMenu():
    # Infinite loop to keep the main menu running
    while True:
        # Gets the loaded background from assets.py and loads it
        screen.blit(assets.menuBG, (0, 0))

        # Gets mouse position
        menuMousePos = pygame.mouse.get_pos()
        # Renders main title text
        menuText = getFont(40).render("THE LAST SHELTER", True, "#ffffff") 
        # Create rectangle to position text
        menuRect = menuText.get_rect(center=(200, 160)) 
        # Renders Subtitle text
        TDText = getFont(20).render("TOWER DEFENCE", True, "#287D20")
        # Create rectangle to position text
        TDRect = menuText.get_rect(center=(270,195))
        # Gets the rectangle for the button backboard image
        buttonBackboardRect = assets.buttonBackboard.get_rect(center=(200, 360))
        # Gets the rectangle for the game logo
        logoRect = assets.logo.get_rect(center=(200,100))

        # Creates Play Button
        playBUTTON = Button(
            image=pygame.image.load("assets/menu/mainMenuButton.png"), # Loads button image
            xPos=200, yPos=300, # Position on the screen
            textInput="PLAY", # Text on the button
            font=getFont(50), # Font used for the button text
            baseColour="#ffffff", 
            hoverColour="#429724" # Colour of the button text when hovered with cursor
            )
        # Creates Options Button
        optionsBUTTON = Button(
            image=pygame.image.load("assets/menu/mainMenuButton.png"),
            xPos=200, yPos=400,
            textInput="SETTINGS",
            font=getFont(50),
            baseColour="#ffffff",
            hoverColour="#429724"
            )
        # Creates Exit Button
        quitBUTTON = Button(
            image=pygame.image.load("assets/menu/mainMenuButton.png"),
            xPos=200, yPos=500,
            textInput="EXIT",
            font=getFont(50),
            baseColour="#ffffff",
            hoverColour="#429724"
            )
        # Draws the button backboard image onto the screen
        screen.blit(assets.buttonBackboard, buttonBackboardRect)
        # Draws the logo image onto the screen
        screen.blit(assets.logo, logoRect)
        # Draws the game title onto the screen
        screen.blit(menuText, menuRect)
        # Draws the subtitle text onto the screen
        screen.blit(TDText, TDRect)

        # Loops through all buttons to update when hovered
        for button in [playBUTTON, optionsBUTTON, quitBUTTON]:
            button.changeColour(menuMousePos)
            button.update(screen)
        
        # Loop for event handling
        for event in pygame.event.get():
            # If window close button is pressed, exit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If the mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playBUTTON.checkForInput(menuMousePos):
                    return print(0) #placeholder TODO: play functions
                if optionsBUTTON.checkForInput(menuMousePos):
                    return print(0) #placeholder TODO: option function
                # If Exit button clicked, game closes
                if quitBUTTON.checkForInput(menuMousePos):
                    pygame.quit()
                    sys.exit()
        
        # Makes sure display is always updated
        pygame.display.update()

# mainMenu function called
mainMenu()