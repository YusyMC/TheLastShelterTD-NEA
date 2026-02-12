import pygame
from pygame.math import Vector2

# Enemy class
class Enemy(pygame.sprite.Sprite): # Inheritance, all functionalities of sprite class 

    # Constructor Method
    def __init__(self, waypoints, animations):
        # Integrates enemy object with pygame's sprite system
        pygame.sprite.Sprite.__init__(self)
        # storing waypoints list
        self.waypoints = waypoints
        # Converts the first waypoint into a vector
        self.pos = Vector2(self.waypoints[0])
        # Stores index of the next waypoint to move towards
        self.targetWaypoint = 1
        # Speed changes for different variables
        self.speed = 60
        # Stores animation dictionary
        self.animations = animations
        # Sets starting direction
        self.direction = "left"
        # Tracks which frame is currently being displayed
        self.frameIndex = 0
        # Stores how much time has passed since last frame change
        self.animTimer = 0
        # Controls the animation speed
        self.animDelay = 0.1
        # Sets the starting sprite image
        self.image = self.animations[self.direction][0]
        # Creates rectangle from sprite image
        self.rect = self.image.get_rect(center=self.pos)
    
    # Updates movement and animation
    def update(self, timeDiff):
        self.move(timeDiff)
        self.animate(timeDiff)
    
    # Method for animation logic
    def animate(self, timeDiff):
        # time since last frame
        self.animTimer += timeDiff
        # Checks if enough time has passed to change the frame
        if self.animTimer >= self.animDelay:
            self.animTimer = 0 # Timer Reset
            # Selects correct animation list based on the direction of movement
            frames = self.animations[self.direction]
            # Cycles to next frame
            self.frameIndex = (self.frameIndex + 1) % len(frames)
            # Updates the sprite image to a new frame
            self.image = frames[self.frameIndex]

    # For enemy movement
    def move(self, timeDiff):
        # Checks if waypoint is in range
        if self.targetWaypoint >= len(self.waypoints):
            # Checks if enemy has reached the end of the path
            return # Stops moving
        
        # Converts next waypoint into a vector
        self.target = Vector2(self.waypoints[self.targetWaypoint])
        # Calculates direction of the vector from the enemy to the target waypoint
        self.movement = self.target - self.pos

        # Distance to target
        distance = self.movement.length()

        step = self.speed * timeDiff # pixels in the frame

        # Prevents errors when normalising 0 valued vectors
        if distance > 0:
            # Horizontal and vertical movement
            x = self.movement.x
            y = self.movement.y
            # Checks which direction is stronger
            if abs(x) > abs(y):
                # If horizontal
                self.direction = "right" if x > 0 else "left"
            else:
                # If vertical
                self.direction = "down" if y > 0 else "up"
        
        # Checks if remaining distance greater than speed
        if distance >= step:
            # Normalises direction vector and multiplies by speed
            self.pos += self.movement.normalize() * step
        else: # Runs when enemy is close to waypoint
            if distance > 0:
                # Moves enemy exactly onto the waypoint
                self.pos += self.movement.normalize() * distance
            # Goes to next waypoint
            self.targetWaypoint += 1
        # Updates rectangle position to vector position
        self.rect.center = (round(self.pos.x), round(self.pos.y))
    
    def takeDamage(self):
        return 0 # TODO

    def isDead(self):
        return 0 # TODO