import pygame
import math
import random

########################
### MESSAGING FORMAT ###
###   (TENTATIVE)    ###
########################

### Tuple
# Index 0: Instruction (int)
#     Value 1: Update component-level variable (update function, etc)
#     Value 2: Update scratch-variables (dict containing variables that can be edit/set by messages)
#     Value 3: Request for information (send a message containing contents of requested variable; currently only supports requests for scratch-variables)
#  Value 4: Response to request
# Index 1: Name of variable to be updated (1,2), sent (3), or received (4)
# Index 2: Value to set variable to (1,2), value is set to (4), or ignore (3)
###


### List of Components
# 1) Renderable Component - individual sprite/image and location
# 2) AI Component - Actions taken by the entity
# 3) Stat Component - HP, MP, Strength, etc
# 4) Inventory Component - Carried equipment
# 5) Ability Components - 0+ components that determine special abilities (breath fire, etc)
# 6) Interact Component - Describes the behavior when one entity interacts with a second
# 7) Overlap Component - Describes the behavior when two entities overlap
# 8) MAY BE ADDED AS NEED ARISES
### 

class Entity(pygame.sprite.Sprite):
    entityTotal = 0
    
    def __init__(self):
        self.startup()
        
    def __init__(self, image, rect):
        self.startup()
        self.image = image
        self.rect = rect
        
    def startup(self):
        pygame.sprite.Sprite.__init__(self)
        Entity.entityTotal = Entity.entityTotal + 1
        self.ID = Entity.entityTotal
        
        self.components = {}    
        
        self.dx = 0
        self.dy = 0
           
        
    def updateComponent(self, key, component):
        self.components[key] = component
        component.owner = self
        
    def deleteComponent(self, key):
        del self.components[key]
        
    def getComponent(self, key):
        if key in self.components.keys():
            return self.components[key]
        else:
           return None 
    
    def update(self):
        self.rect.move_ip(self.dx, self.dy)
        
    def undoMove(self):
        self.rect.move_ip(-self.dx, -self.dy)


class Component:
    
    #takes entity currently assigned this component - the "owner"
    def __init__(self, name, entity=None):
        self.name = name
        self.owner = entity
        if self.owner != None:
            self.owner.updateComponents(name, self)


    #The function that does any processing needed for the component
    def update(self):
        raise NotImplementedError()
    
    def assign2owner(self, name, entity):
        entity.updateComponents(name, self)
        self.owner = entity

class AIComponent(Component):
    name = "ai"
    def __init__(self):
        Component.__init__(self, AIComponent.name)
        self.dx = 0
        self.dy = 0

    def update(self):
        value = math.ceil(random.random()*4) % 4
        if value == 0:
            self.dx = -16
            self.dy = 0
        elif value == 1:
            self.dx = 16
            self.dy = 0
        elif value == 2:
            self.dx = 0
            self.dy = -16
        else:
            self.dx = 0
            self.dy = 16
        self.movement()
        

    def movement(self):
        self.owner.dx = self.dx
        self.owner.dy = self.dy


class PlayerAIComponent(AIComponent):
    
    def __init__(self, playerEntity):
        AIComponent.__init__(self)
        self.playerEntity = playerEntity

    def setMovement(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.movement()

    def update(self):
        return None

class MonsterAIComponent(AIComponent):
    
    def __init__(self):
        AIComponent.__init__(self)
        
class CollisionComponent(Component):
    
    name = "collision"
    
    def __init__(self):
        Component.__init__(self, CollisionComponent.name)
        self.passthrough = False
        self.react = True
        
    def collide(self, colliderEntity):
        raise NotImplementedError()
    
class BorderCollisionComponent(CollisionComponent):
    
    def __init__(self):
        CollisionComponent.__init__(self)
        self.react = False
        
    def collide(self, colliderEntity):
        return None

class MonsterCollisionComponent(CollisionComponent):
    
    def __init__(self):
        CollisionComponent.__init__(self)
        
    def collide(self, colliderEntity):
        print str(self.owner.ID) + " Collision!"
    
        