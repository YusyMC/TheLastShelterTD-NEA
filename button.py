import pygame
#import sys

pygame.init()
#screen = pygame.display.set_mode((500, 500)) #Will be used as a parameter in the code so it can be implemented in main.py


class Button:
    # Constructor method that runs when Button class is called
    def __init__(self, image, xPos, yPos, textInput=None, font=None, baseColour=None, hoverColour=None, clickedImage=None): 
        # Stores button image
        self.image = image
        # Stores alternative image when button is clicked
        self.clickedImage = clickedImage
        # Tracks if button is currently clicked
        self.isClicked = False
        # Stores x position of button's centre
        self.xPos = xPos 
        # Stores y position of button's centre
        self.yPos = yPos
        # Stores font used to render button text 
        self.font = font
        # Stores text that will apear on button
        self.textInput = textInput 
        # Stores both text colour and hover colour
        self.baseColour, self.hoverColour = baseColour, hoverColour 
        # Creates rectangle for button image and centres it at xPos and yPos
        self.rect = self.image.get_rect(center=(self.xPos, self.yPos))
        # Only renders text if both textInput and font are provided 
        if self.textInput is not None and self.font is not None:
            # Renders button using the base colour
            self.text = self.font.render(self.textInput, True, self.baseColour)
            # Creates a rectangle for the text and centres it on the button
            self.textRect = self.text.get_rect(center=(self.xPos, self.yPos))
        else:
            self.text = None
            self.textRect = None
        # If no image is given, use the text as the image
        if self.image is None:
            self.image = self.text

    def toggleClicked(self):
        # Toggle between clicked and normal states
        self.isClicked = not self.isClicked

    def update(self, screen): # Draws button and text onto the screen
        # If button is clicked use clicked image
        currentImage = self.clickedImage if (self.isClicked and self.clickedImage is not None) else self.image
        screen.blit(currentImage, self.rect) # Draws button image onto screen
        if self.text is not None: # Only draws text if its there
            screen.blit(self.text, self.textRect) # Draws text image onto the button image

    def checkForInput(self, position): # Checks if mouse is touching the button
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColour(self, position, hoverColour=None, baseColour=None): # Chnages text colour depending if button is hovered
        if self.text is None or self.font is None:
            return
        # Uses custom or default colours
        hColour = hoverColour if hoverColour is not None else self.hoverColour
        bColour = baseColour if baseColour is not None else self.baseColour
        # If mouse is over button, the text is rendered in the colour
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.textInput, True, pygame.Color(hColour))
        else:
            # Otherwise render it in base colour
            self.text = self.font.render(self.textInput, True, pygame.Color(bColour))


"""
# Testing
 
# Load and scale button image
buttonSurface = pygame.image.load("assets/menu/mainMenuButton.png")
buttonScale = pygame.transform.scale(buttonSurface, (400, 150))

# Use the scaled image 
button = Button(
    image=pygame.image.load("assets/menu/mainMenuButton.png"),
    xPos=150, yPos=250, 
    textInput="Test", 
    font=pygame.font.Font("assets/fonts/gameFont.otf", 50),
    baseColour="#ffffff",
    hoverColour="#429724"
    )

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button.checkForInput(pygame.mouse.get_pos())
    
    screen.fill("white")
    button.changeColour(pygame.mouse.get_pos())
    button.update(screen)
    pygame.display.update()
"""