import pygame
import assets, enemy
import sys, json
from PIL import Image, ImageFilter
from enemy import Enemy
from turret import Turret
from button import Button

pygame.init()

# Loading map.tmj into code
with open("levels/map.tmj") as file:
    mapData = json.load(file)

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
def createTurret(turretType):
    # Gets mouse position
    mousePos = pygame.mouse.get_pos()
    # Converts pixel position into grid tile position
    mouseTileX = mousePos[0] // 80
    mouseTileY = mousePos[1] // 80

    # Prevents placing turrets outside the map
    mapWidth = mapData.get("width", 0)
    mapHeight = mapData.get("height", 0)
    # Checks if X is inside map and Y is inside the map
    if not (0 <= mouseTileX < mapWidth and 0 <= mouseTileY < mapHeight):
        return
    
    # Read Tile Layer 1 and dont place if its 197 (non path tiles)
    try:
        # Accesses tile data from tmj
        layerData = mapData["layers"][0]["data"]
        tileIndex = mouseTileY * mapWidth + mouseTileX
        # Grabs tile ID
        tileID = layerData[tileIndex]
    # If something goes wrong, it stops the function.
    except Exception:
        return
    
    # Prevents placement on path
    if tileID != 197:
        return
    
    # Checks if space is occupied with another turret
    for t in assets.turretGroup:
        if getattr(t, "tileX", None) == mouseTileX and getattr(t, "tileY", None) == mouseTileY:
            return
    
    # Determine which spritesheet to use based on turret type
    if turretType == 0: # Basic Turret
        spriteSheet = assets.basicTurret
    elif turretType == 1: # Sniper turret
        spriteSheet = assets.sniperTurret
    else:
        return
    
    # Creates turret with the correct spritesheet
    turret = Turret(spriteSheet, mouseTileX, mouseTileY)
    # Adds turret to group
    assets.turretGroup.add(turret)

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

# detects if a player has clicked a turret  
def selectTurret(mousePos):
    # converts pixel position into grid tile position
    mouseTileX = mousePos[0] // 80
    mouseTileY = mousePos[1] // 80
    # checks if the tile is occupied by turret
    for t in assets.turretGroup:
        if getattr(t, "tileX", None) == mouseTileX and getattr(t, "tileY", None) == mouseTileY:
            return t

def clearSelection():
    for turret in assets.turretGroup:
        turret.selected = False

# Main game loop function
def gameLoop():
    
    # creates 1580x720 screen 
    screen = pygame.display.set_mode((1280 + 300,720))
    # Display existing blurred menu background before transition starts
    screen.blit(assets.menuBG, (0,0))
    pygame.display.update()


    selectedTurret = None

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
    
    # Creates a variable that stores which turret is selected (0=basic, 1=sniper, None=none)
    selectedTurretType = None

    # Creates a list to store all shop button objects
    shopButtons = [
        Button( # Basic Turret 
            image=pygame.image.load("assets/game/shop/basicTurretShop.png"),
            xPos=1345, yPos=100,
            clickedImage=pygame.image.load("assets/game/shop/basicTurretShopSelected.png")       
        ),

        Button( # Sniper Turret
            image=pygame.image.load("assets/game/shop/sniperTurretShop.png"),
            xPos=1410, yPos=100,
            clickedImage=pygame.image.load("assets/game/shop/sniperTurretShopSelected.png")       
        )
    ]
    # Upgrade button
    upgradeButton = Button(
        image=pygame.image.load("assets/menu/mainMenuButton.png"), # Loads button image
        xPos=1430, yPos=500, # Position on the screen
        textInput="UPGRADE", # Text on the button
        font=assets.getFont(50), # Font used for the button text
        baseColour="#ffffff", 
        hoverColour="#429724" # Colour of the button text when hovered with cursor
    )

    while True:

        timeDiff = clock.tick(60) / 1000.0 # seconds since last frame
        mousePos = pygame.mouse.get_pos()

        # Renders Shop UI
        shopText = assets.getFont(40).render("SHOP", True, "#ffffff")
        shopTextRect = shopText.get_rect(center=(1430, 40))
        buttonBackboardRect = assets.buttonBackboard.get_rect(center=(1430, 360))
        shopBackboardRect = assets.shopBackboard.get_rect(center=(1430,180))
        
        # Draws UI
        screen.blit(assets.buttonBackboard, buttonBackboardRect)
        screen.blit(assets.shopBackboard, shopBackboardRect)
        screen.blit(shopText, shopTextRect)
        # Displayes the fully unblurred image leaving in a state ready for gameplay
        screen.blit(frames[-1], (0,0))

        # Update group for every sprite in it
        assets.enemyGroup.update(timeDiff)
        assets.turretGroup.update(assets.enemyGroup)

        # highlight the selected turrent
        if selectedTurret:  
            selectedTurret.selected = True

        # Draws every enemy sprite from the group onto the creen
        assets.enemyGroup.draw(screen)
        for turret in assets.turretGroup:
            turret.draw(screen)

        # Draws the shop buttons
        for button in shopButtons:
            button.update(screen)
        
        # shows upgrade only when turret selected
        if selectedTurret:
            if selectedTurret.upgradeLevel < 4:
                upgradeButton.update(screen)

        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Checks if Left Mouse Click 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Tracks if a shop button is clicked
                buttonClicked = False
                
                # Loops through shop buttons
                for i, button in enumerate(shopButtons):
                    # checks if button was clicked
                    if button.checkForInput(mousePos):
                        buttonClicked = True
                        # Toggle logic
                        if button.isClicked:
                            button.isClicked = False
                            selectedTurretType = None
                        else:
                            # Ensures only one button is selected at a time
                            for btn in shopButtons:
                                btn.isClicked = False
                            # set selected button
                            button.isClicked = True
                            # Track turret type by button index (0=basic, 1=sniper)
                            selectedTurretType = i
                        break
                
                # Check if upgrade button was clicked (before clearing selection)
                if selectedTurret and upgradeButton.checkForInput(mousePos):
                        selectedTurret.upgrade()
                else:
                    selectedTurret = None
                    clearSelection()

                    # If click was not on a button  
                    if not buttonClicked and selectedTurretType is not None:
                        createTurret(selectedTurretType)
                    else:
                        selectedTurret = selectTurret(mousePos)
        
        #update display
        pygame.display.flip()
        
        pygame.display.update()

#gameLoop()