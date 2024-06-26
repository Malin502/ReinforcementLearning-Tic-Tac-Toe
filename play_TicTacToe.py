import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import random
import time
from time import sleep
import numpy as np
import math
import copy

from gameManager import *
from player_contoroller import *
from Q_Learning import *


pygame.init()

eta = 0.05  # 学習率
gamma = 0.8  # 時間割引率
initial_epsilon = 0.5  # ε-greedy法の初期値
episode = 1500000


Q_Learning = QLearning()
playerController = get_input()
GameManager = gameManager()


#mode 0: train, mode 1: ランダム mode 2: Q学習 mode 3: プレイヤー
mode = 2
#order 1: プレイヤーが先手, 2: プレイヤーが後手
order = 2 



if mode == 0:
    # ランダム vs QL(学習)
    # 試行数設定をお忘れなく
    winner_list = []
    q_table = QLearning.make_q_table()
    q_table_test = QLearning.make_q_table()
    start = time.time()
    
    for i in range(episode):
        epsilon = initial_epsilon * (episode-i) / episode
        
        if i % 20000 == 0:
            print('episode:{}'.format(i))
            q_table_test = q_table.copy()
        
        #(first_inputter: 0で先行, 1で後攻)
        if(i % 2 == 0):
            order = 0
        else:
            order = 1
            
        if(i > 20000):
            winner, q_table = GameManager.QLAI_vs_QLAI(order, q_table, q_table_test, epsilon)
        else:
            winner, q_table = GameManager.randomAI_vs_QLAI(order, q_table, epsilon)
            
        
        winner_list.append(winner)
        
    Q_Learning.save_q_table(q_table)
    elapsed_time = time.time() - start


    print ('elapsed_time:{0}'.format(elapsed_time) + '[sec]')

    num_win_QLAI = winner_list.count('QL AI1') + winner_list.count('QL AI')

    print('勝ち回数')
    print('Random AI:{}'.format(winner_list.count('Random AI')))
    print('QL AI1   :{}'.format(num_win_QLAI))
    print('QL AI2   :{}'.format(winner_list.count('QL AI2')))
    print('NOBODY   :{}'.format(winner_list.count('NOBODY')))
    print('QLの勝率 :{}'.format(num_win_QLAI / len(winner_list)))


elif mode == 1:
    # プレイヤー vs ランダム
    GameManager.player_vs_randomAI(order)
    
    
elif mode == 2:
    # プレイヤー vs QL
    # 試行数設定
    winner_list = []

    q_table = QLearning.make_q_table()
    q_table = Q_Learning.load_q_table('q_table.npy')

    
    continue_flag = True
    
    while True:
        
        epsilon = 0
        winner, q_table = GameManager.player_vs_QLAI(order, q_table, epsilon)
        winner_list.append(winner)
        
        yes_rect, no_rect = gameManager.draw_popup(winner)
        
        continue_flag = gameManager.handle_popup_events(yes_rect, no_rect)
            
        if continue_flag == False:
            break
        
        pygame.display.update()
        
    
elif mode == 3:
    # プレイヤー vs プレイヤー
    GameManager.player_vs_player(order)
        
else:
    print('mode error')
    