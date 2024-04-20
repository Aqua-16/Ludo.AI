# -*- coding: utf-8 -*-
"""
@author: Sahil Dutta
"""

import ludopy
import cv2
import numpy as np
from player import Agent
import time

def createAI(player_idx, filename):
    
    player = Agent(player_idx, 0, 0, 0)
    
    weights = np.load(filename)
    action_table = weights['action_table']
    q_table = weights['q_table']
    move_table = weights['move_table']
    
    player.action_table_player.action_table = action_table
    player.q_learning.q_table = q_table
    player.action_table_player.piece_to_move = move_table
    
    return player

def play(no_of_opponents, file):
    players = []
    if no_of_opponents == 3:
        game = ludopy.Game(ghost_players=[1])
        players.append(createAI(3, file))
        players.append(createAI(2, file))
        players.append(createAI(0, file))
    elif no_of_opponents == 2:
        game = ludopy.Game(ghost_players=[0,1])
        players.append(createAI(3, file))
        players.append(createAI(2, file))
    else:
        game = ludopy.Game(ghost_players=[0,1,2])
        players.append(createAI(3, file))
        
    there_is_a_winner = False
    game.reset()
    cv2.destroyAllWindows()
    cv2.namedWindow("LudoAI")
    while not there_is_a_winner:
        (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_idx = game.get_observation()
        print("Player: ", player_idx)
        moment = game._make_moment()
        image = ludopy.make_img_of_board(*moment)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (800,800), interpolation = cv2.INTER_LINEAR)
        cv2.imshow("LudoAI", image)
        cv2.waitKey(1)
        time.sleep(1)
        if(len(move_pieces)):
            for player in players:
                if (player.agent_idx == player_idx):
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break
                    print("AI is playing..")
                    piece_to_move = player.update(game.players, move_pieces, dice)
                    time.sleep(1)
                    break
            else:
                cv2.putText(image, "YOUR TURN", (25,40), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),thickness = 3)
                cv2.imshow("LudoAI", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
                print("Choose one of these pieces to move:- ")
                for piece in move_pieces:
                    print(piece)
                while(True):
                    piece_to_move = int(input("Enter: "))
                    if(piece_to_move in move_pieces):
                        break
                    print("Invalid Piece. Please enter a valid move.")
                
        else:
            piece_to_move = -1
            
        _, _, _, _, player_is_a_winner, there_is_a_winner = game.answer_observation(piece_to_move)
        
        
    cv2.destroyAllWindows()
    
    
if __name__ == '__main__':
    n = int(input("How many opponents would you like to play against?\t"))
    play(n, 'prime_weights.npz')