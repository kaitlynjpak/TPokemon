import os
from qLearning import *
from RLenvironment import *
from PokemonCreator import *

qtables = {}
qtables_folder = '''C:\\Users\\diyan\\OneDrive\\Documents\\GitHub\\
                    prelim-group-11-tp\\src\\qtables2'''
allPokemon = [kimchee, kosbie, carpeDiem, consultDragon, 
              kerryTheKube, redBull, rubberDuck, shower, taylor, tetrimino]

pokeMap = {poke.name: poke for poke in allPokemon}
# Load Q-tables
for filename in os.listdir(qtables_folder):
    if filename.endswith('.json'):
        p1, p2 = filename.replace('.json', '').split('_vs_')
        poke1 = pokeMap[p1]
        poke2 = pokeMap[p2]
        env = Environment(poke1, poke2)
        qlearn = QLearning(environment=env, alpha=0.1, gamma=0.9, 
                           epsilon=0, decay=0.99, minEpsilon=0.01)
        qlearn.loadQTable(os.path.join(qtables_folder, filename))
        qtables[(p1, p2)] = qlearn

# Pokémon list

# Accuracy results
winAccuracies = {}

numBattles = 100

for i in range(len(allPokemon)):
    for j in range(i + 1, len(allPokemon)):
        p1 = allPokemon[i]
        p2 = allPokemon[j]

        if (p1.name, p2.name) in qtables:
            qAgent = qtables[(p1.name, p2.name)]
            env = qAgent.environment

            p1Wins = 0
            for _ in range(numBattles):
                env.resetBattle()  # No need to pass p1 and p2 here
                state = env.getState()
                done = False
                while not done:
                    action = qAgent.choose(state)
                    nextState, reward, done = env.onStep(action)
                    state = nextState
                winner = env.getWinner()
                if winner is not None and winner.name == p1.name:
                    p1Wins += 1

            accuracy = (p1Wins / numBattles) * 100
            winAccuracies[f'{p1.name} vs {p2.name}'] = accuracy

# Print results
print("Win Accuracy for each Pokémon Combination:")
for match, acc in winAccuracies.items():
    print(f"{match}: {acc:.2f}% win rate")