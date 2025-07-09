import random

class Pokemon:
    
    def __init__(self, name, maxHealth, moveList, sprite, type, defense, speed, 
                 attack):
        self.name = name
        self.health = maxHealth
        self.moves = moveList
        self.sprite = sprite
        self.type = type
        self.defense = defense
        self.speed = speed
        self.attack = attack
        self.level = 1
        self.statEffects = []
        self.tempAttackMod = 0
        self.tempDefenseMod = 0
        self.tempSpeedMod = 0
        
    def __hash__(self):
        return hash(str(self))
    
class PokeMove:
    
    def __init__(self, name, damage, defenseMod, speedMod, attackMod,
                 accuracy, target):
        self.name = name
        self.damage = damage
        self.defenseMod = defenseMod
        self.speedMod = speedMod
        self.attackMod = attackMod
        self.accuracy = accuracy
        self.target = target
        
    def __hash__(self):
        return hash(str(self.name))
    
    def makeMove(self, attacker, defender):
        if self.target == True:
            if self.moveHitCheck(attacker, defender):
                damage = self.calculateDamage(attacker, defender)
                
                defender.health -= damage
                if ((self.defenseMod != 0) or 
                    (self.speedMod != 0) or (self.attackMod != 0)):
                    self.applyStatus(defender)
        else:
            attacker.health -= self.damage
            
            if ((self.defenseMod != 0) or 
                    (self.speedMod != 0) or (self.attackMod != 0)):
                self.applyStatus(attacker)
        
        PokeMove.calculateTempBuffs(attacker)
        PokeMove.calculateTempBuffs(defender)
    
    def calculateDamage(self, attacker, defender):
        A = attacker.attack + attacker.tempAttackMod
        D = defender.defense + defender.tempDefenseMod
        P = self.damage
        
        damage = int(P * (A/D))
        return damage
        
    def moveHitCheck(self, attacker, defender):
        A = self.accuracy
        dS = defender.speed + defender.tempSpeedMod
        aS = attacker.speed + attacker.tempSpeedMod
        chanceHit = A * (1 + (0.5 * ((aS - dS)/100)))
        
        if chanceHit >= 100:
            return True
        else:
            rollHit = random.randint(0, 99)
            if chanceHit >= rollHit:
                return True
            else:
                return False
    
    def applyStatus(self, target):
        for status in target.statEffects:
            if status.name == self.name:
                if status.counter < 3:
                    status.counter += 1
                return
        statMod = StatEffect(self.name, self.defenseMod, 
                             self.speedMod, self.attackMod)
        target.statEffects.append(statMod)
    
    @staticmethod
    def calculateTempBuffs(target):
        target.tempAttackMod = 0
        target.tempDefenseMod = 0
        target.tempSpeedMod = 0
        
        for status in target.statEffects:
            if status.counter == 1:
                target.tempAttackMod += int(status.attackMod * target.attack)
                target.tempDefenseMod += int(status.defenseMod * target.defense)
                target.tempSpeedMod += int(status.speedMod * target.speed)
            elif status.counter == 2:
                target.tempAttackMod += int(1.5 * 
                                            status.attackMod * target.attack)
                target.tempDefenseMod += int(1.5 * 
                                             status.defenseMod * target.defense)
                target.tempSpeedMod += int(1.5 * 
                                           status.speedMod * target.speed)
            elif status.counter == 3:
                target.tempAttackMod += int(1.75 * 
                                            status.attackMod * target.attack)
                target.tempDefenseMod += int(1.75 * 
                                             status.defenseMod * target.defense)
                target.tempSpeedMod += int(1.75 * 
                                           status.speedMod * target.speed)

class StatEffect:
    def __init__(self, name, defenseMod, speedMod, attackMod):
        self.defenseMod = defenseMod
        self.attackMod = attackMod
        self.speedMod = speedMod
        self.name = name
        self.counter = 1
        
    def __eq__(self, other):
        return (isinstance(other, StatEffect) and self.name == other.name)
    
    def __repr__(self):
        return str(f'Name:{self.name} Count:{self.counter}')
    
class Place:
    def __init__(self, name, corners, inside):
        self.name = name
        self.corners = corners
        self.corner0Row, self.corner0Col = self.corners[0]
        self.corner1Row, self.corner1Col = self.corners[1]
        self.corner2Row, self.corner2Col = self.corners[2]
        self.corner3Row, self.corner3Col = self.corners[3]
        self.inside = inside
        self.entranceRow = self.corner1Row
        self.entranceCol = (self.corner0Col+self.corner2Col)//2

class Texture:
    def __init__(self, name, locations):
        self.name = name # texture type
        self.locations = locations # list of tuples of coordinates

        