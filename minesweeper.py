import pygame
import random
import time
import shareddata
import tile

pygame.init()
pygame.display.set_caption('Minesweeper')

# Main container for game functionality
class Minesweeper:
    tiles = list()          # We will store tiles in a list, and which of those are mines
    bombIndexes = list()
    tilesChecked = 0        # Count the number of tiles checked so we know when the player has won
    sharedData = shareddata.SharedData()

    def __init__(self):
        self.main()         # Run the game when the class is instantiated

    def createTiles(self):
        x = 40
        y = 120
        for i in range(480):    # 480 (30 x 16) on an expert level board
            if x > 1200:
                x = 40
                y += 40
            self.tiles.append(tile.Tile(x, y, self.sharedData.icons[11]))
            if i == 0:  # Corners
                self.tiles[i].position = "topLeftCorner"
            elif i == 29:
                self.tiles[i].position = "topRightCorner"
            elif i == 450:
                self.tiles[i].position = "bottomLeftCorner"
            elif i == 479:
                self.tiles[i].position = "bottomRightCorner"
            else:
                if self.tiles[i].x == 40:       # Left and right
                    self.tiles[i].position = "left"
                elif self.tiles[i].x == 1200:
                    self.tiles[i].position = "right"
                elif self.tiles[i].y == 120:    # Top and bottom
                    self.tiles[i].position = "top"
                elif self.tiles[i].y == 720:
                    self.tiles[i].position = "bottom"
                else:                           # Any other mine
                    self.tiles[i].position = "middle"
            self.sharedData.screen.blit(self.tiles[i].icon, (x, y))
            x += 40
        counter = 0
        usedIndexes = list()
        while counter < 99:     # Turn 99 random tiles into mines
            randIdx = random.randint(0, 479)
            self.tiles[randIdx].isBomb = True
            if randIdx not in usedIndexes:
                counter += 1
            self.bombIndexes.append(randIdx)
        self.assignIcons()

    def assignIcons(self):      # This checks the adjacent tiles on each tile to count how many mines it touches
        for i, t in enumerate(self.tiles):
            count = 0
            if t.isBomb:        # If it's a mine already, give it the mine icon for when it is checked
                t.checkedIcon = self.sharedData.icons[9]
            else:
                check = self.sharedData.adjacentTilesToCheck[t.position]
                for num in check:
                    if self.tiles[i + num].isBomb:
                        count += 1
                t.checkedIcon = self.sharedData.icons[count]
                if count == 0:
                    t.isZero = True
            self.sharedData.screen.blit(t.icon, (t.x, t.y))

    def checkTiles(self, index):        # Check adjacent tiles to the tile the player has just uncovered
        check = self.sharedData.adjacentTilesToCheck[self.tiles[index].position]
        if len(check) > 0:
            for num in check:
                idx = index + num
                if not self.tiles[idx].isBomb:
                    if not self.tiles[idx].checked:
                        self.tiles[idx].icon = self.tiles[idx].checkedIcon
                        self.tiles[idx].checked = True
                        self.sharedData.screen.blit(self.tiles[idx].icon, (self.tiles[idx].x, self.tiles[idx].y))
                        self.tilesChecked += 1      # Increment the tiles uncovered
                        if self.tiles[idx].isZero:
                            self.checkTiles(idx)    # Run the function again on each further uncovered tile, if we should

    def gameOver(self, success):
        if success:
            text = self.sharedData.fonts[0].render("CONGRATULATIONS!! PLAY AGAIN?", True, (0, 255, 0))
        else:
            text = self.sharedData.fonts[0].render("GAME OVER - CLICK TO RESTART.", True, (255, 0, 0))
        self.sharedData.screen.blit(text, (400, 40))

    def restart(self):      # Reset the screen and clear the lists, start the game again
        pygame.draw.rect(self.sharedData.screen, (186, 186, 186), self.sharedData.rects[2], 600)
        self.tilesChecked = 0
        self.tiles.clear()
        self.bombIndexes.clear()
        self.main()

    def main(self):
        start = time.time() # Get start time of the game for the timer
        self.createTiles()  # Create our tiles
        running = True
        gameIsOver = False
        flagsRemaining = 99
        previousTime = 0
        timer = self.sharedData.fonts[0].render("0", True, (0, 0, 0))   # Set up a timer and flag counter
        flags = self.sharedData.fonts[0].render(str(flagsRemaining), True, (0, 0, 0))
        self.sharedData.screen.blit(timer, (40, 40))
        self.sharedData.screen.blit(flags, (1200, 40))
        while running:          # Game loop
            if not gameIsOver:
                elapsedTime = int(time.time() - start)  # Get the elapsed time in seconds
                if elapsedTime != previousTime:         # Update the counters only if a second has passed, so this is not being done every pass
                    pygame.draw.rect(self.sharedData.screen, (186, 186, 186), self.sharedData.rects[0], 40)
                    pygame.draw.rect(self.sharedData.screen, (186, 186, 186), self.sharedData.rects[1], 40)
                    timer = self.sharedData.fonts[0].render(str(elapsedTime), True, (0, 0, 0))
                    flags = self.sharedData.fonts[0].render(str(flagsRemaining), True, (0, 0, 0))
                    self.sharedData.screen.blit(timer, (40, 40))
                    self.sharedData.screen.blit(flags, (1200, 40))
                previousTime = elapsedTime
            if self.tilesChecked == 381:    # If the game is completed...
                gameIsOver = True
                self.gameOver(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not gameIsOver:
                        pos = pygame.mouse.get_pos()    # Get the mouse's position when clicked                        
                        for index, t in enumerate(self.tiles):
                            if t.x <= pos[0] < t.x + 40 and t.y <= pos[1] < t.y + 40:   # Find which tile was clicked
                                if event.button == 1:   # If it was a left click...
                                    if t.isBomb:        # If you clicked a bomb, you lose
                                        for b in self.bombIndexes:
                                            self.tiles[b].icon = self.tiles[b].checkedIcon
                                            self.sharedData.screen.blit(self.tiles[b].icon, (self.tiles[b].x, self.tiles[b].y))
                                        gameIsOver = True
                                        self.gameOver(False)
                                    else:               # If it wasn't a bomb, uncover it then check the adjacent tiles if it wasn't touching a mine
                                        t.icon = t.checkedIcon
                                        t.checked = True
                                        self.sharedData.screen.blit(t.icon, (t.x, t.y))
                                        if t.isZero:
                                            self.checkTiles(index)
                                        self.tilesChecked += 1  # Increment the tiles uncovered
                                elif event.button == 3:         # If it was a right click...
                                    if t.icon == self.sharedData.icons[11]: # If the tile wasn't flagged, flag it and decrement the flags remaining
                                        t.icon = self.sharedData.icons[10]
                                        flagsRemaining -= 1
                                    elif t.icon == self.sharedData.icons[10]:   # If it was flagged, unflag it
                                        t.icon = self.sharedData.icons[11]
                                    self.sharedData.screen.blit(t.icon, (t.x, t.y))
                                break                            
                    else:
                        self.restart()  # If the game is over, we can click anywhere on the screen to restart
            pygame.display.update()

minesweeper = Minesweeper() # Make an instance of the game - the __init__ function starts the game
pygame.quit()
quit()
