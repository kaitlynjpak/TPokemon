from RLenvironment import *
from qLearning import *
from PokemonCreator import *
import json
import copy
import ast
print("start train")


#i asked chatgpt if i need to run the algortihm live for every game, and it 
# said to just store it in json files to reference later.
#loop through each pokemon matchu  
# train for each pair
# save to pair-specific qtable
# ill import the qtable to the other doc
#whenevr a pokemon is selected, the pair is recorded and that qtable will be 
# referenced by the AI

pokeList = [kimchee, kosbie, carpeDiem, consultDragon, kerryTheKube, redBull, 
            rubberDuck, shower, taylor, tetrimino]

pokeListLength = len(pokeList)

for i in range(pokeListLength): #makes 90 qtables yayy outer loop
    for j in range(pokeListLength):
        if i!=j:
            me = copy.deepcopy(pokeList[i])
            opponent = copy.deepcopy(pokeList[j])
            newEnv = Environment(me, opponent)
            qInstance = QLearning(newEnv, 0.1, 0.9, 0.2, 0.1, 0.1)
            qInstance.train(10000) #we can increase this if 100 is too little 
            path = f'qtables/{me.name}_vs_{opponent.name}.json' #asked chatgpt 
            #how to save and store the tables
            qInstance.saveQTable(path)

# used chatGPT to figure our how to allow the algorithm to access the qTable 
# corresponding to any given pokemon pair
def getTable(poke1, poke2):
    file = f'qtables/{poke1.name}_vs_{poke2.name}.json' #this is whats 
    #popylating my qTables folder :)))
    with open(file, 'r') as f:
        data = json.load(f)
    return {ast.literal_eval(key): value for key, value in data.items()}


#i had to look this up and im 90% sure we can just run this file in the termina
#and figures crossed it'll autopopulate the qtables .json file - more research 
# needed on this one