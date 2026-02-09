import pygame
from pygame.math import Vector2

# Enemy class
class Enemy(pygame.sprite.Sprite): # Inheritance, all functionalities of sprite class 

    # Constructor Method
    def __init__(self, waypoints, image):
        # Integrates enemy object with pygame's sprite system
        pygame.sprite.Sprite.__init__(self)
        # storing waypoints list
        self.waypoints = waypoints
        # Converts the first waypoint into a vector
        self.pos = Vector2(self.waypoints[0])
        # Stores index of the next waypoint to move towards
        self.targetWaypoint = 1
        # Speed changes for different variables
        self.speed = 1
        # Stores image of the sprite
        self.image = image
        # Creates rectangle from sprite image
        self.rect = self.image.get_rect()
        # Sets enemy position
        self.rect.center = self.pos
    
    # Updates movement
    def update(self):
        self.move()

    # For enemy movement
    def move(self):
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
        
        # Checks if remaining distance greater than speed
        if distance >= self.speed:
            # Normalises direction vector and multiplies by speed
            self.pos += self.movement.normalize() * self.speed
        else: # Runs when enemy is close to waypoint
            if distance > 0:
                # Moves enemy exactly onto the waypoint
                self.pos += self.movement.normalize() * distance
            # Goes to next waypoint
            self.targetWaypoint += 1
        # Updates rectangle position to vector position
        self.rect.center = self.pos
    
    def takeDamage(self):
        return 0 # TODO

    def isDead(self):
        return 0 # TODO