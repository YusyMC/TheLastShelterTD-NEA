import pygame

# Creates Turret class and inherits from pygames sprite class
class Turret(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, tileX, tileY):
        # Integrates enemy object with pygame's sprite system
        pygame.sprite.Sprite.__init__(self)
        # Stores attack range
        self.range = 90
        # Cooldown of animation
        self.cooldown = 3000
        # stores time of last fired
        self.lastShot = pygame.time.get_ticks()
        # stores whtere turret is being selectedby player
        self.selected = False
        # Store tile position inside object
        self.tileX = tileX
        self.tileY = tileY
        # Calculates centre coordinate of tile
        self.x = (self.tileX + 0.5) * 80
        self.y = (self.tileY + 0.5) * 80

        # animation variables
        self.spriteSheet = spriteSheet
        # to extract frames
        self.animationList = self.loadImages()
        # tracks which animation is displayed
        self.frameIndex = 0
        # srtores when last frame changed
        self.updateTime = pygame.time.get_ticks()

        # Assigns turret's image
        self.image = self.animationList[self.frameIndex]
        # Created rectangle around image
        self.rect = self.image.get_rect()
        # Centre of rectangle
        self.rect.center = (self.x, self.y)
        
        # transparent circle for range
        # creates a surface the size of a circle
        self.rangeImage = pygame.Surface((self.range * 2, self.range * 2))
        # makes it black temporarily
        self.rangeImage.fill((0,0,0))
        # black transparent
        self.rangeImage.set_colorkey((0,0,0))
        # draws the circle
        pygame.draw.circle(self.rangeImage, "grey100", (self.range, self.range), self.range)
        # makes the circle semi transparent
        self.rangeImage.set_alpha(100)
        # positions it above the turrent centre
        self.rangeRect = self.rangeImage.get_rect()
        self.rangeRect.center = self.rect.center

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

    # Manually draws the turret
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # If turret selected, draws the range circle
        if self.selected:
            surface.blit(self.rangeImage, self.rangeRect)