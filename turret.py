import pygame

# Creates Turret class and inherits from pygames sprite class
class Turret(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, tileX, tileY):
        # Integrates enemy object with pygame's sprite system
        pygame.sprite.Sprite.__init__(self)
        self.range = 90
        self.cooldown = 3000
        self.lastShot = pygame.time.get_ticks()
        # Store tile position inside object
        self.tileX = tileX
        self.tileY = tileY
        # Calculates centre coordinate of tile
        self.x = (self.tileX + 0.5) * 80
        self.y = (self.tileY + 0.5) * 80

        # animation variables
        self.spriteSheet = spriteSheet
        self.animationList = self.loadImages()
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()

        # Assigns turret's image
        self.image = self.animationList[self.frameIndex]
        # Created rectangle around image
        self.rect = self.image.get_rect()
        # Centre of rectangle
        self.rect.center = (self.x, self.y)
        """
        # transparent circle for range
        self.rangeImage = pygame.Surface((self.range * 2, self.range * 2))
        self.rangeImage.fill((0,0,0))
        self.rangeImage.set_colorkey((0,0,0))
        pygame.draw.circle(self.rangeImage, "grey100", (self.range, self.range))
        """

    def loadImages(self):
        # Extracts frames from spritesheet
        size = 80
        animationList = []
        for x in range(3):
            tempIMG = self.spriteSheet.subsurface(x * size, 0, 80, 80)
            animationList.append(tempIMG)
        return animationList
    
    def update(self):
        # Search for new target once turret cools down
        if pygame.time.get_ticks() - self.lastShot > self.cooldown:
            self.playAnimation()
    
    def playAnimation(self):
        # Updates image
        self.image = self.animationList[self.frameIndex]
        # checks if time has passed
        if pygame.time.get_ticks() - self.updateTime > 150:
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
            # check if finished and reset to normal
            if self.frameIndex >= len(self.animationList):
                self.frameIndex = 0
                self.lastShot = pygame.time.get_ticks()