import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import random
import time
from time import sleep
import numpy as np
import math

from player_contoroller import get_input

import pygame
import sys


# Global variables
play_area = list(range(1, 10))
player = '○'
running = True



window = pygame.display.set_mode((350, 420))
pygame.display.set_caption('Tic Tac Toe with AI')
        
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
button_color = (100, 200, 100)
button_rect = pygame.Rect(100, 320, 100, 50)


pygame.font.init()
font_button = pygame.font.Font(None, 40)
button_text = font_button.render("Fin", True, BLACK)
font = pygame.font.Font(None, 100)




class gameManager(get_input):
    
    
    
    @staticmethod
    def draw_popup(winner):
        # Darken the screen
        width = 600
        height = 600
        
        
        s = pygame.Surface((width, height), pygame.SRCALPHA)   # per-pixel alpha
        s.fill((0, 0, 0, 128))                                # RGBA
        window.blit(s, (0, 0))
        
        # Draw the popup box
        popup_rect = pygame.Rect(50, 100, 200, 150)
        pygame.draw.rect(window, WHITE, popup_rect)
        
        # Draw the text
        font_popup = pygame.font.Font(None, 40)
        
        text = font_popup.render("{} win!!".format(winner), True, BLACK)
        text2 = font_popup.render("Play again?", True, BLACK)
        window.blit(text, (popup_rect.x + 20, popup_rect.y + 20))
        window.blit(text2, (popup_rect.x + 20, popup_rect.y + 50))
        
        # Draw the buttons
        yes_button_rect = pygame.Rect(popup_rect.x + 20, popup_rect.y + 90, 60, 40)
        no_button_rect = pygame.Rect(popup_rect.x + 120, popup_rect.y + 90, 60, 40)
        
        pygame.draw.rect(window, button_color, yes_button_rect)
        pygame.draw.rect(window, button_color, no_button_rect)
        
        yes_text = font_popup.render("Yes", True, BLACK)
        no_text = font_popup.render("No", True, BLACK)
        
        window.blit(yes_text, (yes_button_rect.x + 10, yes_button_rect.y + 5))
        window.blit(no_text, (no_button_rect.x + 15, no_button_rect.y + 5))
        
        
        pygame.display.update()
        return yes_button_rect, no_button_rect
    
    #===================================================================================================
    
    def handle_popup_events(yes_button_rect, no_button_rect):
        start_time = pygame.time.get_ticks()  # 開始時間を記録
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button_rect.collidepoint(event.pos):
                        return True
                    if no_button_rect.collidepoint(event.pos):
                        return False
            current_time = pygame.time.get_ticks()
            if current_time - start_time > 5000:  # 5秒待つ
                break
        return False
                
                
    #===================================================================================================
    
    
    def show_play(play_area, inputter=0, inputted=0):
        
        '''
        TIC TAC TOEの画面を表示する関数

        表示すべきリスト(1～9の数値、○、×から成る)と
        直前の入力者および入力を受け取り、表示する
        '''
        
    
        window.fill(WHITE)
        for i in range(0, 9, 3):
            for j in range(3):
                text = font.render(str(play_area[i + j]), True, BLACK)
                window.blit(text, (j * 100 + 50, i // 3 * 100 + 50))
        pygame.display.update()
    
    
    #===================================================================================================
        
    def judge(play_area, inputter):
        '''
        ゲーム終了及び勝者を判定する

        ゲームの状況をあらわすリストと直前の入力者を受け取り、
        ゲームが終了していれば勝者と終了判定を返す
        '''
        
        end_flg = 0
        winner = "NOBODY"
        
        first_list = [0, 3, 6, 0, 1, 2, 0, 2]
        second_list = [1, 4, 7, 3, 4, 5, 4, 4]
        third_list = [2, 5, 8, 6, 7, 8, 8, 6]
        
        for first, second, third in zip(first_list, second_list, third_list):
            if play_area[first] == play_area[second] == play_area[third]:
                
                winner = inputter
                end_flg = 1
                break
        
        choosable_area = [str(area) for area in play_area if type(area) is int]
        if len(choosable_area) == 0 :
            end_flg = 1
            
        return winner, end_flg
                
        
        #===================================================================================================
        
                
    def player_vs_randomAI(first_inputter):
        """
        プレイヤーとAI(ランダム)のゲームを実行する関数

        先手(1:プレイヤー、2:AI)を受け取り、ゲームが終了するまで実行する
        """
        from Q_Learning import QLearning
        
        inputter1 = 'YOU'
        inputter2 = 'AI'

        play_area = list(range(1, 10))
        gameManager.show_play(play_area)
        inputter_count = first_inputter
        end_flg = 0
        while True:
            if (inputter_count % 2) == 1:
                print('Your turn!')
                play_area, player_input = QLearning.get_player_input(play_area, first_inputter)
                gameManager.show_play(play_area, inputter1, player_input)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                if end_flg:
                    break
            elif (inputter_count % 2) == 0:
                print('AI\'s turn!\n.\n.\n.')
                play_area, ai_input = QLearning.get_AI_input(play_area, first_inputter, mode=0)
                sleep(3)
                gameManager.show_play(play_area, inputter2, ai_input)
                winner, end_flg = gameManager.judge(play_area, inputter2)
                if end_flg:
                    break
            inputter_count += 1
            
        print('{} win!!!'.format(winner))
        
        
#===================================================================================================
        
        
    def make_q_table():
        '''
        Qテーブルを作成する関数
        '''
        n_columns = 9
        n_rows = 3 ** 9
        return np.zeros((n_rows, n_columns))

    #===================================================================================================

    def randomAI_vs_QLAI(self, first_inputter, q_table, epsilon=0):
        """
        AI(ランダム)とAI(Q学習)のゲームを実行する関数

        先手(1:AI(ランダム)、2:AI(Q学習))とQテーブルを受け取り、
        ゲームが終了するまで実行する
        """
        from Q_Learning import QLearning
        inputter1 = 'Random AI'
        inputter2 = 'QL AI'

        # Q学習退避用
        ql_input_list = []
        play_area_list = []

        play_area = list(range(1, 10))
        #show_play(play_area)
        inputter_count = first_inputter
        end_flg = 0
        ql_flg = 0
        reward = 0
        
        while True:
            # Q学習退避用
            play_area_tmp = play_area.copy()
            play_area_list.append(play_area_tmp)
            # Q学習実行フラグ
            ql_flg = 0
            # AI(Q学習)の手番
            if (inputter_count % 2) == 0:
                # QL AI入力
                play_area, ql_ai_input = get_input.get_AI_input(play_area, 
                                                    first_inputter,
                                                    mode=1, 
                                                    q_table=q_table, 
                                                    epsilon=epsilon)
                winner, end_flg = gameManager.judge(play_area, inputter2)
                # Q学習退避用
                ql_input_list.append(ql_ai_input)            
                # 勝利した場合
                if winner == inputter2:
                    reward = 1
                    ql_flg = 1
                play_area_before = play_area_list[-1]
                ql_ai_input_before = ql_input_list[-1]
                
            # AI(ランダム)の手番
            elif (inputter_count % 2) == 1:
                play_area, random_ai_input = get_input.get_AI_input(play_area, 
                                                        first_inputter+1, 
                                                        mode=0)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                # AI(ランダム)が先手の場合の初手以外は学習
                if inputter_count != 1:
                    ql_flg = 1
            # Q学習実行
            if ql_flg == 1:
                ql_ai_input_before = ql_input_list[-1]
                q_table = QLearning.q_learning(play_area_before, ql_ai_input_before,
                                    reward, play_area, q_table, end_flg)
            if end_flg:
                break
            
            inputter_count += 1
        #print('{} win!!!'.format(winner))
        return winner, q_table
    
    #===================================================================================================
    
    def QLAI_vs_QLAI(self, first_inputter, q_table1, q_table2, epsilon=0):
        
        from Q_Learning import QLearning
        inputter1 = 'QL AI1'
        inputter2 = 'QL AI2'

        ql_input_list1 = []
        play_area_list1 = []
        
        ql_input_list2 = []
        play_area_list2 = []

        play_area = list(range(1, 10))
        inputter_count = first_inputter
        end_flg = 0
        reward1 = 0
        reward2 = 0
        
        while True:
            play_area_tmp = play_area.copy()
            
            if (inputter_count % 2) == 0:
                play_area_list1.append(play_area_tmp)
                play_area, ql_ai_input = get_input.get_AI_input(play_area, first_inputter, mode=1, q_table=q_table1, epsilon=epsilon)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                ql_input_list1.append(ql_ai_input)
                if winner == inputter1:
                    reward1 = 1
                    
            elif (inputter_count % 2) == 1:
                play_area_list2.append(play_area_tmp)
                play_area, ql_ai_input = get_input.get_AI_input(play_area, first_inputter + 1, mode=1, q_table=q_table2, epsilon=epsilon)
                winner, end_flg = gameManager.judge(play_area, inputter2)
                ql_input_list2.append(ql_ai_input)
                if winner == inputter2:
                    reward2 = 0
                if end_flg:
                    reward1 = -1
                    
            if end_flg:
                ql_ai_input_before1 = ql_input_list1[-1]
                play_area_before1 = play_area_list1[-1]
                #ql_ai_input_before2 = ql_input_list2[-1]
                #play_area_before2 = play_area_list2[-1]
                q_table1 = QLearning.q_learning(play_area_before1, ql_ai_input_before1, reward1, play_area, q_table1, end_flg)
                #q_table2 = QLearning.q_learning(play_area_before2, ql_ai_input_before2, reward2, play_area, q_table2, end_flg)
                break
            
            
            inputter_count += 1

        #print('{} win!!!'.format(winner))
        return winner, q_table1
        


    #===================================================================================================

    def player_vs_QLAI(self, first_inputter, q_table, epsilon = 0):
        """
        プレイヤーとAI(Q学習)のゲームを実行する関数

        先手(1:プレイヤー)、2:AI(Q学習))を受け取り、ゲームが終了するまで実行する
        """
        from Q_Learning import QLearning
        inputter1 = 'YOU'
        inputter2 = 'QL AI'

        # Q学習退避用
        ql_input_list = []
        play_area_list = []

        play_area = list(range(1, 10))
        
        gameManager.show_play(play_area)
        inputter_count = first_inputter
        end_flg = 0
        ql_flg = 0
        reward = 0
        while True:
            # Q学習退避用
            play_area_tmp = play_area.copy()
            play_area_list.append(play_area_tmp)
            # Q学習実行フラグ
            ql_flg = 0
            # AI(Q学習)の手番
            if (inputter_count % 2) == 0:
                # QL AI入力
                play_area, ql_ai_input = get_input.get_AI_input(play_area, 
                                                    first_inputter,
                                                    mode=1, 
                                                    q_table=q_table, 
                                                    epsilon=epsilon)
                gameManager.show_play(play_area, inputter2, ql_ai_input)
                winner, end_flg = gameManager.judge(play_area, inputter2)
                # Q学習退避用
                ql_input_list.append(ql_ai_input)            
                # 勝利した場合
                if winner == inputter2:
                    reward = 1
                    ql_flg = 1
                play_area_before = play_area_list[-1]
                ql_ai_input_before = ql_input_list[-1]
            # プレイヤーの手番
            elif (inputter_count % 2) == 1:
                print('Your turn!')
                # プレイヤーの入力受付
                play_area, player_input = get_input.get_player_input(play_area, first_inputter)
                gameManager.show_play(play_area, inputter1, player_input)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                # プレイヤーが勝利した場合
                if winner == inputter1:
                    reward = -1
                # プレイヤーが先手の場合の初手以外は学習
                if inputter_count != 1:
                    ql_flg = 1
            # Q学習実行
            if ql_flg == 1:
    #            print('Q学習')
                ql_ai_input_before = ql_input_list[-1]
                q_table = QLearning.q_learning(play_area_before, ql_ai_input_before,
                                    reward, play_area, q_table, end_flg)
                
            if end_flg:
                break
            
            inputter_count += 1
        gameManager.show_play(play_area)
        print('{} win!!!'.format(winner))
        sleep(1)
        return winner, q_table
    
    #===================================================================================================
    
    def player_vs_player(self, first_inputter):
        """
        プレイヤーとプレイヤーのゲームを実行する関数

        先手(1:プレイヤー1、2:プレイヤー2)を受け取り、ゲームが終了するまで実行する
        """
        inputter1 = 'Player1'
        inputter2 = 'Player2'

        play_area = list(range(1, 10))
        gameManager.show_play(play_area)
        inputter_count = first_inputter
        end_flg = 0
        while True:
            if (inputter_count % 2) == 1:
                print('Player1\'s turn!')
                play_area, player_input = get_input.get_player_input(play_area, first_inputter)
                gameManager.show_play(play_area, inputter1, player_input)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                if end_flg:
                    break
            elif (inputter_count % 2) == 0:
                print('Player2\'s turn!')
                play_area, player_input = get_input.get_player_input(play_area, first_inputter+1)
                gameManager.show_play(play_area, inputter2, player_input)
                winner, end_flg = gameManager.judge(play_area, inputter2)
                if end_flg:
                    break
            inputter_count += 1
        print('{} win!!!'.format(winner))