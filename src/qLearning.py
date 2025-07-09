#dumping all the decision making math and explanations as far as i 
# understand here had to watch some tutroials for this one

#qlearning is basically a model-less selection algorithm
#each state and action pair is associated witha certain q value
#the q val reps the quality of the action the pokemon made in the state 
# the game is currently in
#this is the equation to find the q val:
#Q(s​,a​) = alpha(r + γ*max​(Q(s' ​, a'))) alpha is learning rate, r is reward 
# from the curuent (s,a) pair, s' is the next state and a' is the next action 
# and lambda is how much the future action is weigthed in hte reward system 
# compared to the current, called the 'discount'. max​(Q(s' ​, a')) is just 
# the alghorithms prediction for the best reward from the next state 
# (an assumption) qlearning / epsilson greedy algorithms just amalgamate these 
# q vals into a table of rewards it earned from each s, a pair
#typically chooses good action, but ocassonally bad so that the algorithm 
# explores other paths to the goal the state wold be smth like ("kosbie: 50 
# health, taylor: 60 health") and the action/move is 2. and the the assigned 
# qval in the qtable(the dicitonary) is 0.5(ok score)

import json
import random
import os
import ast

class QLearning:
    def __init__(self, environment, alpha, gamma, epsilon, decay, minEpsilon):
        self.environment = environment
        self.alpha = alpha #i defined these above for yall
        self.gamma = gamma
        self.epsilon = epsilon #explore ratw
        self.decay = decay #how much to decrease explore rate, higher means 
        #it explores one move longer
        self.minEpsilon = minEpsilon #we don't want neg vals for rate

        self.qTable = {} #gonna put the s, a tuple pairs here w/ their q vals

    def getQ(self, state, action):
        if (state, action) not in self.qTable:
            self.qTable[(state, action)] = 0 #i used chatgpt to find what the 
            #default q val should be, it said to keep it neutral on the first 
            # pass and also used chat for the next line
        prevQval = self.qTable[(state, action)]
        return prevQval
    
    def updateQ(self, state, action, reward, nextState): #per s,a pair 
        #updating the table
        actionsPossible = []
        for i in range(len(self.environment.possibleMoves)):
            actionsPossible.append(i)

        #next state max q vale (remmebr the equation)
        maxPossibleQVal = -1000000000000000 #smol numebr
        for action in actionsPossible:
            if (nextState, action) not in self.qTable:
                self.qTable[(nextState, action)] = 0
            if self.qTable[(nextState, action)] > maxPossibleQVal:  #chatgpt 
                #helped write this line and the next 
                maxPossibleQVal = self.qTable[(nextState, action)]
        
        #plug into equation
        newQ = self.alpha * (reward + self.gamma * maxPossibleQVal)
        self.qTable[(state, action)] = newQ
     
    def train(self, epochs):   #inner training loop just for 1v1 matchup 
        #calls 100 times
        for epoch in range(epochs):
            state = self.environment.resetBattle() #start
            done = False #initialze game to not over yet
            while done == False: #used chatgpt for this while loop
                action = self.choose(state)
                nextState, reward, done = self.environment.onStep(action)
                #Take a step in the environment
                self.updateQ(state, action, reward, nextState)  # Update 
                #Q-table using the equation Q(s, a) = r + γ * max Q(s', a')
                state = nextState
            self.decayEpsilon() #update eplsion

    def choose(self, state): #this function is all chatgpt for 
        #storing in the qtable:
        if random.random() < self.epsilon:
            # Exploration: Choose a random action
            action = random.choice(range(len(self.environment.possibleMoves)))
            return action
        else: #best Templtae
            bestAction = None
            bestQ = -10000000000000
            for action in range(len(self.environment.possibleMoves)):
                qVal = self.getQ(state, action)
                if qVal > bestQ:
                    bestQ = qVal
                    bestAction = action
            return bestAction
    
    def decayEpsilon(self):
        self.epsilon *=  self.decay

        if self.epsilon < self.minEpsilon:
            self.epsilon = self.minEpsilon
    
    #the next two functions were made with ChatGPT since I dont have 
    # experience with json files
    def saveQTable(self, filename):
        directory = os.path.dirname(filename) #make da file
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        serialized = {str(key): values for key, values in self.qTable.items()}
        with open(filename, 'w') as f: #w is write mode for files
            json.dump(serialized, f)
        

    def loadQTable(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.qTable = {ast.literal_eval(key): value for key, value in 
                       data.items()}
