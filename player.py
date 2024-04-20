# -*- coding: utf-8 -*-
"""
@author: Sahil Dutta
"""

import numpy as np
from QT import Rewards
from stateSpace import Action, State, StateSpace

class Agent(StateSpace):
    
    def __init__(self, agent_idx, gamma, lr, epsilon):
        super().__init__()
        
        self.agent_idx = agent_idx
        self.q_learning = Rewards(len(State), len(Action), gamma=gamma, lr=lr, epsilon = epsilon)
        
        self.state = None
        self.action = None
        
    def update(self, players, pieces_to_move, dice):
        super().update(players, self.agent_idx, pieces_to_move, dice)
        action_table = self.action_table_player.getActionTable()
        state, action = self.q_learning.chooseNextAction(self.agent_idx, action_table)
        pieces_to_move = self.action_table_player.getPieceToMove(state, action)
        self.state = state
        self.action = action
        
        return pieces_to_move
    
    def reward(self, players, pieces_to_move):
        
        super().getPossibleActions(players, self.agent_idx, pieces_to_move)
        new_action_table = np.nan_to_num(self.action_table_player.getActionTable(), nan=0.0)
        self.q_learning.qUpdate(self.state, self.action, new_action_table)