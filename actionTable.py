# -*- coding: utf-8 -*-
"""
@author: Sahil Dutta
"""

import numpy as np

class ActionTable():
    
    action_table = None
    state = 0
    
    def __init__(self, states, actions):
        self.states = states
        self.actions = actions
        self.reset()
    
    def reset(self):
        self.action_table = np.full((self.states, self.actions), np.nan)
        self.piece_to_move = np.full((self.states, self.actions), np.nan)
        
    def setState(self, state):
        self.state = state.value
    
    def getActionTable(self):
        return self.action_table
    
    def getMoveTable(self):
        return self.piece_to_move
    
    def getPieceToMove(self, state, action):
        if (state < 0 or action < 0):
            return -1
        
        return int(self.piece_to_move[state,action])
    
    def updateActionTable(self, action, piece):
        if (np.isnan(self.action_table[self.state, action.value])):
            self.action_table[self.state, action.value] = 1
            self.piece_to_move[self.state, action.value] = piece