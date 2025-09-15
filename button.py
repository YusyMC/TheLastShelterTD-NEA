import pygame
#import sys

pygame.init()
#screen = pygame.display.set_mode((500, 500)) Will be used as a parameter in the code so it can be implemented in main.py
mainFont = pygame.font.SysFont("cambria", 50)



class Button:
    def __init__(self, image, xPos, yPos, textInput):
        self.image = image
        self.xPos = xPos
        self.yPos = yPos
        self.rect = self.image.get_rect(center=(self.xPos, self.yPos))
        self.textInput = textInput
        self.text = mainFont.render(self.textInput, True, "white")
        self.textRect = self.text.get_rect(center=(self.xPos, self.yPos))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            print("Button Registered.")

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = mainFont.render(self.textInput, True, "green")
        else:
            self.text = mainFont.render(self.textInput, True, "white")



# Testing
""" 
# Load and scale button image
buttonSurface = pygame.image.load("Button test.png")
buttonScale = pygame.transform.scale(buttonSurface, (400, 150))

# Use the scaled image 
button = Button(buttonScale, 250, 250, "Click")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button.checkForInput(pygame.mouse.get_pos())
    
    screen.fill("white")
    button.changeColor(pygame.mouse.get_pos())
    button.update()
    pygame.display.update()
"""