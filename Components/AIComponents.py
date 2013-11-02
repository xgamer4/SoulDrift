from BaseComponents import AIComponent

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
    