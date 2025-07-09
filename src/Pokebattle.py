from cmu_graphics import *
from PokemonCreator import *
from assetsUtils import assetPath
from RLenvironment import *
from OpponentAI import *
from trainor import *


#Enters battle with opponent
def enterBattle(app, opponent):
    urlVictory = assetPath('victoryPokemon.mp3')
    app.victorySound = Sound(urlVictory)

    urlDefeat = assetPath('lossSound.wav')
    app.defeatSound = Sound(urlDefeat)
    try:
        app.backgroundMusic.pause()
    except:
        pass
    urlBattle = assetPath('battlePokemon.mp3')
    app.battlePokemonMusic = Sound(urlBattle)
    app.battlePokemonMusic.play(loop=True)

    app.battleState = 'actions'
    app.opponent = opponent
    app.ogOpponentHealth = app.opponent.currentPokemon.health
    
    app.prevPokemonHealth = []
    for pokemon in app.player.pokemon:
        app.prevPokemonHealth.append(pokemon.health)
    
def drawBattle(app):
    drawActionMenu(app, app.actionSelected)
    drawPokemon(app)
    
    
def drawActionMenu(app, selected):
    if app.battleState == 'attacking':
        drawImage(assetPath('battleAttackNone.png'), 0, 0, width = 1250, 
                  height = 750)
        drawAttackMenu(app)
    
    elif app.battleState == 'actions':
        battleSelectList = [assetPath('battleAttackNone.png'), 
                            assetPath('battleAttackSelect.png'),
                            assetPath('battlePokemonSelect.png')]
        drawImage(battleSelectList[selected], 0, 0, width = 1250, height = 750)
        drawLabel('ATTACK', 901, 614, size = 36, font = 'courier',
                  fill = 'black', bold = True)
        drawLabel('POKEMON', 901, 703, size = 36, font = 'courier',
                  fill = 'black', bold = True)
        leftMessage = f'What will {app.player.currentPokemon.name}'
        drawLabel(leftMessage, 189, 630, align = 'left', size = 36, 
                  font = 'courier')
        drawLabel('do next???', 189, 680, align = 'left', size = 36, 
                  font = 'courier')
    
    elif app.battleState == 'pokemonSelect':
        drawImage(assetPath('battleAttackNone.png'), 0, 0, width = 1250, 
                  height = 750)
        drawPokemonSelect(app)
   
    elif (app.battleState == 'playerAttacked' or 
          app.battleState == 'opponentAttacked' or 
          app.battleState == 'victory' or 
          app.battleState == 'defeat' or 
          app.battleState == 'playerPokemonSelected' or
          app.battleState == 'playerCurrentPokemonDied'):
        drawImage(assetPath('battleAttackNone.png'), 0, 0, width = 1250,
                  height = 750)
        drawEvent(app)
    
    elif app.battleState == 'opponent':
        drawImage(assetPath('battleAttackNone.png'), 0, 0, width = 1250, 
                  height = 750)
    
    # Draw health labels
    if app.opponent.currentPokemon:
        drawLabel(f'Health:{app.opponent.currentPokemon.health}', 375, 150, 
                  font = 'courier', size = 24)
        drawLabel(f'{app.opponent.currentPokemon.name}', 255, 150,
                  font = 'courier', size = 24, align = 'right')
    
    if app.player.currentPokemon:
        drawLabel(f'Health:{app.player.currentPokemon.health}', 1120, 486, 
                  font = 'courier', size = 24)
        drawLabel(f'{app.player.currentPokemon.name}', 1000, 486,
                  font = 'courier', size = 24, align = 'right')

def drawAttackMenu(app):
    drawImage(assetPath('attackMenu.png'), 0, 565, width = app.width, 
              height = 750 - 565)
    drawRect(1005, 566, 1250 - 1005, 750 - 566, fill = 'black')
    drawImage(assetPath('PokeBallSprite.png'),1128 ,670, width = 275,
              height = 275, align = 'center')
    drawLine(0,565,app.width,565, lineWidth = 8)
    for move in app.player.currentPokemon.moves:
        moveIndex = app.player.currentPokemon.moves.index(move)
        if moveIndex == app.actionSelected: color = 'white'
        else: color = 'black'
        
        if moveIndex == 0:
            drawLabel(move.name, 242, 605, size = 24, font = 'courier', 
                      fill = color)
        elif moveIndex == 1:
            drawLabel(move.name, 748, 604, size = 24, font = 'courier', 
                      fill = color)
        elif moveIndex == 2:
            drawLabel(move.name, 240, 708, size = 24, font = 'courier', 
                      fill = color)
        elif moveIndex == 3:
            drawLabel(move.name, 751, 706, size = 24, font = 'courier', 
                      fill = color)
            
def drawPokemonSelect(app):
    drawImage(assetPath('attackMenu.png'), 0, 565, width = app.width, 
              height = 750 - 565)
    drawLine(0,565,app.width,565, lineWidth = 8)
    for pokemon in app.player.pokemon:
        pokemonIndex = app.player.pokemon.index(pokemon)
        if pokemonIndex == app.actionSelected: color = 'white'
        else: color = 'black'
        
        if pokemonIndex == 0:
            drawLabel(pokemon.name, 242, 605, size = 24, font = 'courier', 
                      fill = color)
        elif pokemonIndex == 1:
            drawLabel(pokemon.name, 748, 604, size = 24, font = 'courier', 
                      fill = color)
        elif pokemonIndex == 2:
            drawLabel(pokemon.name, 240, 708, size = 24, font = 'courier', 
                      fill = color)
        elif pokemonIndex == 3:
            drawLabel(pokemon.name, 751, 706, size = 24, font = 'courier', 
                      fill = color)

def drawEvent(app):
    if app.battleState == 'playerAttacked':
        drawImage(assetPath('eventPopup.png'), 0, 565, width = app.width, 
              height = 750 - 565)
        moveUsed = app.player.currentPokemon.moves[app.actionSelected].name
        message = f'{app.player.currentPokemon.name} used {moveUsed}!'
        if app.moveMissed:
            missMessage = '...it missed!!!'
            drawLabel(missMessage, 100, 676, align = 'left-top', 
                      fill = 'white', font = 'courier', size = 36)
        drawLabel(message, 100, 600, align = 'left-top', fill = 'white', 
                  font = 'courier', size = 36)
        
    
    elif app.battleState == 'opponentAttacked':
        drawImage(assetPath('eventPopup.png'), 0, 565, width = app.width, 
              height = 750 - 565)
        moveUsed = app.opponentMove.name
        message = f'{app.opponent.currentPokemon.name} used {moveUsed}!'
        if app.moveMissed:
            missMessage = '...it missed!!!'
            drawLabel(missMessage, 100, 676, align = 'left-top', 
                      fill = 'white', font = 'courier', size = 36)
        drawLabel(message, 100, 600, align = 'left-top', fill = 'white', 
                  font = 'courier', size = 36)
    
    elif app.battleState == 'victory':
        drawImage(assetPath('eventPopup.png'), 0, 565, width = app.width, 
              height = 750 - 565)
        drawLabel(('You win!'), 100, 600, align = 'left-top', fill = 'white',
                  font = 'courier', size = 36)
        
    
    elif app.battleState == 'defeat':
        drawImage(assetPath('eventPopup.png'), 0, 565, width = app.width, 
              height = 750 - 565)
        drawLabel(('You have been defeated'), 100, 600, align = 'left-top', 
                  fill = 'white', font = 'courier', size = 36)
        
    elif app.battleState == 'playerPokemonSelected':
        drawImage(assetPath('eventPopup.png'), 0, 565, width = app.width, 
              height = 750 - 565)
        message = f'Go {app.player.currentPokemon.name}!!!'
        drawLabel(message, 100, 600, align = 'left-top', 
                  fill = 'white', font = 'courier', size = 36)
        
    elif app.battleState == 'playerCurrentPokemonDied':
        drawImage(assetPath('eventPopup.png'), 0, 565, width = app.width, 
              height = 750 - 565)
        message = f'Oh no! Come back {app.player.currentPokemon.name}!'
        drawLabel(message, 100, 600, align = 'left-top', 
                  fill = 'white', font = 'courier', size = 36)

def drawPokemon(app):
    # Check if player has a currentPokemon
    if app.player.currentPokemon is None and app.player.pokemon:
        app.player.currentPokemon = app.player.pokemon[0]
    
    # Check if opponent has a currentPokemon
    if app.opponent.currentPokemon is None and app.opponent.pokemon:
        app.opponent.currentPokemon = app.opponent.pokemon[0]
    
    # Draw player's Pokemon
    if app.player.currentPokemon.health <= 0:
        if app.player.currentPokemon:
            drawImage(app.player.currentPokemon.sprite, 225, 500, width = 128, 
                    height = 128, align = 'center', opacity = 30)
    else:
        if app.player.currentPokemon:
            drawImage(app.player.currentPokemon.sprite, 225, 500, width = 128, 
                    height = 128, align = 'center')
    
    # Draw opponent's Pokemon
    if app.opponent.currentPokemon:
        if app.opponent.currentPokemon.health <= 0:
            drawImage(app.opponent.currentPokemon.sprite, 978, 250, width = 256, 
                    height = 256, align = 'center', opacity = 30)
        else:
            drawImage(app.opponent.currentPokemon.sprite, 978, 250, width = 256, 
                    height = 256, align = 'center')
            
def battleMouseMove(app, mouseX, mouseY):
    if app.battleState == 'actions':
        if ((764 <= mouseX <= 1047) and (575 <= mouseY <= 652)):
            app.actionSelected = 1
        elif ((764 <= mouseX <= 1047) and (666 <= mouseY <= 743)):
            app.actionSelected = 2
        else:
            app.actionSelected = 0 
    elif app.battleState == 'attacking':
        if ((0 <= mouseX <= 486) and (570 <= mouseY <= 649)):
            app.actionSelected = 0
        elif ((493 <= mouseX <= 1000) and (570 <= mouseY <= 650)):
            app.actionSelected = 1
        elif ((0 <= mouseX <= 487) and (654 <= mouseY <= 750)):
            app.actionSelected = 2
        elif ((492 <= mouseX <= 1000) and (654 <= mouseY <= 750)):
            app.actionSelected = 3
        else:
            app.actionSelected = None
    elif app.battleState == 'pokemonSelect':
        if ((0 <= mouseX <= 486) and (570 <= mouseY <= 649)):
            app.actionSelected = 0
        elif ((493 <= mouseX <= 1000) and (570 <= mouseY <= 650)):
            app.actionSelected = 1
        elif ((0 <= mouseX <= 487) and (654 <= mouseY <= 750)):
            app.actionSelected = 2
        elif ((492 <= mouseX <= 1000) and (654 <= mouseY <= 750)):
            app.actionSelected = 3
        else:
            app.actionSelected = None
            
def battleMousePress(app, mouseX, mouseY):
    if app.battleState == 'actions':
        if app.actionSelected == 1:
            app.battleState = 'attacking'
            app.actionSelected = None
        elif app.actionSelected == 2:
            app.battleState = 'pokemonSelect'
            app.actionSelected = None
    elif app.battleState == 'attacking':
        moveIndex = app.actionSelected
        if ((moveIndex != None) and 
            (moveIndex < len(app.player.currentPokemon.moves))):
            
            prevHealth = app.opponent.currentPokemon.health
            move = app.player.currentPokemon.moves[moveIndex]
            
            (move.makeMove(app.player.currentPokemon, 
                            app.opponent.currentPokemon))
            
            newHealth = app.opponent.currentPokemon.health
            if (move.target == True and move.damage != 0 and 
                newHealth == prevHealth):
                app.moveMissed = True
            else:
                app.moveMissed = False
            
            app.battleState = 'playerAttacked'
            app.stepsTaken = 0

    elif app.battleState == 'pokemonSelect':
        pokemonIndex = app.actionSelected
        if ((pokemonIndex != None) and 
            (pokemonIndex < len(app.player.pokemon)) and
            (app.player.pokemon[pokemonIndex] != app.player.currentPokemon) and
            (app.player.pokemon[pokemonIndex].health > 0)):
            
            app.player.currentPokemon.statEffects = []
            app.player.currentPokemon = app.player.pokemon[pokemonIndex]
            app.battleState = 'playerPokemonSelected'
            app.stepsTaken = 0            

def battleTimeStep(app):
    if app.battleState == 'playerAttacked':
        app.stepsTaken += 1
        if app.stepsTaken == 75:
            app.battleState = 'opponent'
            checkVictoryLoss(app)
    
    elif app.battleState == 'opponentAttacked':
        app.stepsTaken += 1
        if app.stepsTaken == 75:
            app.battleState = 'actions'
            checkPokemonDied(app)
            checkVictoryLoss(app)
    
    elif app.battleState == 'playerPokemonSelected':
        app.stepsTaken += 1
        if app.stepsTaken == 75:
            app.battleState = 'opponent'
    
    elif app.battleState == 'opponent':
        opponentMove(app)
        
    elif app.battleState == 'playerCurrentPokemonDied':
        app.stepsTaken += 1
        if app.stepsTaken == 75:
            app.battleState = 'actions'
            forceSwapPokemon(app)
    
    elif app.battleState == 'victory' or app.battleState == 'defeat':
        app.stepsTaken += 1
        if app.stepsTaken == 75:
            app.player.currentPokemon.statEffects = []
            app.opponent.currentPokemon.statEffects = []
            
            
            app.opponent.currentPokemon.health = app.ogOpponentHealth
            
            if app.battleState == 'victory':
                newPokemonGet = copy.deepcopy(app.opponent.currentPokemon)
                app.player.completeListOfPokemon.append(newPokemonGet)
                app.player.level += 1
                app.currentOpponentToFight = getOpponent(app.player)
            
            for i in range(len(app.player.pokemon)):
                app.player.pokemon[i].health = app.prevPokemonHealth[i]
            app.state = 'background'
            try: app.victorySound.pause()
            except: pass
            try: app.defeatSound.pause()
            except:pass
    
def checkVictoryLoss(app):
    app.stepsTaken = 0
    playerPotentiallyLost = True
    for pokemon in app.player.pokemon:
        if pokemon.health > 0:
            playerPotentiallyLost = False
    if playerPotentiallyLost == True:
        app.battleState = 'defeat'
        try: app.battlePokemonMusic.pause()
        except: pass
        app.defeatSound.play()
        return
    
    playerPotentiallyWon = True
    if isinstance(app.opponent, Trainor):
        for pokemon in app.opponent.pokemon:
            if pokemon.health > 0:
                playerPotentiallyWon = False
    else:
        if app.opponent.health > 0:
            playerPotentiallyWon = False
    if playerPotentiallyWon == True:
        app.battleState = 'victory'
        try: app.battlePokemonMusic.pause()
        except: pass
        app.victorySound.play()
        return
    
def checkPokemonDied(app):
    if app.player.currentPokemon.health <= 0:
        app.battleState = 'playerCurrentPokemonDied'
        app.stepsTaken = 0
    return

def forceSwapPokemon(app):
    app.player.currentPokemon.statEffects = []
    for pokemon in app.player.pokemon:
        if pokemon.health > 0:
            app.player.currentPokemon = pokemon
            return

def battleKeyPress(app, key):
    if ((key == 'escape') and (app.battleState == 'pokemonSelect' or 
                              app.battleState == 'attacking' or 
                              app.battleState == 'bag')):
        app.battleState = 'actions'
        app.actionSelected = 0
        
def getOpponent(player):
    level = player.level
    return opponentList[level - 1]
    
        
        