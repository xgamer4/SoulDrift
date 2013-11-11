from pygame import sprite
import math
import random


### List of Components
# 1) AI Component - Actions taken by the entity
# 2) Stat Component - HP, Strength, etc
# 3) Inventory Component - Carried equipment
# 4) Ability Components - 0+ components that determine special abilities (breath fire, etc)
# 5) Interact Component - Describes the behavior when one entity interacts with a second
# 6) Overlap Component - Describes the behavior when two entities overlap
# MAY BE ADDED AS NEED ARISES
### 

class Entity(sprite.Sprite):
    entityTotal = 0
    
    def __init__(self, logger):
        self.startup(logger)
        
    def __init__(self, logger, image, rect):
        self.startup(logger)
        self.image = image
        self.rect = rect
        
    def startup(self, logger):
        sprite.Sprite.__init__(self)
        Entity.entityTotal = Entity.entityTotal + 1
        self.ID = Entity.entityTotal
        
        self.logger = logger
        
        self.components = {}   
        self.components[AbilityComponent.name] = {}
        self.abilityIDs = []
        
        self.dx = 0
        self.dy = 0           
        
    def updateComponent(self, key, component):
        if key == AbilityComponent.name:
            for replace in component.replaceIDs:
                if replace in abilityIDs:
                    self.abilityIDs.remove(replace)
                    del self.components[AbilityComponent.name][replace]
            self.components[key][component.ID] = component
        else:
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
        
    def logMessage(self, message):
        self.logger.messageLog.append(message)


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
        
        
class CollisionComponent(Component):
    
    name = "collision"
    
    def __init__(self):
        Component.__init__(self, CollisionComponent.name)
        self.passthrough = False
        self.react = True
        
    def collide(self, colliderEntity):
        raise NotImplementedError()
    
class StatComponent(Component):
    
    name = "stat"
    
    def __init__(self):
        self.stats = {}
        self.stats["HP"] = 10
        self.stats["Max HP"] = 10
        self.stats["Strength"] = 2
        self.stats["Defense"] = 1
        

class AbilityComponent:
    
    name = "ability"
    
    def __init__(self):
        self.ID = 0