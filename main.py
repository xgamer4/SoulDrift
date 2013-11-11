#!/usr/bin/python

import sys
sys.path.insert(1, 'Components')

import pygame
from pygame.locals import *
import platform
from BaseComponents import Entity
from AIComponents import *
from CollisionComponents import *
from Systems import *

os = platform.system()
if os == 'Windows':
    delim = '\\'
else:
    delim = '/'

    
pygame.init()
clock = pygame.time.Clock()

characters = []
components = ["ai"]

sprites = pygame.sprite.Group()

config = ConfigSystem()
logger = LoggingSystem()
rendering = RenderingSystem(config, logger, sprites)

player = Entity(logger, rendering.getSprite(1,5), pygame.Rect((16,16), (16,16)))
characters.append(player)

player.logMessage( ((0,0,0), "I'm the player!"))

rendering.add2SpriteList(player)

player.updateComponent(PlayerAIComponent.name, PlayerAIComponent(player))
player.updateComponent(MonsterCollisionComponent.name, MonsterCollisionComponent())
player.updateComponent(StatComponent.name, StatComponent())

zero = Entity(logger, rendering.getSprite(4,1), pygame.Rect((32, 32), (16,16)))
characters.append(zero)
zero.updateComponent(AIComponent.name, DummyAIComponent())
zero.updateComponent(MonsterCollisionComponent.name, MonsterCollisionComponent())
zero.updateComponent(StatComponent.name, StatComponent())

rendering.add2SpriteList(zero)

pygame.event.set_blocked(MOUSEMOTION)
pygame.event.post(pygame.event.Event(USEREVENT, {"start": 1}))

dx = 0
dy = 0

physics = PhysicsSystem(sprites)

rendering.createBorder()
rendering.render(player)

keyHeld = False

def gameUpdate(dx, dy):
    player.getComponent("ai").setMovement(dx, dy)

    for character in characters:
        character.getComponent("ai").update()
        character.update()
        physics.handleCollisions(character)

    rendering.render(player)

while 1:

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN:
            keyHeld = True
            if event.key == K_UP:
                dx = 0
                dy = -16
            elif event.key == K_DOWN:
                dx = 0
                dy = 16
            elif event.key == K_RIGHT:
                dx = 16
                dy = 0
            elif event.key == K_LEFT:
                dx = -16
                dy = 0
            elif event.key == K_k:
                player.logMessage( ((255, 0,0), "I pressed 'K'! :)") )
            elif event.key == K_j:
                player.logMessage( ( (0,255,0), "I pressed 'J'! :)") )
            
            gameUpdate(dx, dy)
        elif event.type == KEYUP:
            keyHeld = False 




