import pygame
import random
import tile
import sys
import time

sys.setrecursionlimit(1500)

pygame.init()
screen = pygame.display.set_mode((1280, 800))
screen.fill((186, 186, 186))

pygame.display.set_caption('Minesweeper')

start = time.time()
font = pygame.font.Font('Resources/popincourt.ttf', 64)

zeroIcon = pygame.image.load('Resources/zero.png')
oneIcon = pygame.image.load('Resources/one.png')
twoIcon = pygame.image.load('Resources/two.png')
threeIcon = pygame.image.load('Resources/three.png')
fourIcon = pygame.image.load('Resources/four.png')
fiveIcon = pygame.image.load('Resources/five.png')
sixIcon = pygame.image.load('Resources/six.png')
sevenIcon = pygame.image.load('Resources/seven.png')
eightIcon = pygame.image.load('Resources/eight.png')
bombIcon = pygame.image.load('Resources/bomb.png')
uncheckedIcon = pygame.image.load('Resources/unchecked.png')
flagIcon = pygame.image.load('Resources/flag.png')
icons = (zeroIcon, oneIcon, twoIcon, threeIcon, fourIcon, fiveIcon, sixIcon, sevenIcon, eightIcon)

tileIcons = list()
tileIconsUnchecked = list()
tileX = list()
tileY = list()
tileCoords = dict()
tileChecked = list()
tileIsBomb = list()
tileUncovered = list()
tileIsZero = list()

def populateLists():
    tileIcons.clear()
    tileIconsUnchecked.clear()
    tileX.clear()
    tileY.clear()
    tileCoords.clear()
    tileChecked.clear()
    tileIsBomb.clear()
    tileUncovered.clear()
    tileIsZero.clear()
    x = 40
    y = 120
    for i in range(480):
        if x == 1240:
            x = 40
            y += 40
        tileIcons.append(zeroIcon)
        tileIconsUnchecked.append(uncheckedIcon)
        tileX.append(x)
        tileY.append(y)
        tileCoords.update({x : y})
        tileChecked.append(False)
        tileIsBomb.append(False)
        tileUncovered.append(False)
        tileIsZero.append(False)
        x += 40

populateLists()

def createBombs():
    counter = 0
    usedIndexes = list()
    while counter < 99:
        randIdx = random.randint(0, 479)
        tileIcons[randIdx] = bombIcon
        tileIsBomb[randIdx] = True
        if randIdx not in usedIndexes:
            counter += 1
        usedIndexes.append(randIdx)

createBombs()

def numberTiles():
    for j in range(480):
        if tileIsBomb[j] is False:
            if j == 0:
                check = (1, 30, 31)
                count = 0
                for num in check:
                    if tileIsBomb[num]:
                        count += 1
            elif j == 29:
                check = (28, 58, 59)
                count = 0
                for num in check:
                    if tileIsBomb[num]:
                        count += 1
            elif j == 450:
                check = (420, 421, 451)
                count = 0
                for num in check:
                    if tileIsBomb[num]:
                        count += 1
            elif j == 479:
                check = (448, 449, 478)
                count = 0
                for num in check:
                    if tileIsBomb[num]:
                        count += 1
            else:
                if tileX[j] == 40:
                    check = (-30, -29, 1, 30, 31)
                    count = 0
                    for num in check:
                        if tileIsBomb[j + num]:
                            count += 1
                elif tileX[j] == 1200:
                    check = (-31, -30, -1, 29, 30)
                    count = 0
                    for num in check:
                        if tileIsBomb[j + num]:
                            count += 1
                elif tileY[j] == 120:
                    check = (-1, 1, 29, 30, 31)
                    count = 0
                    for num in check:
                        if tileIsBomb[j + num]:
                            count += 1
                elif tileY[j] == 720:
                    check = (-31, -30, -29, -1, 1)
                    count = 0
                    for num in check:
                        if tileIsBomb[j + num]:
                            count += 1
                else:
                    check = (-31, -30, -29, -1, 1, 29, 30, 31)
                    count = 0
                    for num in check:
                        if tileIsBomb[j + num]:
                            count += 1
            tileIcons[j] = icons[count]
        if tileIcons[j] == icons[0]:
            tileIsZero[j] = True
        screen.blit(tileIconsUnchecked[j], (tileX[j], tileY[j]))

numberTiles()

def checkTiles(index):
    if index == 0:
        check = (1, 30, 31)
    elif index == 29:
        check = (-1, 29, 30)
    elif index == 450:
        check = (-30, -29, 1)
    elif index == 479:
        check = (-31, -30, -1)
    else:
        if tileX[index] == 40:
            check = (-30, -29, 1, 30, 31)
        elif tileX[index] == 1200:
            check = (-31, -30, -1, 29, 30)
        elif tileY[index] == 120:
            check = (-1, 1, 29, 30, 31)
        elif tileY[index] == 720:
            check = (-31, -30, -29, -1, 1)
        else:
            check = (-31, -30, -29, -1, 1, 29, 30, 31)
    if len(check) > 0:
        for num in check:
            idx = index + num
            if not tileIsBomb[idx]:
                if not tileUncovered[idx]:
                    tileIconsUnchecked[idx] = tileIcons[idx]
                    tileUncovered[idx] = True
                    screen.blit(tileIconsUnchecked[idx], (tileX[idx], tileY[idx]))
                    if tileIsZero[idx]:
                        checkTiles(idx)

def gameOver():
    text = font.render("GAME OVER. CLICK TO RESTART.", True, (255, 0, 0))
    screen.blit(text, (400, 40))

rect3 = pygame.Rect(400, 40, 600, 40)
gameIsOver = False

def restart():
    pygame.draw.rect(screen, (186, 186, 186), rect3, 600)
    populateLists()
    createBombs()
    numberTiles()
    global gameIsOver
    global start
    global flagsRemaining
    gameIsOver = False
    flagsRemaining = 99
    start = time.time()

running = True
rect = pygame.Rect(40, 40, 80, 40)
rect2 = pygame.Rect(1200, 40, 40, 40)
flagsRemaining = 99

while running:
    if not gameIsOver:
        pygame.draw.rect(screen, (186, 186, 186), rect, 40)
        pygame.draw.rect(screen, (186, 186, 186), rect2, 40)
        elapsedTime = int(time.time() - start)
        timer = font.render(str(elapsedTime), True, (0, 0, 0))
        flags = font.render(str(flagsRemaining), True, (0, 0, 0))
        screen.blit(timer, (40, 40))
        screen.blit(flags, (1200, 40))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not gameIsOver:
                pos = pygame.mouse.get_pos()
                index = 0
                if event.button == 1:
                    for x in tileX:
                        if x <= pos[0] < x + 40 and tileY[index] <= pos[1] < tileY[index] + 40:
                            if tileIconsUnchecked[index] != flagIcon:
                                print(index)
                                if tileIsBomb[index]:
                                    tileIconsUnchecked[index] = tileIcons[index]
                                    screen.blit(tileIconsUnchecked[index], (tileX[index], tileY[index]))
                                    for i in range(480):
                                        if tileIsBomb[i]:
                                            tileIconsUnchecked[i] = tileIcons[i]
                                        screen.blit(tileIconsUnchecked[i], (tileX[i], tileY[i]))
                                    gameIsOver = True
                                    gameOver()
                                else:
                                    tileIconsUnchecked[index] = tileIcons[index]
                                    tileUncovered[index] = True
                                    screen.blit(tileIconsUnchecked[index], (tileX[index], tileY[index]))
                                    if tileIsZero[index]:
                                        checkTiles(index)
                        index += 1
                elif event.button == 3:
                    print("Right click")
                    print(pos)
                    for x in tileX:
                        if x <= pos[0] < x + 40 and tileY[index] <= pos[1] < tileY[index] + 40:
                            if tileIconsUnchecked[index] == uncheckedIcon:
                                if flagsRemaining > 0:
                                    tileIconsUnchecked[index] = flagIcon
                                    flagsRemaining -= 1
                            elif tileIconsUnchecked[index] == flagIcon:
                                tileIconsUnchecked[index] = uncheckedIcon
                            screen.blit(tileIconsUnchecked[index], (tileX[index], tileY[index]))
                        index += 1
            else:
                restart()
    pygame.display.update()

pygame.quit()
quit()
