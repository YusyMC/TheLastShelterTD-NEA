import pygame, math
import assets
from turret_data import BASIC_TURRET_DATA, SNIPER_TURRET_DATA
# Creates Turret class and inherits from pygames sprite class
class Turret(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, tileX, tileY):
        # Integrates enemy object with pygame's sprite system
        pygame.sprite.Sprite.__init__(self)
        self.upgradeLevel = 1
        # animation variables
        self.spriteSheet = spriteSheet

        # Checks which sprite sheet is being used so it can identify the object data to use
        if self.spriteSheet == assets.basicTurret:
            self.range = BASIC_TURRET_DATA[self.upgradeLevel - 1].get("range")
            # Cooldown of animation
            self.cooldown = BASIC_TURRET_DATA[self.upgradeLevel - 1].get("cooldown")
            # Damage dealt depending on level
            self.damage = BASIC_TURRET_DATA[self.upgradeLevel - 1].get("damage")
        if self.spriteSheet == assets.sniperTurret:
            self.range = SNIPER_TURRET_DATA[self.upgradeLevel - 1].get("range")
            # Cooldown of animation
            self.cooldown = SNIPER_TURRET_DATA[self.upgradeLevel - 1].get("cooldown")
            # Damage dealt depending on level
            self.damage = SNIPER_TURRET_DATA[self.upgradeLevel - 1].get("damage")

        # stores time of last fired
        self.lastShot = pygame.time.get_ticks()
        # stores whtere turret is being selectedby player
        self.selected = False
        # Stores target that turret is aiming at
        self.target = None
        # Store tile position inside object
        self.tileX = tileX
        self.tileY = tileY
        # Calculates centre coordinate of tile
        self.x = (self.tileX + 0.5) * 80
        self.y = (self.tileY + 0.5) * 80

        # to extract frames
        self.animationList = self.loadImages()
        # tracks which animation is displayed
        self.frameIndex = 0
        # srtores when last frame changed
        self.updateTime = pygame.time.get_ticks()

        # stores to control angle rotation
        self.angle = 90
        # Assigns turret's original image
        self.OrignalImage = self.animationList[self.frameIndex]
        # storing rotating turret image
        self.image = pygame.transform.rotate(self.OrignalImage, self.angle)
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
    
    def update(self, enemyGroup):
        # only fires when there is a target now
        if self.target:
            self.playAnimation()
        else:
            # Search for new target once turret cools down
            if pygame.time.get_ticks() - self.lastShot > self.cooldown:
                self.pickTarget(enemyGroup)
    
    def pickTarget(self, enemyGroup):
        # Pythagoras theorem to calculate distance
        xDistance = 0
        yDistance = 0
        for enemy in enemyGroup:
            if enemy.health > 0:
                xDistance = enemy.pos[0] - self.x
                yDistance = enemy.pos[1] - self.y
                distance = math.sqrt(xDistance**2 + yDistance**2)
                if distance < self.range:
                    self.target = enemy
                    # calculates the angle towards it
                    self.angle = math.degrees(math.atan2(-yDistance, xDistance))
                    # Damage enemy
                    self.target.health -= self.damage
    
    def playAnimation(self):
        # Updates image
        self.OrignalImage = self.animationList[self.frameIndex]
        # checks if time has passed
        if pygame.time.get_ticks() - self.updateTime > 150:
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
            # check if finished and reset to normal
            if self.frameIndex >= len(self.animationList):
                self.frameIndex = 0
                self.lastShot = pygame.time.get_ticks()
                # Resetting target after animation
                self.target = None

 
    # upgrade method for upgrading turret
    def upgrade(self, playerStats):
        # Get the upgrade cost for current level
        upgradeCost = 0
        if self.spriteSheet == assets.basicTurret:
            upgradeCost = BASIC_TURRET_DATA[self.upgradeLevel - 1].get("upgradeToNextLevelCost")
        elif self.spriteSheet == assets.sniperTurret:
            upgradeCost = SNIPER_TURRET_DATA[self.upgradeLevel - 1].get("upgradeToNextLevelCost")
        
        # Check if player has enough money
        if playerStats.money < upgradeCost:
            return False  # Insufficient funds
        
        # Deduct cost and upgrade
        playerStats.loseMoney(upgradeCost)
        self.upgradeLevel += 1
        
        if self.spriteSheet == assets.basicTurret:
            self.range = BASIC_TURRET_DATA[self.upgradeLevel - 1].get("range")
            # Cooldown of animation
            self.cooldown = BASIC_TURRET_DATA[self.upgradeLevel - 1].get("cooldown")
        if self.spriteSheet == assets.sniperTurret:
            self.range = SNIPER_TURRET_DATA[self.upgradeLevel - 1].get("range")
            # Cooldown of animation
            self.cooldown = SNIPER_TURRET_DATA[self.upgradeLevel - 1].get("cooldown")

        # upgrade range circle
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
        
        return True  # Upgrade successful
            
    # Manually draws the turret
    def draw(self, surface):
        # Rotating
        self.image = pygame.transform.rotate(self.OrignalImage, self.angle - 90)
        # Calculating rect after rotation
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        # If turret selected, draws the range circle
        if self.selected:
            surface.blit(self.rangeImage, self.rangeRect)