from cmu_graphics import *
from welcome import *
from background import *
from Pokebattle import *
from PokemonCreator import *
from userName import *
import PIL.Image as PILImage  # needed to change the import to avoid conflicts
from assetsUtils import assetPath
import time
import cv2 
import os
import tempfile
import copy

def onAppStart(app):
    setupBackground(app)
    setupTrainor(app)
    resetApp(app)

def resetApp(app):
#welcome page stuff
    app.welcomePage = assetPath('welcomePage.png')
    app.name = ''
    app.getUserImageScreen = False #is the user uploading their image so we can 
    #use it for the sprite
    app.nameInput = ''  # Store the current text input
    app.nameInputActive = False  # is name input field is active
    app.cameraActive = False  # is camera active
    app.camera = None  # camera
    app.cameraFrame = None  #current camera frame
    app.captureReady = False  # is camera ready to capture
    app.templateSelection = 0  # which template is currently selected
    app.helpOpen = False
    openingSong = assetPath('iPlayPokemonGo.mp3')
    app.iPlayPokemonGo = Sound(openingSong)

    backgroundMusic = assetPath('openWorld.mp3')
    app.backgroundMusic = Sound(backgroundMusic)

    app.drawPreCamera = False


#other stuff
    app.state = 'welcome'
    app.actionSelected = 0
    app.currentOpponentToFight = opponentOne
    app.pokeTeamBuildMenu = False
    app.battleState = 'actions'
    app.selectedTeammate = None

    app.height = 750
    app.width = 1250

    #app.pressedRestart = False    add restart functionality later
    
    pokeList = [copy.deepcopy(kimchee)]
    app.player = Trainor(None, assetPath('Trainor.png'), pokeList)

#Storing template trainer paths, this'll be used to animate later
    app.templateTrainorPaths = [
        assetPath('Trainor.png'),
        assetPath('Trainor1.png'),
        assetPath('Trainor2.png')
    ]

#Starting point of trainor
    app.cx, app.cy = getCoords(app, app.rows//2, app.cols//2)


def redrawAll(app):
    #welcome page
    if app.state == 'welcome':
        if app.helpOpen:
            drawHelp(app)
        else:
            drawImage(app.welcomePage, app.width/2, app.height/2, 
                      align='center')
        app.iPlayPokemonGo.play()
    
    elif app.state == 'input name':
        # Show a simple text input field
        drawRect(0, 0, app.width, app.height, fill='white')
        drawLabel("Enter your name:", app.width/2, app.height/2 - 50, size=30, 
                  fill='blue', bold=True)
        
        # Draw the input field
        drawRect(app.width/2, app.height/2, 300, 40, fill='lightGray', 
                 align='center')
        drawLabel(app.nameInput, app.width/2, app.height/2, size=20, 
                  fill='black')
        
        # Draw a blinking cursor if the input field is active
        #this doens't rlly work well but fix later
        if app.nameInputActive and int(time.time() * 2) % 2 == 0:
            # Calculate the width of the text to position the cursor
            textWidth = len(app.nameInput) * 5  # Approximate width
            drawLine(app.width/2 + textWidth, app.height/2 - 10, 
                    app.width/2 + textWidth, app.height/2 + 10, 
                    fill='black', lineWidth=2)
        
        drawLabel("Press Enter to confirm", app.width/2, app.height/2 + 50, 
                  size=16)
    
    elif app.getUserImageScreen:
        # Draw the camera screen
        drawRect(0, 0, app.width, app.height, fill='white')
        
        if app.cameraActive:
            if app.cameraFrame is not None:
                # cameera takes pic in opposite color, so this convergts ir bac
                rgbFrame = cv2.cvtColor(app.cameraFrame, cv2.COLOR_BGR2RGB)
                # save picture to a temporary file
                tempPath = os.path.join(tempfile.gettempdir(),
                                         "camera_frame.png")
                cv2.imwrite(tempPath, rgbFrame)
                # Draw picture
                drawImage(tempPath, app.width/2, app.height/2, 
                          width=640, height=480, align='center')
            
            #instructions
            drawLabel("Press SPACE to take a photo", app.width/2, 
                      app.height - 100, size=20, bold=True)
    
    elif app.drawPreCamera:
        preCameraImage = assetPath('precamera.png')
        drawImage(preCameraImage, app.width/2, app.height/2, align='center')

    elif app.state == 'battle':
        drawBattle(app)

    elif app.state == 'background':
        app.iPlayPokemonGo.pause()
        app.backgroundMusic.play()
        drawBackground(app)
        drawTrainor(app)
        if app.pokeTeamBuildMenu:
            drawTeamBuildMenu(app)

    
    
def overlay(userFacePath, templateTrainorPath, spriteType='standing'):
    face = PILImage.open(userFacePath).resize((56, 40)) 

    template = PILImage.open(templateTrainorPath)
    facePosition = (6, 5) 

    result = template.copy()
    result.paste(face, facePosition)

    # Use different file paths for different sprite types
    if spriteType == 'standing':
        customTrainorPath = assetPath('customTrainer1.png')
    elif spriteType == 'walking1':
        customTrainorPath = assetPath('customTrainer2.png')
    elif spriteType == 'walking2':
        customTrainorPath = assetPath('customTrainer3.png')
    else:
        customTrainorPath = assetPath('customTrainer1.png')
        
    result.save(customTrainorPath)

    return customTrainorPath


def onKeyPress(app, key):
    if app.state == 'welcome':
        welcomeKeyPress(app, key)
    if app.state == 'battle':
        battleKeyPress(app, key)
    if app.state == 'input name' and app.nameInputActive:
        if key == 'enter':
            # Confirm the name
            if app.nameInput.strip() != '':
                app.name = app.nameInput.strip()
                app.state = 'precamera'

            else:
                # Use a default name if no input
                app.name = "Player"
            app.state = 'precamera'
            app.drawPreCamera = True


        elif key == 'backspace': 
            app.nameInput = app.nameInput[:-1]
        elif len(key) == 1 and key.isprintable(): 
            # Add the character to the input
            app.nameInput += key

    if app.state == 'precamera':
        if key == 'y':
            app.state = 'camera'
        elif key == 'n':
            app.state = 'background'
            app.drawPreCamera = False

    if app.state == 'camera' and not app.getUserImageScreen:
        app.getUserImageScreen = True
        #initialize the camera
        app.camera = cv2.VideoCapture(0) 
            
        if app.camera.isOpened():
            app.cameraActive = True
            print("Camera initialized")
        else:
            app.cameraActive = False
            print("Failed to open camera")

    elif app.getUserImageScreen:
        # if key == 'n':
        #     app.drawPreCamera = False
        #     # Close the camera and go back
        #     #if app.cameraActive and app.camera is not None:
        #     app.state = 'background'
        #     app.camera.release()
        #     app.camera = None
        #     app.cameraActive = False
        #     app.getUserImageScreen = False
            
        if key == 'space' and app.cameraActive:
            app.drawPreCamera = False
            # Take a photo
            if app.camera is not None and app.camera.isOpened():
                ret, frame = app.camera.read()
                if ret:
                    # Save the frame to a temporary file
                    tempPath = os.path.join(tempfile.gettempdir(), 
                                            "captured_photo.png")
                    cv2.imwrite(tempPath, frame)
                    
                    # Create custom sprites for standing and walking by 
                    # overlaying photo
                    # Standing sprite
                    templatePath = app.templateTrainorPaths[0]
                    customStandingPath = overlay(tempPath, templatePath, 
                                                 'standing')
                    
                    # Walking sprite 1
                    templatePath1 = app.templateTrainorPaths[1]
                    customWalkingPath1 = overlay(tempPath, templatePath1, 
                                                 'walking1')
                    
                    # Walking sprite 2
                    templatePath2 = app.templateTrainorPaths[2]
                    customWalkingPath2 = overlay(tempPath, templatePath2, 
                                                 'walking2')
                    
                    # Update all sprite paths with overlaid images
                    app.customSpritePath = customStandingPath
                    app.customWalkingSprite1 = customWalkingPath1
                    app.customWalkingSprite2 = customWalkingPath2
                    app.standingSprite = customStandingPath
                    app.walkSprite1 = customWalkingPath1
                    app.walkSprite2 = customWalkingPath2
                    app.currentSprite = customStandingPath
                    app.player.sprite = customStandingPath
                    app.player.updateSprite(customStandingPath)
                    
                    # Mark that we have a custom sprite
                    app.hasCustomSprite = True
                    
                    # Clean up camera and transition to game world
                    app.camera.release()
                    app.camera = None
                    app.cameraActive = False
                    app.getUserImageScreen = False
                    app.state = 'background'
        
        if not app.player.pokemon:
            app.player.pokemon = [kimchee]
            app.player.currentPokemon = kimchee
            
        enterBattle(app, app.currentOpponentToFight)
    
    elif key == '?':
        resetApp(app)
        
    elif app.state == 'background':
        if key == 'p':
            if app.pokeTeamBuildMenu == False:
                app.player.pokemon = []
            if app.pokeTeamBuildMenu == True:
                if app.player.pokemon == []:
                    pokemonToAdd = app.player.completeListOfPokemon[0]
                    app.player.pokemon.append(pokemonToAdd)
                app.player.currentPokemon = app.player.pokemon[0]
            app.pokeTeamBuildMenu = not app.pokeTeamBuildMenu

def onKeyHold(app, keys):
    if app.state == 'background':
        move(app, keys)

def onKeyRelease(app, key):
    # Only set walking to False if no movement keys are pressed
    if key in ['left', 'right', 'up', 'down']:
        app.walking = False

def onStep(app):
    if app.state == 'background':
        updateSprite(app)
        
        # Update camera frame if active
        if (app.cameraActive and app.camera is not None and 
            app.camera.isOpened()):
            ret, frame = app.camera.read()
            if ret:
                app.cameraFrame = frame          
    else:
        battleTimeStep(app)

def onMousePress(app, mouseX, mouseY):
    if app.state == 'welcome':
        welcomeMousePress(app, mouseX, mouseY)
    elif app.state == 'input name':
        # Check if the input field was clicked
        if (app.width/2 - 150 <= mouseX <= app.width/2 + 150 and 
            app.height/2 - 20 <= mouseY <= app.height/2 + 20):
            app.nameInputActive = True
        else:
            app.nameInputActive = False
    elif app.state == 'battle':
        battleMousePress(app, mouseX, mouseY)
    elif app.state == 'background' and app.pokeTeamBuildMenu:
        if app.selectedTeammate != None and len(app.player.pokemon) <= 4:
            pokemonAdd = app.player.completeListOfPokemon[app.selectedTeammate]
            app.player.pokemon.append(pokemonAdd)

def onMouseMove(app, mouseX, mouseY):
    if app.state == 'welcome':
        welcomeMouseMove(app, mouseX, mouseY)
    elif app.state == 'battle':
        battleMouseMove(app, mouseX, mouseY)
    if app.pokeTeamBuildMenu:
        app.selectedTeammate = getSelectedTeammate(app, mouseX, mouseY)

def getSelectedTeammate(app, mouseX, mouseY):
    for i in range(len(app.player.completeListOfPokemon)):
        if (481 <= mouseX <= 756) and (65 + i * 54 <= mouseY <= 110 + i * 54):
            return i
    return None

def inWelcomeRect(app, mouseX, mouseY):
    if ((app.width/2 - app.width/4 <= mouseX <= app.width/2 + app.width/4)
        and (app.height/2 - app.height/4 <= mouseY <= app.height/2 + 
             app.height/4)):
        return True
    return False

def updateSprite(app):
    # only update sprite if we're not in battle 
    if app.state == 'background':
        # Call the updateSprite function from trainor.py
        from trainor import updateSprite as trainorUpdateSprite
        trainorUpdateSprite(app)
        
def move(app, keys):
    dx, dy = 0, 0

    # Check if any movement key is pressed
    movementKeys = ['left', 'right', 'up', 'down']
    hasMovement = any(key in keys for key in movementKeys)
    
    if hasMovement:
        app.walking = True
        
        if 'right' in keys:
            dx = 7
        elif 'left' in keys:
            dx = -7
        if 'up' in keys:
            dy = -7
        elif 'down' in keys:
            dy = 7
    else:
        app.walking = False

    makeMove(app, dx, dy)


def main():
    runApp()

main()