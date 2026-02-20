import pygame

# Creates Turret class and inherits from pygames sprite class
class Turret(pygame.sprite.Sprite):
    def __init__(self, image, tileX, tileY):
        # Integrates enemy object with pygame's sprite system
        pygame.sprite.Sprite.__init__(self)
        # Store tile position inside object
        self.tileX = tileX
        self.tileY = tileY
        # Calculates centre coordinate of tile
        self.x = (self.tileX + 0.5) * 80
        self.y = (self.tileY + 0.5) * 80
        # Assigns turret's image
        self.image = image
        # Created rectangle around image
        self.rect = self.image.get_rect()
        # Centre of rectangle
        self.rect.center = (self.x, self.y)