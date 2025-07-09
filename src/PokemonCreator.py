from entityClasses import *
from assetsUtils import assetPath
from trainor import *
import copy

#Typical defense modifier increases by 25%, typical attack and speed by 50%
#Defining all of the moves that will be used in TPokemon
#(name, damage, defenseMod, speedMod, attackMod, 
# duration, accuracy, hasOtherTarget)

splash = PokeMove('Splash', 30, 0, 0, 0, 100, True)
bounce = PokeMove('Bounce', 0, 0, 0.5, 0, 100, False)
boogie = PokeMove('Boogie', -20, 0, 0, 0, 100, False)
consult = PokeMove('Consult', 0, 0.15, 0.15, 0.15, 100, False)
seizeTheDay = PokeMove('Seize the day', 100, 0, 0, 0, 10, True)
tomatoSplotch = PokeMove('Tomato SPLOTCH', 40, 0, -.15, 0, 85, True)
doKingsTour = PokeMove('doKingsTour', 0, 0, 1, 0, 100, False)
kosbieKrashout = PokeMove('Kosbie Krashout', 112, 0, 0, 0, 60, True)
givesYouWings = PokeMove('RedBull Gives You Wings!!!', 0, 0, 0.85, 0,
                         100, False)
squeak = PokeMove('SQUEAK!!!', 50, 0, 0, 0, 100, True)
hygiene = PokeMove('Hygiene', 60, 0, 0, 0, 75, True)
tetriminoHardDrop = PokeMove('HARD drop', 75, 0, 0, 0, 75, True)
synthesize = PokeMove('SYNTHESIZE', -30, 0.1, 0.1, 0.1, 100, False)

kimcheeList = [splash, bounce, boogie]

#(name, health, moveList, sprite, type, defense, speed, attack)
kimchee = Pokemon('Kimchee', 50, kimcheeList, 
               assetPath('kimchee.png'),'water',
               20, 40, 15)

kosbieList = [kosbieKrashout, boogie, doKingsTour, seizeTheDay]

kosbie = Pokemon('Kosbie', 250, kosbieList, assetPath('kosbie.png'), 'cs',
                       50, 40, 75)

carpeDiemList = [seizeTheDay]

carpeDiem = Pokemon('Carpe Diem', 75, carpeDiemList, assetPath('carpeDiem.png'),
                    'cs', 30, 10, 50)

consultDragonList = [consult, splash, givesYouWings, hygiene]

consultDragon = Pokemon('Consult Dragon', 150, consultDragonList, 
                        assetPath('consultDragon.png'), 'water', 75, 30, 40)

kerryList = [tomatoSplotch, tetriminoHardDrop]

kerryTheKube = Pokemon('Kerry the Kube', 100, kerryList, 
                       assetPath('kerryTheKube.png'), 'game', 40, 15, 15)

redbullList = [givesYouWings, splash, bounce]

redBull = Pokemon('RedBull', 50, redbullList, assetPath('redbull.png'), 'water', 
                  10, 80, 10)

duckList = [splash, squeak, hygiene]

rubberDuck = Pokemon('Coding Duck', 100, duckList, assetPath('rubberDuck.png'), 
                     'water', 25, 25, 25)

showerList = [splash, hygiene]

shower = Pokemon('Shower', 150, showerList, assetPath('shower.png'), 'water',
                 35, 35, 35)

taylorList = [synthesize, seizeTheDay, tetriminoHardDrop]

taylor = Pokemon('Taylor', 250, taylorList, assetPath('taylor.png'), 'cs', 
                 100, 40, 50)

tetrisList = [tetriminoHardDrop, tomatoSplotch]

tetrimino = Pokemon('Tetrimino', 100, tetrisList, assetPath('tetris.png'), 
                    'game', 10, 30, 50)

# Creates proper opponents for each level
opponentOne = Trainor('opponentOne', assetPath('Trainor.png'), 
                      [copy.deepcopy(carpeDiem)])
opponentTwo = Trainor('opponentTwo', assetPath('Trainor.png'), 
                      [copy.deepcopy(redBull)])
opponentThree = Trainor('opponentThree', assetPath('Trainor.png'), 
                        [copy.deepcopy(kerryTheKube)])
opponentFour = Trainor('opponentFour', assetPath('Trainor.png'), 
                       [copy.deepcopy(rubberDuck)])
opponentFive = Trainor('opponentFive', assetPath('Trainor.png'), 
                       [copy.deepcopy(shower)])
opponentSix = Trainor('opponentSix', assetPath('Trainor.png'), 
                      [copy.deepcopy(tetrimino)])
opponentSeven = Trainor('opponentSeven', assetPath('Trainor.png'), 
                        [copy.deepcopy(consultDragon)])
opponentEight = Trainor('opponentEight', assetPath('Trainor.png'), 
                        [copy.deepcopy(taylor)])
opponentNine = Trainor('opponentNine', assetPath('Trainor.png'), 
                       [copy.deepcopy(kosbie)])

opponentList = [opponentOne, opponentTwo, opponentThree, opponentFour,
                opponentFive, opponentSix, opponentSeven, opponentEight,
                opponentNine]



