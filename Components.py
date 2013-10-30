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

class Entity:
    entityTotal = 0
    
    def __init__(self):
        Entity.entityTotal = Entity.entityTotal + 1
        self.ID = Entity.entityTotal
        
        self.components = {}
        
    def updateComponent(self, key, component):
        self.components[key] = component
        
    def deleteComponent(self, key):
        del self.components[key]
        
    def getComponent(self, key):
        return self.components[key]


class Component:
    
    def __init__(self):
        self.outgoing = []
        self.incoming = []
        # the "scratch variables"
        self.vars = {}

    def queueMessage(self, recipient, message):
        self.outgoing.append( (recipient, message) )

    def sendMessages(self):
        return self.outgoing
        self.outgoing.clear()

    def receiveMessage(self, sender, message):
        self.incoming.append( (sender, message) )

    def processMessages(self):
        for sender, message in self.incoming:
            index, key, newVar = message
            if index == 2:
                self.vars[key] = newVar
            elif index == 3:
                self.queueMessage(sender, (4, key, self.vars[var]))

    #The function that does any processing needed for the component
    def update(self):
        raise NotImplementedError()
        
class RenderableComponent(Component, pygame.sprite.Sprite):

    def baseUpdate(self):
        if self.rect.top + self.vars["dy"] <= 0:
            self.vars["dy"] = 0
        if self.rect.left + self.vars["dx"] <= 0:
            self.vars["dx"] = 0
        if self.rect.right + self.vars["dx"] >= 800:
            self.vars["dx"] = 0
        if self.rect.bottom + self.vars["dy"] >= 600 :
            self.vars["dy"] = 0

        self.rect.move_ip(self.vars["dx"], self.vars["dy"])

    
    def __init__(self, image, rect):
        Component.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        #A pygame.Rect object holding the size and location of the sprite
        self.rect = rect
        #A pygame.Surface object holding the actual sprite/tile 
        self.image = image

        self.vars["dx"] = 0
        self.vars["dy"] = 0

        self.update = self.baseUpdate

    def processMessages(self):
        for sender, message in self.incoming:
            index, key, newVar = message
            if index == 1:
                if key == "update":
                    self.update = newVar
            if index == 2:
                self.vars[key] = newVar
            elif index == 3:
                self.queueMessage(sender, (4, key, self.vars[var]))
                        

class AIComponent(Component):
    
    def __init__(self):
        Component.__init__(self)
        self.vars["dx"] = 0
        self.vars["dy"] = 0

    def update(self):
        value = math.ceil(random.random()*4) % 4
        print value
        if value == 0:
            self.vars["dx"] = -16
            self.vars["dy"] = 0
        elif value == 1:
            self.vars["dx"] = 16
            self.vars["dy"] = 0
        elif value == 2:
            self.vars["dx"] = 0
            self.vars["dy"] = -16
        else:
            self.vars["dx"] = 0
            self.vars["dy"] = 16
        self.movement()
        

    def movement(self):
        self.queueMessage("render", (2, "dx", self.vars["dx"]))
        self.queueMessage("render", (2, "dy", self.vars["dy"]))


class PlayerAIComponent(AIComponent):
    
    def __init__(self, playerEntity):
        AIComponent.__init__(self)
        self.playerEntity = playerEntity

    def setMovement(self, dx, dy):
        self.vars["dx"] = dx
        self.vars["dy"] = dy
        self.movement()

    def update(self):
        return None

class MonsterAIComponent(AIComponent):
    
    def __init__(self):
        AIComponent.__init__(self)
        
    def update(self):
        value = math.ceil(random.random()*4) % 4
        if value == 0:
            self.vars["dx"] = -16
            self.vars["dy"] = 0
        elif value == 1:
            self.vars["dx"] = 16
            self.vars["dy"] = 0
        elif value == 2:
            self.vars["dx"] = 0
            self.vars["dy"] = -16
        elif value == 3:
            self.vars["dx"] = 0
            self.vars["dx"] = 16
    
        