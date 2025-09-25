import pygame
from PIL import Image, ImageFilter

pygame.init()

# MAIN MENU

# Menu background 
imgBG = Image.open("assets/placeholderBG.jpg")
blurredBG = imgBG.filter(ImageFilter.GaussianBlur(radius=5)) # Makes it blurry
mode = blurredBG.mode
size = blurredBG.size
data = blurredBG.tobytes()
menuBG = pygame.image.fromstring(data, size, mode)
menuBG = pygame.transform.scale(menuBG, (1280,720)) # sets menu background to 1280x720 to fit screen

# Button backboard

buttonBackboard = pygame.image.load("assets/menu/menu_button_backboard.png")