import pygame
from PIL import Image, ImageFilter

pygame.init()

# load and process background image and turns it blurry for aesthetics
imgBG = Image.open("assets/placeholderBG.jpg")
blurredBG = imgBG.filter(ImageFilter.GaussianBlur(radius=5))
mode = blurredBG.mode
size = blurredBG.size
data = blurredBG.tobytes()
menuBG = pygame.image.fromstring(data, size, mode)
menuBG = pygame.transform.scale(menuBG, (1280,720)) # sets menu background to 1280x720 to fit screen
