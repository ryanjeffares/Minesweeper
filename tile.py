class Tile:
    isBomb = False
    checked = False
    isZero = False
    checkedIcon = None
    position = None

    def __init__(self, x, y, icon):
        self.x = x
        self.y = y
        self.icon = icon
