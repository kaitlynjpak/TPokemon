import random
from qtables import *
from qLearning import *
from RLenvironment import *
import json
import ast
from qtablesUtils import *

#ChatGPT function used to load the q table given the opponent pokemon and the 
#player pokemon
def loadQtable(pokemon1, pokemon2):
    filename = f"{pokemon1}_vs_{pokemon2}.json"
    filepath = qtablePath(filename)

    with open(filepath, 'r') as f:
        rawQtable = json.load(f)
    
    parsedQtable = {ast.literal_eval(k): v for k, v in rawQtable.items()}
    return parsedQtable


def opponentMove(app):
    opponentPokemon = app.opponent.currentPokemon
    playerPokemon = app.player.currentPokemon

    
    qtable = loadQtable(opponentPokemon.name, playerPokemon.name)
    
    healthState = getOpponentState(app)
    
    stateToSearchFor = (healthState, 0)
    for state in qtable:
        if state == stateToSearchFor:
            qList = []
            for i in range(len(opponentPokemon.moves)):
                stateKey = ((healthState), i)
                qList.append(qtable.get(stateKey))
            
            maxQ = -1000000000
            bestMoveIndex = None
            for i in range(len(qList)):
                if qList[i] > maxQ:
                    bestMoveIndex = i
                    maxQ = qList[i]
            
            app.opponentMove = opponentPokemon.moves[bestMoveIndex]
            
            prevHealth = playerPokemon.health
            app.opponentMove.makeMove(opponentPokemon, playerPokemon)
            newHealth = playerPokemon.health
            
            if (app.opponentMove.target == True and app.opponentMove.damage != 0 
                and prevHealth == newHealth):
                app.moveMissed = True
            else:
                app.moveMissed = False
                
            app.stepsTaken = 0
            app.battleState = 'opponentAttacked'
            return
    #If exact state isn't found, approximate state is searched for +-10%:
    for state in qtable:
        opponentHealth = healthState[0]
        playerHealth = healthState[1]
        diff1 = abs(opponentHealth - state[0][0])
        diff2 = abs(playerHealth - state[0][1])
        
        if diff1 <= 0.1 and diff2 <= 0.1:
            qList = []
            for i in range(len(opponentPokemon.moves)):
                stateKey = ((state[0]), i)
                qList.append(qtable.get(stateKey))
                
            maxQ = -1000000000
            bestMoveIndex = None
            for i in range(len(qList)):
                if qList[i] > maxQ:
                    bestMoveIndex = i
                    maxQ = qList[i]
            
            prevHealth = playerPokemon.health
            app.opponentMove = opponentPokemon.moves[bestMoveIndex]
            app.opponentMove.makeMove(opponentPokemon, playerPokemon)
            newHealth = playerPokemon.health
            
            if (app.opponentMove.target == True and app.opponentMove.damage != 0 
                and prevHealth == newHealth):
                app.moveMissed = True
            else:
                app.moveMissed = False
            
            app.stepsTaken = 0
            app.battleState = 'opponentAttacked'
            return
    #If no approximate state is found, opponent uses random move
    upperBound = len(app.opponent.currentPokemon.moves) - 1
    moveIndex = random.randint(0, upperBound)
    app.opponentMove = opponentPokemon.moves[moveIndex]
    
    prevHealth = playerPokemon.health
    app.opponentMove.makeMove(opponentPokemon, 
                              playerPokemon)
    newHealth = playerPokemon.health
    
    if (app.opponentMove.target == True and app.opponentMove.damage != 0 
        and prevHealth == newHealth):
        app.moveMissed = True
    else:
        app.moveMissed = False
    
    app.stepsTaken = 0
    app.battleState = 'opponentAttacked'

            
def getOpponentState(app):
    oppHealth = app.opponent.currentPokemon.health
    playerHealth = app.player.currentPokemon.health
    
    return (oppHealth / 250, playerHealth / 250)
    
    
    

    
    
    


