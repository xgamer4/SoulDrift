import pygame

import sys
sys.path.insert(1, "Components")

import math
from BaseComponents import *
from CollisionComponents import BorderCollisionComponent

class RenderingSystem:

    def __init__(self, config, logger, spriteList):
        
        self.config = config
        self.logger = logger
        
        self.screen = pygame.display.set_mode(self.config.res)
        pygame.display.set_caption("Soul Drift")
        
        self.font = pygame.font.Font(None, 16)

        backgroundx = self.config.mapSize[0]
        backgroundy = self.config.mapSize[1]

        if self.config.res[0] > self.config.mapSize[0]:
            backgroundx = self.config.res[0]

        if self.config.res[1] > self.config.mapSize[1]:
            backgroundy = self.config.res[1]

        self.background = pygame.Surface( (backgroundx, backgroundy) ).convert()
        
        self.background.fill((0, 0, 0))

        self.messageHeight = int(math.floor( (1.0/3)*self.config.res[1] ))
        self.statWidth = int(math.floor( (1.0/3)*self.config.res[0]))
        
        
        self.cameraSize = self.config.res[0] - self.statWidth, self.config.res[1] - self.messageHeight
        
        if self.cameraSize[0] > self.config.mapSize[0]:
            self.cameraSize = serowlf.config.mapSize[0], self.cameraSize[1]
            self.statWidth = self.res[0] - self.cameraSize[0]
        
        if self.cameraSize[1] > self.config.mapSize[1]:
            self.cameraSize = self.cameraSize[0], self.config.mapSize[1]
            self.messageHeight = self.res[1] - self.cameraSize[1]
        
        self.messageBar = pygame.Surface( (self.config.res[0], self.messageHeight) ).convert()
        self.messageBarLoc = 0, self.config.res[1]-self.messageHeight
        self.messageBar.fill( (0,0,0) )
        
        self.statWindow = pygame.Surface( (self.statWidth, self.config.res[1]-self.messageHeight) ).convert()
        self.statWindowLoc = self.config.res[0]-self.statWidth, 0
        self.statWindow.fill( (0, 0, 0) )
        
        self.map = pygame.Surface(self.config.mapSize).convert()

        self.sprites = spriteList

        self.colorkey = pygame.Color(self.config.colorkey)
        self.spritesheet = pygame.image.load(self.config.ssheetFile)
        self.spritesheet.set_colorkey(self.colorkey)
        
        #self.createBorder()

    def getSprite(self, col, row):
        coords = (col-1)*self.config.dimension[0], (row-1)*self.config.dimension[1]
        return self.spritesheet.subsurface(coords, self.config.dimension)

    def add2SpriteList(self, renderComp):
        self.sprites.add(renderComp)

    def update(self):
        self.sprites.update()
        
    def renderMessages(self):
        windowWidth = self.config.res[0]
        windowHeight = self.messageHeight - 20
        spacing = self.font.get_linesize()
        
        renderHeight = self.messageHeight
        
        messages = []
        
        cMessageLog = list(self.logger.messageLog)
        cMessageLog.reverse()  
        
        for color, line in cMessageLog:
            if renderHeight > 20:
                size = self.font.size(line)
                
                while size[0] > windowWidth:
                     splitLine = line.split()
                     secondLine = []
                     secondLine.append(splitLine.pop())
                     size = self.font.size(' '.join(splitLine))
                     cMessageLog.append( (color, ' '.join(splitLine)) )
                     line = ' '.join(secondLine)
                    
                        
                renderHeight = renderHeight - size[1]
                renderedLine = self.font.render(line, False, color, (0,0,0))
                self.messageBar.blit(renderedLine, (0, renderHeight))

    def renderStats(self, player):
        
        statblock = player.getComponent(StatComponent.name).stats
        width = self.statWindow.get_width()
        height = self.statWindow.get_height()
        
        renderHeight = 0
        renderWidth = 20
        hp = statblock["HP"]
        max_hp = statblock["Max HP"]
        
        hp_line = self.font.render("HP: " + str(hp) + "/" + str(max_hp), False, (0, 0, 255), (0,0,0) )
        self.statWindow.blit(hp_line, (renderWidth, 0))
        renderHeight = 16
        for key,value in statblock.iteritems():
            if key not in ("HP", "Max HP"):
                line = self.font.render(str(key) + ": " + str(value), False, (255,255,255), (0,0,0))
                self.statWindow.blit(line, (renderWidth, renderHeight))
                renderHeight += 16
                
        

    def render(self, player):
        
        self.sprites.clear(self.screen, self.background)
        self.sprites.clear(self.map, self.background)
                
        camera = self.map.get_rect(size=self.cameraSize)
        camera.center = player.rect.topleft
        camera.clamp_ip(self.map.get_rect())        
        
        
        self.sprites.draw(self.map)
        self.renderMessages()
        self.renderStats(player)
        
        windowBorderH = self.getSprite(self.config.windowBorderH[0], self.config.windowBorderH[1])
        windowBorderV = self.getSprite(self.config.windowBorderV[0], self.config.windowBorderV[1])
        
        for i in range(self.config.res[0]/self.config.dimension[0]):
            self.messageBar.blit(windowBorderH, (self.config.dimension[0]*i, 0))
            
        for i in range((self.config.res[1] - self.messageHeight)/self.config.dimension[1]):
            self.statWindow.blit(windowBorderV, (0, self.config.dimension[1]*i) )
        
        self.screen.blit(self.map, (0,0), camera)
        self.screen.blit(self.messageBar, self.messageBarLoc)
        self.screen.blit(self.statWindow, self.statWindowLoc)
        
        pygame.display.flip()
        
    def createBorder(self):
        wall = self.getSprite(self.config.wallSprite[0], self.config.wallSprite[1])
        collisionComp = BorderCollisionComponent()
        
        numVert = int(math.floor(self.config.mapSize[1]/self.config.dimension[1])-1)
        numHoriz = int(math.floor(self.config.mapSize[0]/self.config.dimension[0])-2)
        
        leftStart = 0, 0
        rightStart = self.config.mapSize[0]-self.config.dimension[0], 0
        topStart = self.config.dimension[1], 0
        botStart = self.config.dimension[1], self.config.mapSize[1]-self.config.dimension[1]
        
        for i in range(numVert):
            border = Entity(self.logger, wall, pygame.rect.Rect(leftStart, self.config.dimension) )
            border.updateComponent(collisionComp.name, collisionComp)
            self.sprites.add(border)
            
            border = Entity(self.logger, wall, pygame.rect.Rect(rightStart, self.config.dimension) )
            border.updateComponent(collisionComp.name, collisionComp)
            self.sprites.add(border)
            
            leftStart = leftStart[0], leftStart[1] + self.config.dimension[1]
            rightStart = rightStart[0], rightStart[1] + self.config.dimension[1]
            
        for i in range(numHoriz):
            border = Entity(self.logger, wall, pygame.rect.Rect(topStart, self.config.dimension) )
            border.updateComponent(collisionComp.name, collisionComp)
            self.sprites.add(border)
            
            border = Entity(self.logger, wall, pygame.rect.Rect(botStart, self.config.dimension) )
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
        self.windowBorderH = 14,13
        self.windowBorderV = 11,12
        
        self.mapSize = 800,600

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
            

class LoggingSystem:
    
    def __init__(self):
        self.messageLog = []
        
    