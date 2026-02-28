import pygame
import assets, enemy
import sys, json
from PIL import Image, ImageFilter
from enemy import Enemy
from turret import Turret
from button import Button
from enemy_data import ENEMY_WAVE_DATA

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

# Wave spawning function - generates a queue of enemies for a wave
def spawnWave(waveNumber):

    # Retrieve the enemy composition for this wave from ENEMY_WAVE_DATA
    waveData = ENEMY_WAVE_DATA[waveNumber]
    
    # Create a queue (list) to store each enemy type that needs to spawn
    enemiesToSpawn = []
    
    # For each enemy type (walker, runner, armoured, boss) in the wave
    for enemyType, count in waveData.items():
        # Add the enemy type to the queue 'count' times
        for i in range(count):
            enemiesToSpawn.append(enemyType)
    
    # Return the complete queue of enemies to spawn
    return enemiesToSpawn

# Main game loop function
def gameLoop():
    
    # creates 1580x720 screen 
    screen = pygame.display.set_mode((1280 + 300,720))
    # Display existing blurred menu background before transition starts
    screen.blit(assets.menuBG, (0,0))
    pygame.display.update()

    # wave tracking
    currentWave = 0
    waveSpawned = False
    waveEnemiesSpawned = 0


    selectedTurret = None

    # Precompute frames and play them once
    frames = menuUnblur()

    # Converts walker zombie spritesheet into individual animation frames
    walkingZombieAnimated = animatedMovement(
        spritesheet=assets.walkerZombie,
        frameWidth=48,
        frameHeight=64
    )
    runnerZombieAnimated = animatedMovement(
        spritesheet=assets.runnerZombie,
        frameWidth=48,
        frameHeight=64
    )
    armouredZombieAnimated = animatedMovement(
        spritesheet=assets.armouredZombie,
        frameWidth=48,
        frameHeight=64
    )
    bossZombieAnimated = animatedMovement(
        spritesheet=assets.bossZombie,
        frameWidth=48,
        frameHeight=64
    )

    
    # Waypoints define the path enemies will follow across the map
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

    clock = pygame.time.Clock()
    
    # Store animations in a dictionary for easier access during spawning
    animations = {
        "walker": walkingZombieAnimated,
        "runner": runnerZombieAnimated,
        "armoured": armouredZombieAnimated,
        "boss": bossZombieAnimated
    }
    
    # Wave system spawn tracking variables
    enemiesToSpawn = []  # Queue of enemies waiting to be spawned for current wave
    spawnTimer = 0  # Timer tracking time since last enemy spawn
    spawnDelay = 1  # Delay in seconds between each enemy spawn (adjust to change difficulty)
    
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


        # Only triggers if all enemies from current wave are defeated AND there are more waves
        if len(assets.enemyGroup) == 0 and currentWave < len(ENEMY_WAVE_DATA):
            # If the spawn queue is empty, load the next wave
            if len(enemiesToSpawn) == 0:
                # Generate the queue of enemies for this wave
                enemiesToSpawn = spawnWave(currentWave)
                spawnTimer = 0  # Reset spawn timer
                currentWave += 1  # Increment wave counter for display

        # Timed enemy spawning - spawns enemies at intervals instead of all at once
        if enemiesToSpawn:
            # Accumulate time since last enemy spawn
            spawnTimer += timeDiff
            # Check if enough time has passed to spawn another enemy
            if spawnTimer >= spawnDelay:
                # Remove the next enemy type from the queue (FIFO - First In, First Out)
                enemyType = enemiesToSpawn.pop(0)
                # Create new enemy with correct animation and add to game
                newEnemy = Enemy(enemyType, waypoints, animations[enemyType])
                assets.enemyGroup.add(newEnemy)
                spawnTimer = 0  # Reset timer for next spawn

        # Renders Shop UI
        shopText = assets.getFont(40).render("SHOP", True, "#ffffff")
        shopTextRect = shopText.get_rect(center=(1430, 40))
        buttonBackboardRect = assets.buttonBackboard.get_rect(center=(1430, 360))
        shopBackboardRect = assets.shopBackboard.get_rect(center=(1430,180))
        # NEW: Display current wave number on screen
        # Shows which wave the player is currently on
        waveText = assets.getFont(50).render(f"Wave {currentWave}", True, "#ffffff")
        waveTextRect = waveText.get_rect(center=(1430, 650))
        
        # Draws UI
        # Render all UI elements on screen
        screen.blit(assets.buttonBackboard, buttonBackboardRect)
        screen.blit(assets.shopBackboard, shopBackboardRect)
        screen.blit(shopText, shopTextRect)
        screen.blit(waveText, waveTextRect)  # NEW: Draw wave number display
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
                if selectedTurret and selectedTurret.upgradeLevel < 4 and upgradeButton.checkForInput(mousePos):
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

gameLoop()