import pygame
import glob

pygame.init()

class SharedData:
    icons = list()
    fonts = list()
    rects = list()
    screen = pygame.display.set_mode((1280, 800))
    screen.fill((186, 186, 186))

    def __init__(self):
        self.loadImages()
        self.loadFonts()
        self.drawRects()

    def loadImages(self):
        imageDirectory = './Resources/Images/'
        for file in glob.glob(imageDirectory + '*.png'):
            self.icons.append(pygame.image.load(file))      # bomb : 9, flag : 10, unchecked : 11

    def loadFonts(self):
        fontsDirectory = './Resources/Fonts/'
        for file in glob.glob(fontsDirectory + '*.ttf'):
            self.fonts.append(pygame.font.Font(file, 64))

    def drawRects(self):
        self.rects.append(pygame.Rect(40, 40, 80, 40))      # 0 - rect to hide timer
        self.rects.append(pygame.Rect(1200, 40, 40, 40))    # 1 - rect to hide flag counter
        self.rects.append(pygame.Rect(400, 40, 600, 40))    # 2 - rect to hide game over text
