import pygame
from Components import *

class RenderingSystem:

    def __init__(self, config, spriteList):
        
        self.config = config
        
        self.screen = pygame.display.set_mode(self.config.res)
        pygame.display.set_caption("Soul Drift")

        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

        self.sprites = spriteList

        self.colorkey = pygame.Color(self.config.colorkey)
        self.spritesheet = pygame.image.load(self.config.ssheetFile)
        self.spritesheet.set_colorkey(self.colorkey)
        
        #self.createBorder()

    def getSprite(self, col, row):
        coords = (col-1)*self.config.dimension[0] + self.config.ssheetBuffer, (row-1)*self.config.dimension[1] + self.config.ssheetBuffer
        return self.spritesheet.subsurface(coords, self.config.dimension)

    def add2SpriteList(self, renderComp):
        self.sprites.add(renderComp)

    def update(self):
        self.sprites.update()
        
    def render(self):
        self.sprites.clear(self.screen, self.background)
        self.sprites.draw(self.screen)
        pygame.display.flip()
        
    def createBorder(self):
        wall = self.getSprite(self.config.wallSprite[0], self.config.wallSprite[1])
        collisionComp = BorderCollisionComponent()
        
        numVert = int(math.floor(self.config.res[1]/self.config.dimension[1])-1)
        numHoriz = int(math.floor(self.config.res[0]/self.config.dimension[0])-2)
        
        leftStart = 0, 0
        rightStart = self.config.res[0]-self.config.dimension[0], 0
        topStart = self.config.dimension[1], 0
        botStart = self.config.dimension[1], self.config.res[1]-self.config.dimension[1]
        
        for i in range(numVert):
            border = Entity(wall, pygame.rect.Rect(leftStart, self.config.dimension) )
            border.updateComponent(collisionComp.name, collisionComp)
            self.sprites.add(border)
            
            border = Entity(wall, pygame.rect.Rect(rightStart, self.config.dimension) )
            border.updateComponent(collisionComp.name, collisionComp)
            self.sprites.add(border)
            
            leftStart = leftStart[0], leftStart[1] + self.config.dimension[1]
            rightStart = rightStart[0], rightStart[1] + self.config.dimension[1]
            
        for i in range(numHoriz):
            border = Entity(wall, pygame.rect.Rect(topStart, self.config.dimension) )
            border.updateComponent(collisionComp.name, collisionComp)
            self.sprites.add(border)
            
            border = Entity(wall, pygame.rect.Rect(botStart, self.config.dimension) )
            border.updateComponent(collisionComp.name, collisionComp)
            self.sprites.add(border)
                      
            topStart = topStart[0] + self.config.dimension[0], topStart[1] 
            botStart = botStart[0] + self.config.dimension[0], botStart[1] 
        
class ConfigSystem:
    
    def __init__(self):
        self.res = 800,600
        self.dimension = 16,16
        self.ssheetBuffer = 1
        self.ssheetFile = "curses_square_16x16.png"
        self.colorkey = "#ff00ff"
        
        self.wallSprite = 4,3

class PhysicsSystem:
    
    def __init__(self, spriteList):
        self.sprites = spriteList
        
    def handleCollisions(self, sprite):
        undoneMove = False
        
        colliders = pygame.sprite.spritecollide(sprite, self.sprites, False)
        if sprite in colliders:
            colliders.remove(sprite)
        for item in colliders:
            if (item.getComponent("collision").passthrough == False and not undoneMove):
                sprite.undoMove()
                undoneMove = True
            if item.getComponent("collision").react:
                item.getComponent("collision").collide(sprite)
            if sprite.getComponent("collision").react:
                sprite.getComponent("collision").collide(item)
            
