import pygame
import assets, enemy
import sys
from PIL import Image, ImageFilter
from enemy import Enemy

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

# Reusable function that extracts animation frames
def animatedMovement(spritesheet, frameWidth, frameHeight):
    # Array to store each animation step in order
    frames = []
    
    # Gets total size of the sprite sheet
    sheetWidth = spritesheet.get_width()
    sheetHeight = spritesheet.get_height()

    # Moves down the sprite sheet one row at a time
    for y in range(0, sheetHeight, frameHeight):
        # Moves across the sprite sheet fram by frame
        for x in range(0, sheetWidth, frameWidth):
            # Crops a single frame from the sprite sheet
            frame = spritesheet.subsurface((x, y, frameWidth, frameHeight))
            # Stores the fram in the array in the correct order
            frames.append(frame)
    # Returns frame to be used anywhere
    return frames

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

        # creating sprite group to store enemy objects
        enemyGroup = pygame.sprite.Group()

        # Waypoints
        waypoints = [
            (1280,440),
            (920,440),
            (920,200),
            (520,200),
            (520,600),
            (280,600),
            (280,360),
            (40,360)
        ]

        # creating enemy object
        enemy = Enemy(waypoints, walkingZombieAnimated[3])
        # Addes enemy to the group
        enemyGroup.add(enemy)

    while True:
    # Displayes the fully unblurred image leaving in a state ready for gameplay
        screen.blit(frames[-1], (0,0))

        # Update group for every sprite in it
        enemyGroup.update()

        # Draws every enemy sprite from the group onto the creen
        enemyGroup.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #update display
        pygame.display.flip()
        
        pygame.display.update()