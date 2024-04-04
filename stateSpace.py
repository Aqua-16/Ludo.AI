# -*- coding: utf-8 -*-
"""
@author: Sahil Dutta
"""

from enum import Enum

import numpy as np
from actionTable import ActionTable
from ludopy.player import Player

class State(Enum):
    
    HOME = 0 # Player Start
    SAFE = 1 # Spaces where the player cannot be killed
    UNSAFE = 2 # All other spaces where player can be killed
    
class Action(Enum):
    
    HOME_BEGIN = 0
    HOME_MOVE = 1
    HOME_GOAL = 2
    HOME_KILL = 3
    HOME_PROTECT = 4
    HOME_STAR = 5
    HOME_GLOBE = 6
    HOME_DIE = 7
    HOME_ZONE = 8
    
    SAFE_BEGIN = 9
    SAFE_MOVE = 10
    SAFE_GOAL = 11
    SAFE_KILL = 12
    SAFE_PROTECT = 13
    SAFE_STAR = 14
    SAFE_GLOBE = 15
    SAFE_DIE = 16
    SAFE_ZONE = 17
    
    UNSAFE_BEGIN = 18
    UNSAFE_MOVE = 19
    UNSAFE_GOAL = 20
    UNSAFE_KILL = 21
    UNSAFE_PROTECT = 22
    UNSAFE_STAR = 23
    UNSAFE_GLOBE = 24
    UNSAFE_DIE = 25
    UNSAFE_ZONE = 26
    
class StateSpace():
    
    def __init__(self):
        self.quarter_game_size = 13
        self.star_positions = [5, 12, 18, 25, 31, 38, 44, 51]
        self.globe_positions_global = [9, 22, 35, 48]
        self.globe_position_local = [1]
        self.danger_positions_local = [14, 27, 40]
        self.local_player_position = [Player(), Player(), Player(), Player()] # Player positions as mapped by individual players for themselves
        self.global_player_position = [Player(), Player(), Player(), Player()] # Player positions relative to actual board indices
        self.action_table_player = ActionTable(len(State), len(Action))
        
    def getGlobalPosition(self, player, piece):
        return self.global_player_position[player].pieces[piece]

    def getLocalPosition(self, player, piece):
        return self.local_player_position[player].pieces[piece]
    
    def getGlobalPositionFromLocalPosition(self, player_idx, local_position):
        if local_position == 0 or local_position == 59:
            return local_position
        else:
            return (local_position + (self.quarter_game_size * player_idx)) % 52
    
    def updatePlayerPositions(self, players):
        self.local_player_position = players
        player_idx = 0
        
        for player in players:
            piece_idx = 0
            for piece in player.pieces:
                self.global_player_position[player_idx].pieces[piece_idx] = self.getGlobalPositionFromLocalPosition(player_idx, piece)
                piece_idx = piece_idx + 1
            player_idx = player_idx + 1
            
   
    def isPieceSafe(self, player, piece):
        local_pos = self.local_position(player, piece)
        global_pos = self.global_position(player, piece)
        is_protected = len(np.where(self.local_player_position[player].pieces == self.local_position(player, piece))[0]) > 1
        if global_pos in self.globe_positions_global or local_pos in self.globe_positions_local:
            return True
        # check if piece is in goal zone
        if local_pos >= 53:
            return True
        if local_pos != 0 and local_pos != 59 and is_protected:
            return True
        return False
    