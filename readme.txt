Dependancies in terminal:
1. pip install pillow
2. pip install opencv-python

NOTE: You must NOT be in FULL SCREEN for certain game functions to work, please do not alter window size.

Description:
In this game, you are a pokemon trainer and your job is to explore the world map and find gyms to fight other pokemon. 
If you win the battle (by depleting the other pokemons health before yours is depleted), then you win the pokemon. 

There are 10 pokemon total, the default is your starter pokemon, and as you win games against other pokemon, 
those pokemon get added to the set of pokemon that the user can use in their next game. 
So at the beginning of each of the 9 battles in the game, you can select which pokemon you want to play in battle 
(the opponent is predetermined) and there's only 9 opponent pokemon (3 per difficulty level)). 

Use the 4 attack buttons available to your pokemon in this turn based game to deplete the health of your opponent before 
they can deplete yours! At the end of each battle your pokemons will automatically be healed so you can use them again if you wish!
Good Luck! 

Game toggles: 
'y' to battle
't' to view the open world map
'u' to input your face as your trainer sprite


Special Feature**: AI opponent pokemon

We used reinforcement learning to get the AI to play pokemon with very high accuracy by anticipating the user's next move. 
Then, we altered the algorithm in our game to purposely make wrong moves based on the difficulty level so the user would
win a certain percentage of the time based on the difficulty level of the gym.

**an additional special feature is our use of opencv to upload the user's photo to create a custom trainor!

