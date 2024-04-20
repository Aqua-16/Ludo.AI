# -*- coding: utf-8 -*-
"""
@author: Sahil Dutta
"""

import ludopy
import cv2
import numpy as np
import matplotlib.pyplot as plt
from player import Agent

def epsilon_decay(epsilon, e_decay, episode):
    return epsilon * np.exp(-e_decay * episode)

def learn(episodes, no_of_players, epsilon, e_decay, lr, gamma):
    win_avg = []
    epsilon_history = []
    win_count = 0
    win_rate = []
    
    if no_of_players == 4:
        game = ludopy.Game(ghost_players=[])
    elif no_of_players == 3:
        game = ludopy.Game(ghost_players=[1])
    else:
        game = ludopy.Game(ghost_players=[1,3])
        
    player_1 = Agent(0, gamma, lr, epsilon) # Main Player
    player_2 = Agent(1, gamma, lr, epsilon)
    
    for episode in range(episodes):
        there_is_a_winner = False
        game.reset()
        cv2.destroyAllWindows()
        while not there_is_a_winner:
            (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_idx = game.get_observation()
            
            if(len(move_pieces)):
                if (player_1.agent_idx == player_idx):
                    piece_to_move = player_1.update(game.players, move_pieces, dice)
                elif (player_2.agent_idx == player_idx):
                    piece_to_move = player_2.update(game.players, move_pieces, dice)
                else:
                    piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
            else:
                piece_to_move = -1
                
            _, _, _, _, player_is_a_winner, there_is_a_winner = game.answer_observation(piece_to_move)
            
            if(episode % 50 == 0):
                enviroment_image_rgb = game.render_environment() # RGB image of the enviroment
                enviroment_image_bgr = cv2.cvtColor(enviroment_image_rgb, cv2.COLOR_RGB2BGR)
                enviroment_image_bgr = cv2.resize(enviroment_image_bgr, (800,800), interpolation = cv2.INTER_LINEAR)
                cv2.imshow("LudoAI", enviroment_image_bgr)
                cv2.waitKey(1)
            
            if (player_1.agent_idx == player_idx and piece_to_move != -1):
                player_1.reward(game.players, [piece_to_move])
            
        new_epsilon = epsilon_decay(epsilon, e_decay, episode)
        epsilon_history.append(new_epsilon)
        player_1.q_learning.updateEpsilon(new_epsilon)
        
        if(game.first_winner_was == player_1.agent_idx):
            win_avg.append(1)
            win_count += 1
        else:
            win_avg.append(0)
            
        elo = (win_count / len(win_avg)) * 100.0
        win_rate.append(elo)
        
        if((episode+1) % 50 == 0):
            print("Episode : ", (episode+1))
            print(f"Win Rate: {np.round(elo, 1)}%")
            
        player_1.q_learning.max_reward = 0
    game.save_hist_video("training_end_game.mp4")
    np.savez('weights.npz', action_table = player_1.action_table_player.getActionTable(), q_table = player_1.q_learning.getQTable(), move_table = player_1.action_table_player.getMoveTable())
    return win_rate, epsilon_history
def plot(win_rate, epsilon_history):
    
    window_size = 20
    win_rate = np.insert(win_rate, 0, 0)
    
    cumsum = np.cumsum(win_rate)
    win_rate_moving_average = (cumsum[window_size:] - cumsum[:-window_size]) / window_size
        
    moving_average_list = [0] * window_size
    win_rate_moving_average = moving_average_list + win_rate_moving_average.tolist()
    
    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Win Rates")
    axes[0].set_xlabel("Episodes")
    axes[0].set_ylabel("Win Rate %")
    axes[0].plot(win_rate_moving_average, color = 'red')
    
    axes[1].set_title("Epsilon Decay")
    axes[1].set_xlabel("Episodes")
    axes[1].set_ylabel("Epsilon")
    axes[1].plot(epsilon_history, color = 'blue')
    
    plt.show()
    
def test(agent_file, no_of_opponents):
    weights = np.load(agent_file)
    action_table = weights['action_table']
    q_table = weights['q_table']
    move_table = weights['move_table']
    
    player = Agent(0, 0, 0, 0)
    player.action_table_player.action_table = action_table
    player.q_learning.q_table = q_table
    player.action_table_player.piece_to_move = move_table
    
    if no_of_opponents == 3:
        game = ludopy.Game(ghost_players=[])
    elif no_of_opponents == 2:
        game = ludopy.Game(ghost_players=[1])
    else:
        game = ludopy.Game(ghost_players=[1,3])
        
    there_is_a_winner = False
    game.reset()
    cv2.destroyAllWindows()
    while not there_is_a_winner:
        (dice, move_pieces, player_pieces, enemy_pieces, player_is_a_winner, there_is_a_winner), player_idx = game.get_observation()
        if(len(move_pieces)):
            if (player.agent_idx == player_idx):
                piece_to_move = player.update(game.players, move_pieces, dice)
            else:
                piece_to_move = move_pieces[np.random.randint(0, len(move_pieces))]
        else:
            piece_to_move = -1
            
        _, _, _, _, player_is_a_winner, there_is_a_winner = game.answer_observation(piece_to_move)
        
    if(game.first_winner_was == player.agent_idx):
        print("AI has won!")
    else:
        print("AI has lost!")
    
    cv2.destroyAllWindows()
    game.save_hist_video("gameplay.mp4")
                

if __name__ == '__main__':
    
    learning_rate = 0.01
    gamma = 0.7
    epsilon = 0.9
    e_decay = 0.05
    episodes = 300
    
    win_rate, epsilon_history = learn(episodes, 2, epsilon, e_decay, learning_rate, gamma)
    plot(win_rate, epsilon_history)
    test('weights.npz', 2)