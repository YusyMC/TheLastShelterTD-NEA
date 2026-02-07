import pygame

# Enemy class
class Enemy(pygame.sprite.Sprite): # Inheritance, all functionalities of sprite class 

    # Constructor Method
    def __init__(self, pos, image):
        # Integrates enemy object with pygame's sprite system
        pygame.sprite.Sprite.__init__(self)
        # Stores image of the sprite
        self.image = image
        # Creates rectangle from sprite image
        self.rect = self.image.get_rect()
        # Sets enemy position
        self.rect.center = pos
    
    # Updates movement
    def update(self):
        self.move()

    # For enemy movement
    def move(self):
        # Moves enemy horizontally
        self.rect.x += 1
    
    def takeDamage(self):
        return 0 # TODO

    def isDead(self):
        return 0 # TODO