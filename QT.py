# -*- coding: utf-8 -*-
"""
@author: Sahil Dutta
"""
import random
import numpy as np
from stateSpace import Action

class Rewards():
    
    def __init__(self, states, actions, epsilon=0.9, gamma=0.3, lr=0.2,):
        self.rewards_table = np.zeros(len(Action))
        self.q_table = np.zeros([states, actions])
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        
        VERY_BAD = -1.0
        BAD = -0.5
        GOOD = 0.5
        VERY_GOOD = 1.0
        
        self.rewards_table[Action.SAFE_BEGIN.value] = 0.5
        self.rewards_table[Action.SAFE_DIE.value] = -0.8
        self.rewards_table[Action.SAFE_GLOBE.value] = 0.4
        self.rewards_table[Action.SAFE_GOAL.value] = 0.8
        self.rewards_table[Action.SAFE_KILL.value] = 1.5
        self.rewards_table[Action.SAFE_MOVE.value] = 0.1
        self.rewards_table[Action.SAFE_PROTECT.value] = 0.2
        self.rewards_table[Action.SAFE_STAR.value] = 0.4
        self.rewards_table[Action.SAFE_ZONE.value] = 0.8
        
        self.rewards_table[Action.UNSAFE_BEGIN.value] = self.rewards_table[Action.SAFE_BEGIN.value] + GOOD
        self.rewards_table[Action.UNSAFE_DIE.value] = self.rewards_table[Action.SAFE_DIE.value] + VERY_BAD
        self.rewards_table[Action.UNSAFE_GLOBE.value] = self.rewards_table[Action.SAFE_GLOBE.value] + GOOD
        self.rewards_table[Action.UNSAFE_GOAL.value] = self.rewards_table[Action.SAFE_GOAL.value] + VERY_GOOD
        self.rewards_table[Action.UNSAFE_KILL.value] = self.rewards_table[Action.SAFE_KILL.value] + VERY_GOOD
        self.rewards_table[Action.UNSAFE_MOVE.value] = self.rewards_table[Action.SAFE_MOVE.value] + BAD
        self.rewards_table[Action.UNSAFE_PROTECT.value] = self.rewards_table[Action.SAFE_PROTECT.value] + GOOD
        self.rewards_table[Action.UNSAFE_STAR.value] = self.rewards_table[Action.SAFE_STAR.value] + GOOD
        self.rewards_table[Action.UNSAFE_ZONE.value] = self.rewards_table[Action.SAFE_ZONE.value] + VERY_GOOD
        
        self.rewards_table[Action.HOME_BEGIN.value] = self.rewards_table[Action.SAFE_BEGIN.value] + VERY_GOOD
        self.rewards_table[Action.HOME_DIE.value] = self.rewards_table[Action.SAFE_DIE.value] + VERY_BAD
        self.rewards_table[Action.HOME_GLOBE.value] = self.rewards_table[Action.SAFE_GLOBE.value] + VERY_BAD
        self.rewards_table[Action.HOME_GOAL.value] = self.rewards_table[Action.SAFE_GOAL.value] + VERY_BAD
        self.rewards_table[Action.HOME_KILL.value] = self.rewards_table[Action.SAFE_KILL.value] + VERY_BAD
        self.rewards_table[Action.HOME_MOVE.value] = self.rewards_table[Action.SAFE_MOVE.value] + VERY_BAD
        self.rewards_table[Action.HOME_PROTECT.value] = self.rewards_table[Action.SAFE_PROTECT.value] + VERY_BAD
        self.rewards_table[Action.HOME_STAR.value] = self.rewards_table[Action.SAFE_STAR.value] + VERY_BAD
        self.rewards_table[Action.HOME_ZONE.value] = self.rewards_table[Action.SAFE_ZONE.value] + VERY_BAD
        
    def qUpdate(self, state, action, action_table):
        state = int(state)
        action = int(action)
        reward = self.rewards_table[action]
        
        Q_ = np.max(self.q_table * action_table)
        Q = self.q_table[state,action]
        
        delta_Q = self.lr * (reward + self.gamma * Q_ - Q)
        
        self.q_table[state, action] = Q + delta_Q
        
    def updateEpsilon(self, new_epsilon):
        self.epsilon = new_epsilon
        
    def getStateAction(self, value, array):
        if np.isnan(value):
            return (-1, -1)
        pairs = np.where(array == value) # Find possible state action pairs
        pair_idx = random.randint(0, len(pairs[0]) - 1) # Randomly choose one of these pairs
        state = pairs[0][pair_idx]
        action = pairs[1][pair_idx]
        return (state, action)
    
    def chooseNextAction(self, player, action_table):
        q_table_options = self.q_table * action_table
        maxVal = np.nanmax(q_table_options)
        
        if (random.uniform(0, 1) < self.epsilon) or (np.isnan(maxVal)):
            nz = action_table[np.logical_not(np.isnan(action_table))]
            randomValue = nz[random.randint(0, len(nz) - 1)]
            state, action = self.getStateAction(randomValue, action_table)
        else:
            state, action = self.getStateAction(maxVal, q_table_options)
            
        return (state, action)
    
    def getQTable(self):
        return self.q_table