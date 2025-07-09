Dependancies in terminal:
1. pip install pillow
2. pip install opencv-python

Description:
In this game, you are a pokemon trainer and your job is to explore the world map and find gyms to fight other pokemon. 
If you win the battle, you win the pokemon. 

There are 10 pokemon total, the default is your starter pokemon, and as you win games against other pokemon, 
those pokemon get added to the set of pokemon that the user can use in their next game. 
You can select which pokemon you want to play in battle at any time, however, the opponent is predetermined.

There are 3 gymns and 3 levels per gym, and each gym increases in difficulty. 

Use the arrow keys to move on the map and find the gyms.

Use the 4 attack buttons available to your pokemon in the battles to deplete the health of your opponent before 
they can deplete yours! At the end of each battle your pokemons will automatically be healed so you can use them again if you wish!
Good Luck! 

Game toggles: 
'y' to battle
't' to view the open world map
'u' to input your face as your trainer sprite

Special Feature**: AI opponent pokemon

We used reinforcement learning to train the AI to play pokemon against a human very well. 
Then, we altered the algorithm in our game to choose the best move or not based on the difficulty level 
so the user wins a certain percentage of the time.
