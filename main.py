#!/usr/bin/python
import pygame
from pygame.locals import *
import platform
from Components import *
from Systems import *

os = platform.system()
if os == 'Windows':
    delim = '\\'
else:
    delim = '/'

    
pygame.init()

characters = []
components = ["ai"]

sprites = pygame.sprite.Group()

config = ConfigSystem()
rendering = RenderingSystem(config, sprites)

player = Entity(rendering.getSprite(1,5), pygame.Rect((16,16), (16,16)))
characters.append(player)


rendering.add2SpriteList(player)

player.updateComponent(PlayerAIComponent.name, PlayerAIComponent(player))
player.updateComponent(MonsterCollisionComponent.name, MonsterCollisionComponent())

zero = Entity(rendering.getSprite(4,1), pygame.Rect((32, 32), (16,16)))
characters.append(zero)
zero.updateComponent(AIComponent.name, AIComponent())
zero.updateComponent(MonsterCollisionComponent.name, MonsterCollisionComponent())

rendering.add2SpriteList(zero)

pygame.event.set_blocked(MOUSEMOTION)
pygame.event.post(pygame.event.Event(USEREVENT, {"start": 1}))

dx = 0
dy = 0

physics = PhysicsSystem(sprites)

rendering.createBorder()
rendering.render()

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN:
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
            player.getComponent("ai").setMovement(dx, dy)

            for character in characters:
                character.getComponent("ai").update()
                character.update()
                physics.handleCollisions(character)
                
            rendering.render()