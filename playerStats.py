class PlayerStats():

    def __init__(self):
        self.shelterHealth = 100
        self.money = 150
        self.score = 0
    
    
    def addMoney(self, amount):
        # Called when enemy is killed to award currency
        self.money += amount
    
    def loseMoney(self, amount):
        # Called when player places turret or upgrades turret to deduct cost
        self.money -= amount
    
    def loseHealth(self, amount):

        # Health is capped at 0 to prevent negative values
        self.shelterHealth -= amount
        if self.shelterHealth < 0:
            self.shelterHealth = 0
    
    def addScore(self, amount):
        # Available for future scoring system
        self.score += amount