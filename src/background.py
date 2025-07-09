from cmu_graphics import *
from assetsUtils import assetPath
import random
from entityClasses import Texture, Place
from Pokebattle import *

def setupBackground(app):
    app.currBackgroundState = 'world'
    app.prevBackgroundState = None
    app.gym = None
    app.width = 1250
    app.height = 750
    app.cellWidth = 125
    app.cellHeight = 125
    app.rows = 35
    app.cols = 50

    app.cx, app.cy = getCoords(app, app.rows//2, app.cols//2)
    app.gymXDefault, app.gymYDefault = app.width//2, app.height - app.cellHeight
    app.gymX, app.gymY = app.gymXDefault, app.gymYDefault
    # app.rows - 2 so that it doesn't automatically enter on the exit tile

    app.board = [['blank']*app.cols for i in range(app.rows)]
    app.rockNum = 60
    app.treeNum = 60
    app.fenceHNum = 40
    app.tRow, app.tCol = app.rows//2, app.cols//2

    # Places setup!!!!!!
    app.corners = {
                    'gym1': [
                                (app.tRow-4, app.tCol-1),
                                (app.tRow-2, app.tCol-1),
                                (app.tRow-4, app.tCol+1),
                                (app.tRow-2, app.tCol+1)
                    ]
    }
    app.placeImages = {
                        'gym1': assetPath('gym1.png')
                       }
    app.placeInsides = {
                        'gym1' : assetPath('gymInside.png')
                        }
    app.places=[
                Place('gym1', app.corners['gym1'], app.placeInsides['gym1'])
    ]

    # Background setup!!!!!!!!!!!
    app.obstacleLocations = set()
    app.noObstacles = {
                        (app.tRow, app.tCol),
                        (app.tRow - 2, app.tCol - 1),
                        (app.tRow - 2, app.tCol + 1)
                      }
    app.locations = {
                        'grass1Grass':{(i,j) for i in range(app.rows) 
                                        for j in range(app.cols)},
                        'grass1Rock':randomObstacle(app, app.rockNum),
                        'grass1Sand':generateSand(app, 3),
                        'grass1Tree':randomObstacle(app, app.treeNum),
                        'grass1FenceH':randomObstacle(app, app.fenceHNum),
                        'grass2Grass':{(1,13), (6,9), (14,7)},
                        'grass2Rock':{(i,j) for i in range(app.rows)
                                        for j in range(app.cols)}
                    }
    app.backgrounds = {
                        'grass1':[
                                Texture('rock',
                                        app.locations['grass1Rock']),
                                Texture('grass', 
                                        app.locations['grass1Grass']-
                                        app.locations['grass1Rock']-
                                        app.locations['grass1Tree']-
                                        app.locations['grass1FenceH']),
                                Texture('sand',
                                        app.locations['grass1Sand']),
                                Texture('tree',
                                        app.locations['grass1Tree']),
                                Texture('fenceH',
                                        app.locations['grass1FenceH'])
                                ]
                        }
    app.obstacles = {'rock', 'tree', 'fence'}
    app.backgroundList = app.backgrounds['grass1']
    app.textures = {'blank': assetPath('blank.jpg'),
                    'grass': assetPath('grass.jpg'), 
                    'rock': assetPath('rock1.jpg'),
                    'sand': assetPath('sand.jpg'),
                    'fenceH': assetPath('fenceHorizontal.jpg'),
                    'fenceV': assetPath('fenceVertical.jpg'),
                    'tree': assetPath('tree.jpg')}
    
    editBoard(app, app.backgroundList)

def editBoard(app, background):
    for texture in background:
        for (row, col) in texture.locations:
            app.board[row][col] = texture.name

def drawBoard(app):
    tRow, tCol = getTile(app, app.cx, app.cy)
    halfCols = (app.width // app.cellWidth) // 2 + 1
    halfRows = (app.height // app.cellHeight) // 2 + 1
    leftCol = max(tCol - halfCols, 0)
    rightCol = min(tCol + halfCols, app.cols)
    topRow = max(tRow - halfRows, 0)
    bottomRow = min(tRow + halfRows, app.rows)
    
    for row in range(topRow, bottomRow + 1):
        for col in range(leftCol, rightCol + 1):
            texture = app.board[row][col]
            drawTexture(app, texture, row, col)

def drawTexture(app, texture, row, col):
    url = app.textures[texture]
    leftOffset = app.cx - app.width//2 # app.cx, app.cy imported from trainor
    topOffset = app.cy - app.height//2
    left = col * app.cellWidth - leftOffset
    top = row * app.cellHeight - topOffset
    drawImage(url, left, top, width=app.cellWidth, height=app.cellHeight)

def getTile(app, x, y): #helped generate with chatgpt
    col = int(x // app.cellWidth)
    row = int(y // app.cellHeight)
    if ((0 <= row < app.rows) and (0 <= col < app.cols)):
        return row, col
    else:
        return None
    
def visible(app, boardRow, boardCol, cx, cy):
    trainorRow, trainorCol = getTile(app, cx, cy)
    drow = boardRow - trainorRow
    dcol = boardCol -trainorCol
    return ((-app.rows//2 <= drow <= app.rows//2) and
            (-app.cols//2 <= dcol <= app.cols//2))

def getCoords(app, row, col):
    xCoord = col * app.cellWidth + app.cellWidth//2
    yCoord = row * app.cellHeight + app.cellHeight//2
    return xCoord, yCoord

def randomObstacle(app, num):
    count = 0
    obstacles = set()
    while count < num:
        randRow = random.randint(0, app.rows-1)
        randCol = random.randint(0, app.cols-1)
        coords = (randRow, randCol)
        if (coords not in obstacles) and canHaveObstacle(coords):
            obstacles.add(coords)
            count += 1
    app.obstacleLocations = app.obstacleLocations | obstacles
    print(f"Generated {len(obstacles)} obstacles!")
    return obstacles

def canHaveObstacle(coords):
    row, col = coords
    for item in app.noObstacles:
        itemRow, itemCol = item
        drow = itemRow - row
        dcol = itemCol - col
        for crow in range(-1, 2):
            for ccol in range(-1, 2):
                if (drow, dcol) == (crow, ccol):
                    return False
    for place in app.places:
        for prow in range(place.corner0Row-1, place.corner1Row+2):
            for pcol in range(place.corner0Col-1, place.corner2Col+2):
                if (row, col) == (prow, pcol):
                    return False
    if coords in app.obstacleLocations:
        return False
    return True

def generateSand(app, pathLength):
    sand = set()
    for place in app.places:
        for i in range(pathLength):
            sand.add((place.entranceRow + 1 + i, place.entranceCol))
    return sand

def drawPlaces(app):
    for place in app.places:
        url = app.placeImages[place.name]
        leftOffset = app.cx - app.width//2
        topOffset = app.cy - app.height//2
        left = place.corner0Col * app.cellWidth - leftOffset
        top = place.corner0Row * app.cellHeight - topOffset
        right = (place.corner3Col+1) * app.cellWidth - leftOffset
        bottom = (place.corner3Row+1) * app.cellHeight - topOffset
        placeHeight = bottom - top
        placeWidth = right - left
        drawImage(url, left, top, width=placeWidth, height=placeHeight)

def makeMove(app, dx, dy):
    if app.currBackgroundState == 'world':
        newX, newY = app.cx + dx, app.cy + dy
        newTileCoords = getTile(app, newX, newY)
        
        if newTileCoords != None:
            newRow, newCol = newTileCoords
            newTile = app.board[newRow][newCol]
        if (newRow<0 or newRow > app.rows) or (newCol < 0 or newCol > app.cols):
            return
        if newTile in app.obstacles:
            return
        for place in app.places:
            if ((place.corner0Row <= newRow <= place.corner3Row) and
                (place.corner0Col <= newCol <= place.corner3Col)):
                if (newRow, newCol) != (place.entranceRow, place.entranceCol):
                    return
        app.cx, app.cy = app.cx + dx, app.cy + dy
    elif app.currBackgroundState == 'gym':
        newX, newY = app.gymX + dx, app.gymY + dy
        if canMoveInGym(app, newX, newY):
            app.gymX, app.gymY = app.gymX + dx, app.gymY + dy
    changeBackground(app)
    # return True

def canMoveInGym(app, newX, newY):
    left = 366
    right = 884
    top = 184
    bottom = 716
    if ((newX < left or newX > right) or
        (newY < top or newY > bottom)):
        return False
    return True
    
def checkInWhichPlace(app, row, col):
    for place in app.places:
        if (row, col) == (place.entranceRow, place.entranceCol):
            app.gym = place.name

def checkIfGymExit(app, gymX, gymY):
    width = 125
    height = 125
    left = app.gymXDefault - width//2
    right = app.gymXDefault + width//2
    top = app.height - height//2
    bottom = app.height
    if ((left <= gymX <= right) and
        (top <= gymY <= bottom)):
        app.gym = None

def inBattleZone(gymX, gymY):
    left = app.width * 0.5296
    right = app.width * 0.58
    top = app.height * 0.3573
    bottom = app.height * 0.464
    return ((left <= gymX <= right) and
        (top <= gymY <= bottom))

def drawInsidePlace(app, place):
    url = app.placeInsides[place]
    drawImage(url, app.width//2, app.height//2, align='center',
              width=app.height, height=app.height)

def changeBackground(app):
    tRow, tCol = getTile(app, app.cx, app.cy)
    if app.gym == None:
        checkInWhichPlace(app, tRow, tCol)
        if app.gym != None: # entered a gym from the world
            if app.currBackgroundState == 'world': # may not need this
                # app.prevBackgroundState = 'world'
                app.gymX, app.gymY = app.gymXDefault, app.gymYDefault
            app.currBackgroundState = 'gym'
        else:
            app.currBackgroundState = 'world'
    elif app.gym != None: 
        checkIfGymExit(app, app.gymX, app.gymY)
        if app.gym == None: # exited the gym to the world
            if app.currBackgroundState == 'gym': # may not need this
                app.cx, app.cy = getCoords(app, tRow + 1, tCol)
            app.currBackgroundState = 'world'
            return
        else:
            app.currBackgroundState = 'gym'
            if inBattleZone(app.gymX, app.gymY): # entered battle state
                app.state = 'battle'
                enterBattle(app, app.currentOpponentToFight)
                app.gymX, app.gymY = app.gymXDefault, app.gymYDefault

def drawBackground(app):
    if app.currBackgroundState == 'gym':
        drawInsidePlace(app, app.gym)
        drawImage(app.currentOpponentToFight.currentPokemon.sprite,
                  app.width*0.444, app.height*0.394, align='center', 
                  width=app.cellWidth, height=app.cellHeight)
    elif app.currBackgroundState == 'world': 
        drawBoard(app)
        drawPlaces(app)
        
def drawTeamBuildMenu(app):
    drawImage(assetPath('pokeSelectMenu.png'), app.width / 2 - 200, 25, 
              width = 400, height = 700)
    for i in range(len(app.player.completeListOfPokemon)):
        pokemon = app.player.completeListOfPokemon[i]
        if i == app.selectedTeammate: color = 'red'
        else: color = 'black'
        drawLabel(pokemon.name, app.width//2, 87 + 54 * i, font = 'courier', 
                  fill = color, size = 24, bold = True)
    
    for i in range(len(app.player.pokemon)):
        if i < 2:
            drawImage(app.player.pokemon[i].sprite, 547+i*160,
                      616, width = 64, height = 64, align = 'center')
        else:
            drawImage(app.player.pokemon[i].sprite,547+(i-2)*160,677, 
                      width = 64, height = 64, align = 'center')
    