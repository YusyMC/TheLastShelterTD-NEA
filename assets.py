import pygame
from PIL import Image, ImageFilter

pygame.init()

# MAIN MENU

# Menu background 
imgBG = Image.open("levels/map.png").convert("RGBA")


blurredBG = imgBG.filter(ImageFilter.GaussianBlur(radius=10)) # Makes it blurry
mode = blurredBG.mode
size = blurredBG.size
data = blurredBG.tobytes()
menuBG = pygame.image.fromstring(data, size, mode)

menuBG = pygame.transform.scale(menuBG, (1280,720)) # sets menu background to 1280x720 to fit screen


# Button backboard

buttonBackboard = pygame.image.load("assets/menu/menu_button_backboard.png")
buttonBackboardMenu = pygame.transform.scale(buttonBackboard, (300,660))

# logo

logo = pygame.image.load("assets/menu/logo.png")
logo = pygame.transform.scale(logo, (100,100))

# Shop
shopBackboard = pygame.image.load("assets/game/shop/shopBackboard.png")

# Group Loading

# creating sprite group to store objects
enemyGroup = pygame.sprite.Group()
turretGroup = pygame.sprite.Group()

# Sprite Loading

#enemy spritesheets
walkerZombie = pygame.image.load("assets/objects/enemies/walker_zombie.png")
runnerZombie = pygame.image.load("assets/objects/enemies/running_zombie.png")
armouredZombie = pygame.image.load("assets/objects/enemies/armoured_zombie.png")
bossZombie = pygame.image.load("assets/objects/enemies/boss_zombie.png")

#defence sprite sheets
basicTurret = pygame.image.load("assets/objects/defences/basic_turret.png")
sniperTurret = pygame.image.load("assets/objects/defences/sniper_turret.png")

# Function to get the custom game font at different sizes
def getFont(size):
    return pygame.font.Font("assets/fonts/gameFont.otf", size)

def loadImage(path):
    pilImage = Image.open(path).convert("RGBA")
    mode = pilImage.mode
    size = pilImage.size
    data = pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode)