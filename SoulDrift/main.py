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
components = ["ai", "render"]

sprites = pygame.sprite.Group()

rendering = RenderingSystem(sprites)
messaging = MessagingSystem()


player = Entity()
characters.append(player)


player.updateComponent("render", RenderableComponent(rendering.getSprite(1, 5), pygame.Rect( (0,0), (16,16) )))

rendering.add2SpriteList(player.getComponent("render"))

player.updateComponent("ai", PlayerAIComponent(player))
player = player.getComponent("ai")


zero = Entity()
characters.append(zero)
zero.updateComponent("render", RenderableComponent(rendering.getSprite(4,1), pygame.Rect((16,16), (16,16)))) 
zero.updateComponent("ai", AIComponent())

rendering.add2SpriteList(zero.getComponent("render"))

pygame.event.set_blocked(MOUSEMOTION)
pygame.event.post(pygame.event.Event(USEREVENT, {"start": 1}))

dx = 0
dy = 0

physics = PhysicsSystem(sprites)

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
            player.setMovement(dx, dy)

            for component in components:
                for character in characters:
                    componentRef = character.getComponent(component)
                    componentRef.processMessages()
                    messaging.process(character, component)
                    componentRef.update()

            rendering.render()