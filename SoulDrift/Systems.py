import pygame
from Components import *

class MessagingSystem:
    
    def process(self, entity, componentName):
        component = entity.getComponent(componentName)
        messages = component.sendMessages()
        for note in messages:
            recipient, message = note
            entity.getComponent(recipient).receiveMessage(componentName, message)

class RenderingSystem:

    def __init__(self, spriteList):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Soul Drift")

        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

        self.sprites = spriteList

        self.ssheetBuffer = 1
        self.colorkey = pygame.Color("#ff00ff")
        self.spritesheetFile = "curses_square_16x16.png"
        self.spritesheet = pygame.image.load(self.spritesheetFile)
        self.spritesheet.set_colorkey(self.colorkey)
        self.playerDim = (16, 16)

    def getSprite(self, col, row):
        coords = (col-1)*16 + self.ssheetBuffer, (row-1)*16 + self.ssheetBuffer
        return self.spritesheet.subsurface(coords, self.playerDim)

    def add2SpriteList(self, renderComp):
        self.sprites.add(renderComp)

    def render(self):
        self.sprites.clear(self.screen, self.background)
        self.sprites.draw(self.screen)
        pygame.display.flip()

class PhysicsSystem:
    
    def __init__(self, spriteList):
        self.sprites = spriteList
