import pygame
import assets, enemy
import sys
from PIL import Image, ImageFilter
from enemy import Enemy
from turret import Turret

pygame.init()

# Menu Background unblurs transition
def menuUnblur():
    imgBG = Image.open("levels/map.png").convert("RGBA")

    # Empty List to sotre each animation frame
    frames = []
    for i in range(11):
        blurredBG = imgBG.filter(ImageFilter.GaussianBlur(radius=10-i))
        mode = blurredBG.mode
        size = blurredBG.size
        data = blurredBG.tobytes()
        # Converts image data to Python
        menuBG = pygame.image.fromstring(data, size, mode).convert_alpha()
        menuBG = pygame.transform.scale(menuBG, (1280,720))
        # Adds the frame to list of animation frames
        frames.append(menuBG)

    return frames

# Creates turret on mouse
def createTurret(turretIMG):
    # Gets mouse position
    mousePos = pygame.mouse.get_pos()
    # Converts pixel position into grid tile position
    mouseTileX = mousePos[0] // 80
    mouseTileY = mousePos[1] // 80
    # Selects up direction animation frame
    framesTurret = turretIMG["up"]
    # Creates animation frame using Turret class
    basicTurret = Turret(framesTurret[0], mouseTileX, mouseTileY)
    # Adds turret to group
    assets.turretGroup.add(basicTurret)   

# Reusable function that extracts animation frames
def animatedMovement(spritesheet, frameWidth, frameHeight, directions=None):
    # Array to store each animation step in order
    
    # Order by row of direction on spritesheet
    if directions is None:
        directions = ["up", "right", "down", "left"]
    
    # Gets total size of the sprite sheet
    sheetWidth = spritesheet.get_width()
    sheetHeight = spritesheet.get_height()

    # frames per row
    framesPerRow = sheetWidth // frameWidth

    # Dictionaru to store the frames
    animations = {}
    # Moves down the sprite sheet one row at a time
    for rowX, y in enumerate(range(0, sheetHeight, frameHeight)):
        frames = []
        # Moves across the sprite sheet fram by frame
        for x in range(0, sheetWidth, frameWidth):
            # Crops a single frame from the sprite sheet
            frame = spritesheet.subsurface((x, y, frameWidth, frameHeight))
            # Stores the fram in the array in the correct order
            frames.append(frame)
        
        # Assigns frames to directpm
        if rowX < len(directions):
            animations[directions[rowX]] = frames
    
    return animations
        

# Main game loop function
def gameLoop():
    
    # creates 1280x720 screen
    screen = pygame.display.set_mode((1280,720))
    # Display existing blurred menu background before transition starts
    screen.blit(assets.menuBG, (0,0))
    pygame.display.update()

    # Precompute frames and play them once
    frames = menuUnblur()

    # Iterates through each frame  of the unblur animation
    for menuBG in frames:
        screen.blit(menuBG, (0,0))

        # Keep the window responsive while the blur fades
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Show this intermediate blurred frame and pause briefly
        pygame.display.update()
        pygame.time.delay(180)  # milliseconds between steps to control animeation speed

        # Converts walker zombie spritesheet into individual animation frames
        walkingZombieAnimated = animatedMovement(
            spritesheet=assets.walkerZombie,
            frameWidth=48,
            frameHeight=64
        )

        basicTurretFrame = animatedMovement(
            spritesheet=assets.basicTurret,
            frameWidth=80,
            frameHeight=80
        )


        # Waypoints
        waypoints = [
            (1280,440), # Enemy Spawn Point
            (920,440), # First turn point
            (920,200), # Second turn point
            (520,200), # Third turn point
            (520,600), # Fourth turn point
            (280,600), # Fifth turn point
            (280,360), # Sixth turn point
            (40,360) # Zombie end point
        ]

        # creating enemy object
        enemy = Enemy(waypoints, walkingZombieAnimated)
        # Addes enemy to the group
        assets.enemyGroup.add(enemy)

    clock = pygame.time.Clock()

    while True:

        timeDiff = clock.tick(60) / 1000.0 # seconds since last frame

        # Displayes the fully unblurred image leaving in a state ready for gameplay
        screen.blit(frames[-1], (0,0))

        # Update group for every sprite in it
        assets.enemyGroup.update(timeDiff)

        # Draws every enemy sprite from the group onto the creen
        assets.enemyGroup.draw(screen)
        assets.turretGroup.draw(screen)

        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Checks if Left Mouse Click 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                createTurret(basicTurretFrame)
        
        #update display
        pygame.display.flip()
        
        pygame.display.update()