import pygame
import sys
from button import Button # Imports Button class from button.py
import assets, game # Imports assets.py
from assets import loadImage


# Initialise's Pygame
pygame.init()
pygame.mixer.init()

# Game window
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Last Shelter TD")

# settings ui
def settingsUI():
    while True:

        # updates screen to new display
        pygame.display.update()
        # Fills screen with grey screen
        screen.fill((128, 128, 128))

        # Gets mouse position
        mousePos = pygame.mouse.get_pos()

        # Creating a button for the player to go back
        backButton = Button(
            image=pygame.image.load("assets/menu/mainMenuButton.png"),
            xPos=640, yPos=450,
            textInput="Back",
            font=assets.getFont(40),
            baseColour="#ffffff",
            hoverColour="#429724"
        )

        # Text to display that this feature will is coming soon
        settingsText = assets.getFont(40).render("COMING SOON!", True, "#ffffff")
        settingsTextRect = settingsText.get_rect(center=(640, 360))

        # Display text
        screen.blit(settingsText, settingsTextRect)

        # display button
        backButton.changeColour(mousePos)
        backButton.update(screen)

        # Event handler
        for event in pygame.event.get():
            # If user presses cross
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # When user presses back button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if the button is pressed
                if backButton.checkForInput(mousePos):
                    # Plays click sound
                    assets.buttonClickSound.play()
                    # Display main menu again
                    return mainMenu()

# main menu screen function
def mainMenu():
    # Infinite loop to keep the main menu running
    while True:
        # Gets the loaded background from assets.py and loads it
        screen.blit(assets.menuBG, (0, 0))

        # Gets mouse position
        menuMousePos = pygame.mouse.get_pos()
        # Renders main title text
        menuText = assets.getFont(40).render("THE LAST SHELTER", True, "#ffffff") 
        # Create rectangle to position text
        menuRect = menuText.get_rect(center=(200, 160)) 
        # Renders Subtitle text
        TDText = assets.getFont(20).render("TOWER DEFENCE", True, "#287D20")
        # Create rectangle to position text
        TDRect = menuText.get_rect(center=(270,195))
        # Gets the rectangle for the button backboard image
        buttonBackboardRect = assets.buttonBackboardMenu.get_rect(center=(200, 360))
        # Gets the rectangle for the game logo
        logoRect = assets.logo.get_rect(center=(200,100))

        # Creates Play Button
        playBUTTON = Button(
            image=pygame.image.load("assets/menu/mainMenuButton.png"), # Loads button image
            xPos=200, yPos=300, # Position on the screen
            textInput="PLAY", # Text on the button
            font=assets.getFont(50), # Font used for the button text
            baseColour="#ffffff", 
            hoverColour="#429724" # Colour of the button text when hovered with cursor
            )
        # Creates Options Button
        optionsBUTTON = Button(
            image=pygame.image.load("assets/menu/mainMenuButton.png"),
            xPos=200, yPos=400,
            textInput="SETTINGS",
            font=assets.getFont(50),
            baseColour="#ffffff",
            hoverColour="#429724"
            )
        # Creates Exit Button
        quitBUTTON = Button(
            image=pygame.image.load("assets/menu/mainMenuButton.png"),
            xPos=200, yPos=500,
            textInput="EXIT",
            font=assets.getFont(50),
            baseColour="#ffffff",
            hoverColour="#429724"
            )
        # Draws the button backboard image onto the screen
        screen.blit(assets.buttonBackboardMenu, buttonBackboardRect)
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
                    # plays click sound when clicked
                    assets.buttonClickSound.play()
                    return game.gameLoop() 
                if optionsBUTTON.checkForInput(menuMousePos):
                    assets.buttonClickSound.play()
                    # go to settings screen
                    return settingsUI()
                # If Exit button clicked, game closes
                if quitBUTTON.checkForInput(menuMousePos):
                    assets.buttonClickSound.play()
                    pygame.time.delay(500)  # Allow sound to play before quitting
                    #Quit Game
                    pygame.quit()
                    sys.exit()
        
        # Makes sure display is always updated
        pygame.display.update()

# mainMenu function called
mainMenu()