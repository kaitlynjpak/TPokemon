import random

def opponentMove(app): 
    upperBound = len(app.opponent.currentPokemon.moves) - 1
    moveIndex = random.randint(0, upperBound)
    app.opponentMove = app.opponent.currentPokemon.moves[moveIndex]
    app.opponentMove.makeMove(app.opponent, app.player)
    app.stepsTaken = 0
    app.battleState = 'opponentAttacked'


class Environment: #everythign here is to setup simulations

    def __init__(self, attacker, defender): # attacker and defender alternates 
        #depending on the turn
        self.attacker = attacker
        self.defender = defender
        self.originalAttackerHealth = attacker.health
        self.originalDefenderHealth = defender.health
        self.possibleMoves = []
        numMoves = len(attacker.moves)
        for i in range(numMoves): #each pokemon gets 4 moves
            self.possibleMoves.append(i) 
        self.maxTurns = 50  #so we never have an infinite game
        self.turnCount = 0 #what turn ur on rn

        self.prevPlayerHealth = attacker.health # track health from the last r
        self.prevOpponentHealth = defender.health

    def getState(self): 
        p1 = self.attacker
        p2 = self.defender
        return ( #i asked chatgpt here to understand how to get the ai to 
                #incorporate the battle moves
        p1.health / 250,        
        p2.health / 250,      
    )
    
    def onStep(self, battleMove):
        self.prevPlayerHealth = self.attacker.health
        self.prevOpponentHealth = self.defender.health
        
        playerMove = self.attacker.moves[battleMove]
        playerMove.makeMove(self.attacker, self.defender)

        opponentMove = random.choice(self.defender.moves) #we just gong to 
        #select a random move from the possible moves fro now
        opponentMove.makeMove(self.defender, self.attacker) #swaps defense and 
        #offense on each call

        self.turnCount += 1 #move has been made!! 

        done = self.isDone()       
        reward = self.getReward(done) #according to RL docs this is needed to 
        #actually force the RL to learn
        return self.getState(), reward, done  #chatgpt said this is the info 
    #that the RL would need. this is gon reutrn the updated state. i asked chat 
    # how the RL algorithm will actually use this, and apparently it's just 
    # storing the different states with the moves it plays and using that to 
    # learn from

    def isDone(self):
        if (self.attacker.health <= 0 or self.defender.health <= 0 or 
            self.turnCount >= self.maxTurns):
            return True
        return False
    
    def getReward(self, done):
        if done:
            if self.attacker.health <= 0:
                return -100 #bad
            elif self.defender.health <=0:
                return +100  #yayyy reward for the win
            else:
                return 0 #tie or you maxxed out the turnCount
        else: #this is where i started ysing chat in this function. 
            damageToOpponent = self.prevOpponentHealth - self.defender.health
            damageTaken = self.prevPlayerHealth - self.attacker.health
            return damageToOpponent - damageTaken  # higher opponent damage 
        #means higher reward 
   

    def resetBattle(self):
        
        self.attacker.health = self.originalAttackerHealth     
        self.defender.health = self.originalDefenderHealth    

        self.turnCount = 0
        self.prevPlayerHealth = self.attacker.health
        self.prevOpponentHealth = self.defender.health
        return self.getState()
    
    def getWinner(self):
        if self.attacker.health > 0 and self.defender.health <= 0:
            return self.attacker
        elif self.defender.health > 0 and self.attacker.health <= 0:
            return self.defender
        return None