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
            
   
    def isPieceSafe(self, player, piece, dice = 0):
        local_pos = self.getLocalPosition(player, piece) + dice
        global_pos = self.getGlobalPosition(player, piece) + dice
        is_protected = len(np.where(self.local_player_position[player].pieces == local_pos)[0]) > 1
        if global_pos in self.globe_positions_global or local_pos in self.globe_position_local:
            return True
        # check if piece is in goal zone
        if local_pos >= 53:
            return True
        if local_pos != 0 and local_pos != 59 and is_protected:
            return True
        return False
    
    def getEnemyList(self, player):
        
        kill_list = []
        die_list = []
        
        for enemy_player_idx in range(len(self.global_player_position)):
            for enemy_piece_idx in range(len(self.global_player_position[enemy_player_idx].pieces)):
                enemy_position = self.getGlobalPosition(enemy_player_idx, enemy_piece_idx)
                enemy_local_position = self.getLocalPosition(enemy_player_idx, enemy_piece_idx)
                if (enemy_local_position in player.pieces) or (enemy_position > 53 or enemy_position == 0):
                    continue
                
                if enemy_position in self.globe_positions_global or enemy_local_position in self.globe_position_local:
                    die_list.append(enemy_position)
                    continue
                
                if enemy_position in kill_list: # The purpose of this is to mark spots where the enemy has stacked pieces
                    die_list.append(enemy_position)
                    kill_list.remove(enemy_position)
                    
                else:
                    kill_list.append(enemy_position)
                    
        enemyList = []
        enemyList.extend(kill_list)
        enemyList.extend(die_list)
        return (kill_list, die_list, enemyList)
    
    def getPlayerState(self, player, piece, dice):
        local_pos = self.getLocalPosition(player, piece) + dice
        if local_pos == dice:
            return State.HOME
        if self.isPieceSafe(player, piece, dice):
            return State.SAFE
        return State.UNSAFE
    
    def setPlayerState(self, player, piece):
        
        if self.getLocalPosition(player, piece) == 0:
            self.action_table_player.setState(State.HOME)
            
        elif self.isPieceSafe(player, piece):
            self.action_table_player.setState(State.SAFE)
            
        else:
            self.action_table_player.setState(State.UNSAFE)
    
    
    def updateBeginAction(self, player, piece, dice):
        if self.getLocalPosition(player, piece) == 0 and dice == 6:
            next_state = self.getPlayerState(player, piece, dice).value
            if self.getGlobalPositionFromLocalPosition(player, 1) in self.enemyList:
                self.action_table_player.updateActionTable(Action(Action.HOME_KILL.value + next_state * 9), piece)
            else:
                self.action_table_player.updateActionTable(Action(Action.HOME_BEGIN.value + next_state * 9), piece)
            return True
        return False

    def updateMoveAction(self, player, piece, dice):
        if self.getLocalPosition(player, piece) == 0:
            return False
        
        if self.getLocalPosition(player, piece) + dice <= 59:
            next_state = self.getPlayerState(player, piece, dice).value
            self.action_table_player.updateActionTable(Action(Action.HOME_MOVE.value + next_state * 9), piece)
            return True

    def updateGoalAction(self, player, piece, dice):
        if self.getLocalPosition(player, piece) + dice == 59:
            next_state = self.getPlayerState(player, piece, dice).value
            self.action_table_player.updateActionTable(Action(Action.HOME_GOAL.value + next_state * 9), piece)
            return True
        return False

    def updateStarAction(self, player, piece, dice):
        if self.getLocalPosition(player, piece) == 0:
            return False
        if (self.getLocalPosition(player, piece) + dice) in self.star_positions:
            next_state = self.getPlayerState(player, piece, dice).value
            self.action_table_player.updateActionTable(Action(Action.HOME_STAR.value + next_state * 9), piece)
            return True
        return False

    def updateGlobeAction(self, player, piece, dice):
        if self.getLocalPosition(player, piece) == 0:
            return False
        if (self.getGlobalPosition(player, piece) + dice) in self.globe_positions_global:
            next_state = self.getPlayerState(player, piece, dice).value
            self.action_table_player.updateActionTable(Action(Action.HOME_GLOBE.value + next_state * 9), piece)
            return True
        return False

    def updateProtectAction(self, player, piece, dice):
        if self.getLocalPosition(player, piece) == 0:
            return False
        target_position = self.getLocalPosition(player, piece) + dice
        if target_position > 53:
            return False
        for i in range(len(self.local_player_position)):
            if i == piece:
                continue
            if target_position == self.getLocalPosition(player, i):
                next_state = self.getPlayerState(player, piece, dice).value
                self.action_table_player.updateActionTable(Action(Action.HOME_PROTECT.value + next_state * 9), piece)
                return True
        return False

    def updateKillAction(self, player, piece, dice, kill_list):
        if self.getLocalPosition(player, piece) == 0:
            local_target_position = 1
        else:
            local_target_position = self.getLocalPosition(player, piece) + dice
        if local_target_position > 53:
            return False

        target_position = self.getGlobalPosition(player, piece) + dice
        if (
            target_position in kill_list
            and target_position not in self.globe_positions_global
            and local_target_position not in self.globe_position_local
            and local_target_position not in self.danger_positions_local
        ):
            next_state = self.getPlayerState(player, piece, dice).value
            self.action_table_player.updateActionTable(Action(Action.HOME_KILL.value + next_state * 9), piece)
            return True
        return False

    def updateDieAction(self, player, piece, dice, dieList):
        if self.getLocalPosition(player, piece) == 0:
            return False
        local_target_position = self.getLocalPosition(player, piece) + dice
        if local_target_position > 53:
            return False

        target_position = self.getGlobalPosition(player, piece) + dice
        if target_position in dieList:
            next_state = self.getPlayerState(player, piece, dice).value
            self.action_table_player.updateActionTable(Action(Action.HOME_DIE.value + next_state * 9), piece)
            return True
        return False

    def updateZoneAction(self, player, piece, dice):
        if self.getLocalPosition(player, piece) == 0:
            return False
        local_target_position = self.getLocalPosition(player, piece) + dice
        if local_target_position > 53 and local_target_position < 59:
            next_state = self.getPlayerState(player, piece, dice).value
            self.action_table_player.updateActionTable(Action(Action.HOME_ZONE.value + next_state * 9), piece)
            return True
        return False
    
    def checkGoalZone(self, player, piece, dice):
        local_position = self.getLocalPosition(player, piece)
        local_target_position = local_position + dice
        if local_target_position < 53:
            return False
        if local_position >= 53:
            self.action_table_player.setState(State.SAFE)
        if local_target_position == 59:
            self.action_table_player.updateActionTable(Action(Action.SAFE_GOAL), piece)
            return True
        self.action_table_player.updateActionTable(Action(Action.SAFE_ZONE), piece)
        return True
    
    def update(self, players, current_player, pieces_to_move, dice):
        self.updatePlayerPositions(players)
        self.action_table_player.reset()
        player = players[current_player]
        (killList, dieList, enemyList) = self.getEnemyList(player)
        self.enemyList = enemyList
        for piece in pieces_to_move:
            self.setPlayerState(current_player, piece)
            if self.updateBeginAction(current_player, piece, dice):
                continue
            if self.checkGoalZone(current_player, piece, dice):
                continue
            if self.updateDieAction(current_player, piece, dice, dieList):
                continue
            if self.updateStarAction(current_player, piece, dice):
                continue
            if self.updateGlobeAction(current_player, piece, dice):
                continue
            if self.updateProtectAction(current_player, piece, dice):
                continue
            if self.updateKillAction(current_player, piece, dice, killList):
                continue
            if self.updateMoveAction(current_player, piece, dice):
                continue
            
    def getPossibleActions(self, players, current_player, pieces_to_move):
        
        self.updatePlayerPositions(players)
        self.action_table_player.reset()
        player = players[current_player]
        (killList, dieList, enemyList) = self.getEnemyList(player)
        self.enemyList = enemyList
        
        for piece in pieces_to_move:
            for dice in range(1,6):
                self.setPlayerState(current_player, piece)
                self.updateBeginAction(current_player, piece, dice)
                self.checkGoalZone(current_player, piece, dice)
                self.updateDieAction(current_player, piece, dice, dieList)
                self.updateStarAction(current_player, piece, dice)
                self.updateGlobeAction(current_player, piece, dice)
                self.updateProtectAction(current_player, piece, dice)
                self.updateKillAction(current_player, piece, dice, killList)
                self.updateMoveAction(current_player, piece, dice)