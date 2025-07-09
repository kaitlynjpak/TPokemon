from cmu_graphics import *

def enterWelcome(app):
    app.buttonSelected = None
    app.state = 'welcome'
    app.helpOpen = False

def redrawAll(app):
    #welcome page
    if app.state == 'welcome':
        if app.helpOpen:
            drawHelp(app)
        drawImage(app.welcomePage, app.width/2, app.height/2, align='center')
        app.iPlayPokemonGo.play()

def welcomeMouseMove(app, mouseX, mouseY):
    if app.state == 'welcome':
        if ((550 <= mouseX <= 730) and (668 <= mouseY <= 750)):
            app.buttonSelected = 'start'
        elif ((788 <= mouseX <= 950) and (687 <= mouseY <= 740)):
            app.buttonSelected = 'help'
        else:
            app.buttonSelected = None

def welcomeMousePress(app, mouseX, mouseY):
    if app.buttonSelected == 'start':
        app.state = 'input name'
        app.buttonSelected = None
    elif app.buttonSelected == 'help':
        app.helpOpen = True
        app.buttonSelected = None

def welcomeKeyPress(app, key):
    if (app.helpOpen) and (key == 'escape'):
        resetApp(app)

def drawHelp(app):
    color = gradient('yellow', 'orange', 'red')

    drawRect(app.width/2, app.height/2, app.width/2, app.width/2, 
             align = 'center', fill = color)
    drawLabel('Welcome to TPokemon!', app.width/2, 310, font='orbitron', 
              size=20, align = 'center')
    drawLabel('''In this game, you are a trainer and your job is to catch and 
              battle Pokemon.''', app.width/2, 330, font='orbitron', size=12, 
              align = 'center')
    drawLabel('''To begin, you will be making your trainer by taking
              a photo of yourself. You will be given one pokemon to start.''', 
              app.width/2, 350, font='orbitron', size=12, align = 'center')
    drawLabel('''To collect new pokemon, you will battle the pokemon of other 
              trainers in the gyms on the map.''', app.width/2, 370, 
              font='orbitron', size=12, align = 'center')
    drawLabel('''There are 3 trainers per arena, with the final 
                boss being Kozzymon.''', app.width/2, 390, font='orbitron', 
              size=12, align = 'center')
    drawLabel('As you defeat pokemon, you collect them to your set.', 
              app.width/2, 410, font='orbitron', size=12, align = 'center')
    drawLabel('Click "p" to see your pokemon inventory, and make a team!', 
              app.width/2, 430, font='orbitron', size=12, align='center')
    drawLabel('Use the arrow keys to move around on the map.', app.width/2, 450, 
              font='orbitron', size=12, align = 'center')
    drawLabel('Click "escape" to go back. Carpe Diem :) ps. sound on!!', 
              app.width/2, 470, font='orbitron', size=12, align = 'center')

def resetApp(app):
    app.buttonSelected = None
    app.state = 'welcome'
    app.helpOpen = False


def onMouseMove(app, mouseX, mouseY):
    if app.state == 'welcome': 
        welcomeMouseMove(app, mouseX, mouseY)


