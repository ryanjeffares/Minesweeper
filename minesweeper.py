import pygame
import random
import time
import shareddata
import tile

pygame.init()
pygame.display.set_caption('Minesweeper')

class Minesweeper:
    tiles = list()
    bombIndexes = list()
    tilesChecked = 0
    sharedData = shareddata.SharedData()

    def __init__(self):
        self.main()

    def createTiles(self):
        x = 40
        y = 120
        for i in range(480):
            if x > 1200:
                x = 40
                y += 40
            self.tiles.append(tile.Tile(x, y, self.sharedData.icons[11]))
            self.sharedData.screen.blit(self.tiles[i].icon, (x, y))
            x += 40
        counter = 0
        usedIndexes = list()
        while counter < 99:
            randIdx = random.randint(0, 479)
            self.tiles[randIdx].isBomb = True
            if randIdx not in usedIndexes:
                counter += 1
            self.bombIndexes.append(randIdx)

    def assignIcons(self):
        i = 0
        for t in self.tiles:
            count = 0
            if t.isBomb:
                t.checkedIcon = self.sharedData.icons[9]
            else:
                if i == 0:
                    check = (1, 30, 31)
                elif i == 29:
                    check = (-1, 29, 30)
                elif i == 450:
                    check = (-30, -29, 1)
                elif i == 479:
                    check = (-31, -30, -1)
                else:
                    if t.x == 40:
                        check = (-30, -29, 1, 30, 31)
                    elif t.x == 1200:
                        check = (-31, -30, -1, 29, 30)
                    elif t.y == 120:
                        check = (-1, 1, 29, 30, 31)
                    elif t.y == 720:
                        check = (-31, -30, -29, -1, 1)
                    else:
                        check = (-31, -30, -29, -1, 1, 29, 30, 31)
                for num in check:
                    if self.tiles[i + num].isBomb:
                        count += 1
                t.checkedIcon = self.sharedData.icons[count]
                if count == 0:
                    t.isZero = True
            self.sharedData.screen.blit(t.icon, (t.x, t.y))
            i += 1

    def checkTiles(self, index):
        if index == 0:
            check = (1, 30, 31)
        elif index == 29:
            check = (-1, 29, 30)
        elif index == 450:
            check = (-30, -29, 1)
        elif index == 479:
            check = (-31, -30, -1)
        else:
            if self.tiles[index].x == 40:
                check = (-30, -29, 1, 30, 31)
            elif self.tiles[index].x == 1200:
                check = (-31, -30, -1, 29, 30)
            elif self.tiles[index].y == 120:
                check = (-1, 1, 29, 30, 31)
            elif self.tiles[index].y == 720:
                check = (-31, -30, -29, -1, 1)
            else:
                check = (-31, -30, -29, -1, 1, 29, 30, 31)
        if len(check) > 0:
            for num in check:
                idx = index + num
                if not self.tiles[idx].isBomb:
                    if not self.tiles[idx].checked:
                        self.tiles[idx].icon = self.tiles[idx].checkedIcon
                        self.tiles[idx].checked = True
                        self.sharedData.screen.blit(self.tiles[idx].icon, (self.tiles[idx].x, self.tiles[idx].y))
                        self.tilesChecked += 1
                        if self.tiles[idx].isZero:
                            self.checkTiles(idx)

    def gameOver(self, success):
        if success:
            text = self.sharedData.fonts[0].render("CONGRATULATIONS!! PLAY AGAIN?", True, (0, 255, 0))
        else:
            text = self.sharedData.fonts[0].render("GAME OVER - CLICK TO RESTART.", True, (255, 0, 0))
        self.sharedData.screen.blit(text, (400, 40))

    def restart(self):
        pygame.draw.rect(self.sharedData.screen, (186, 186, 186), self.sharedData.rects[2], 600)
        self.tiles.clear()
        self.bombIndexes.clear()
        self.main()

    def main(self):
        start = time.time()
        self.createTiles()
        self.assignIcons()
        running = True
        gameIsOver = False
        flagsRemaining = 99
        while running:
            if not gameIsOver:
                pygame.draw.rect(self.sharedData.screen, (186, 186, 186), self.sharedData.rects[0], 40)
                pygame.draw.rect(self.sharedData.screen, (186, 186, 186), self.sharedData.rects[1], 40)
                elapsedTime = int(time.time() - start)
                timer = self.sharedData.fonts[0].render(str(elapsedTime), True, (0, 0, 0))
                flags = self.sharedData.fonts[0].render(str(flagsRemaining), True, (0, 0, 0))
                self.sharedData.screen.blit(timer, (40, 40))
                self.sharedData.screen.blit(flags, (1200, 40))
            if self.tilesChecked == 381:
                gameIsOver = True
                self.gameOver(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not gameIsOver:
                        pos = pygame.mouse.get_pos()
                        index = 0
                        for t in self.tiles:
                            if t.x <= pos[0] < t.x + 40 and t.y <= pos[1] < t.y + 40:
                                if event.button == 1:
                                    if t.isBomb:
                                        for b in self.bombIndexes:
                                            self.tiles[b].icon = self.tiles[b].checkedIcon
                                            self.sharedData.screen.blit(self.tiles[b].icon, (self.tiles[b].x, self.tiles[b].y))
                                        gameIsOver = True
                                        self.gameOver(False)
                                    else:
                                        t.icon = t.checkedIcon
                                        t.checked = True
                                        self.sharedData.screen.blit(t.icon, (t.x, t.y))
                                        if t.isZero:
                                            self.checkTiles(index)
                                        self.tilesChecked += 1
                                elif event.button == 3:
                                    if t.icon == self.sharedData.icons[11]:
                                        t.icon = self.sharedData.icons[10]
                                        flagsRemaining -= 1
                                    elif t.icon == self.sharedData.icons[10]:
                                        t.icon = self.sharedData.icons[11]
                                    self.sharedData.screen.blit(t.icon, (t.x, t.y))
                                break
                            index += 1
                    else:
                        pass
                        self.restart()
            pygame.display.update()

minesweeper = Minesweeper()
pygame.quit()
quit()
