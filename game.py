import pygame, time
import assets
import sys
from PIL import Image, ImageFilter

pygame.init()




def gameLoop():
    screen = pygame.display.set_mode((1280,720))

    imgBG = Image.open("assets/map.png").convert("RGBA")


    print(time.time())

    while True:

        for i in range(11):
            blurredBG = imgBG.filter(ImageFilter.GaussianBlur(radius=10 - i))
            mode = blurredBG.mode
            size = blurredBG.size
            data = blurredBG.tobytes()
            menuBG = pygame.image.fromstring(data, size, mode).convert_alpha()
            menuBG = pygame.transform.scale(menuBG, (1280,720))
            screen.blit(menuBG, (0,0))

            # Keep the window responsive while the blur fades
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Show this intermediate blurred frame and pause briefly
            pygame.display.update()
            pygame.time.delay(180)  # milliseconds between steps

        # Final event handling outside the animation loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()