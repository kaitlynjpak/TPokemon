from cmu_graphics import *
# from background import *
from assetsUtils import assetPath
from PokemonCreator import *
import copy

class Trainor:
    def __init__(self, name, sprite, pokemon):
        self.name = name
        self.sprite = sprite
        self.completeListOfPokemon = copy.deepcopy(pokemon)
        self.pokemon = pokemon
        self.currentPokemon = pokemon[0] if pokemon else None
        self.level = 1

    def updateSprite(self, newSpritePath):
        self.sprite = newSpritePath

def setupTrainor(app):
    # Initialize sprite images
    app.standingSprite = assetPath('Trainor.png')
    app.walkSprite1 = assetPath('Trainor1.png')
    app.walkSprite2 = assetPath('Trainor2.png')
    app.currentSprite = app.standingSprite

    # Initialize animation variables
    app.walking = False
    app.currentFrame = 1
    app.stepCounter = 0
    app.stepsPerSecond = 30

    # Position
    # app.cx, app.cy = getCoords(app, app.rows//2, app.cols//2)

    if hasattr(app, 'customSpritePath') and app.customSpritePath: #this 
        #was chatgpt's solution to making sure a custom sprite is actually made
        app.standingSprite = app.customSpritePath
        app.currentSprite = app.standingSprite

def redrawAll(app):
    drawImage(app.currentSprite, app.cx, app.cy, align='center')

# def move(app, keys):
#     dx, dy = 0, 0

#     # Check if any movement key is pressed
#     movementKeys = ['left', 'right', 'up', 'down']
#     hasMovement = any(key in keys for key in movementKeys)
    
#     if hasMovement:
#         app.walking = True
        
#         if 'right' in keys:
#             dx = 7
#         elif 'left' in keys:
#             dx = -7
#         if 'up' in keys:
#             dy = -7
#         elif 'down' in keys:
#             dy = 7
#     else:
#         app.walking = False

#     makeMove(app, dx, dy)
    # newX, newY = app.cx + dx, app.cy + dy
    # newTileCoords = getTile(app, newX, newY)
    
    # if newTileCoords != None:
    #     newRow, newCol = newTileCoords
    #     newTile = board[newRow][newCol]
    #     makeMove(app, newTile, newRow, newCol, dx, dy)


def updateSprite(app):
    if app.walking:
        app.stepCounter += 1
        if app.stepCounter >= app.stepsPerSecond / 5: 
            takeStep(app)
            app.stepCounter = 0  # Reset counter after taking a step
    else:
        app.currentSprite = app.standingSprite
        app.currentFrame = 1

def takeStep(app):
    if app.currentFrame == 1:
        # Use custom walking sprite if available
        if (hasattr(app, 'hasCustomSprite') and app.hasCustomSprite and 
            hasattr(app, 'customWalkingSprite1')):
            app.currentSprite = app.customWalkingSprite1
        else:
            app.currentSprite = app.walkSprite1
        app.currentFrame = 2
    else:
        # Use custom walking sprite if available
        if (hasattr(app, 'hasCustomSprite') and app.hasCustomSprite and 
            hasattr(app, 'customWalkingSprite2')):
            app.currentSprite = app.customWalkingSprite2
        else:
            app.currentSprite = app.walkSprite2
        app.currentFrame = 1

def drawTrainor(app):
    if app.currBackgroundState == 'world':
        drawImage(app.currentSprite, app.width//2, app.height//2, 
                  align='center')
    elif app.currBackgroundState == 'gym':
        drawImage(app.currentSprite, app.gymX, app.gymY, 
                  align='center')
        