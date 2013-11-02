from BaseComponents import CollisionComponent

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
        #print str(self.owner.ID) + " Collision with " + str(colliderEntity.ID)
        return None