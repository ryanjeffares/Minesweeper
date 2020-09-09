import pygame

class Tile:
    icon = ''

    def __init__(self, isBomb, x, y):
        self.x = x
        self.y = y
        self.isBomb = isBomb
        if isBomb:
            icon = 'Resources/bomb.png'
        else:
            self.calculateNumber()

    def calculateNumber(self):
        pass
