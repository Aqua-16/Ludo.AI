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
    HOME_GOAL = 1
    HOME_KILL = 2
    HOME_PROTECT = 3
    HOME_STAR = 4
    HOME_GLOBE = 5
    HOME_DIE = 6
    HOME_ZONE = 7
    
    SAFE_BEGIN = 0
    SAFE_GOAL = 1
    SAFE_KILL = 2
    SAFE_PROTECT = 3
    SAFE_STAR = 4
    SAFE_GLOBE = 5
    SAFE_DIE = 6
    SAFE_ZONE = 7
    
    UNSAFE_BEGIN = 0
    UNSAFE_GOAL = 1
    UNSAFE_KILL = 2
    UNSAFE_PROTECT = 3
    UNSAFE_STAR = 4
    UNSAFE_GLOBE = 5
    UNSAFE_DIE = 6
    UNSAFE_ZONE = 7
    
class StateSpace():
    
    quarter_game_size = 13
    star_positions = [5, 12, 18, 25, 31, 38, 44, 51]
    globe_positions_global = [9, 22, 35, 48]
    globe_position_local = [1]
    danger_positions_local = [14, 27, 40]
    local_player_position = [Player(), Player(), Player(), Player()]
    global_player_position = [Player(), Player(), Player(), Player()]
    action_table_player = ActionTable(len(State), len(Action))
    
    