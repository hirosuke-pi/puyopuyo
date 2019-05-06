import os, sys
import random
import copy
import time
import threading
from graphics import *

class GraphicBoard:

    def __init__(self):
        self.moving_flag = True
        self.removing_puyo_list = []
        self.__board = [[0, 0, 0, 0, 0, 0] for i in range(14)]
        self.__check_list = ((0, -1), (-1, 0), (0, 1), (1, 0))
        self.__check_dic = {self.__check_list[0] : 0, self.__check_list[1] : 1,
        self.__check_list[2] : 2, self.__check_list[3] : 3}
        self.__drawing = False

        self.all_clear = False
        self.chain_val = 0
        self.max_chain_val = 0
        self.score = 0
        self.board_x = len(self.__board[0])
        self.board_y = len(self.__board)
        self.puyo = [[0, 0, 0], [0, 0, 0]]
        self.puyo1 = [[0, 0, 0], [0, 0, 0]]
        self.puyo2 = [[0, 0, 0], [0, 0, 0]]

        self.chain_bonus_dict = { 1:0, 2:8, 3:16, 4:32, 5:64, 7:128, 8:160, 9:192, 10:224, 11:256, 12:288, 13:320, 14:352, 15:384, 16:416, 17:448, 18:480, 19:512 }
        self.link_bonus_dict = { 4:0, 5:2, 6:3, 7:4, 8:5, 9:6, 10:7, 11:10 }
        self.color_bonus_dict = { 1:0, 2:3, 3:6, 4:12, 5:24 }
        self.set_next_puyo()

    def __reload_gmaover_line(self):
        self.__board[0][2] = -8
        

    def __get_filled_puyo_x(self, puyo, x, count, now_line, max_line):
        if (max_line <= now_line and x > 0) or (max_line >= now_line and x < 0):
            return count

        puyo_status = self.__board[puyo[2]][puyo[1] + now_line]
        if puyo_status == 0:
            count += 1
        elif puyo_status > 0:
            return count
        now_line += x
        return self.__get_filled_puyo_x(puyo, x, count, now_line, max_line)
    

    def __get_filled_puyo_y(self, puyo, y, count, now_line, max_line):
        if max_line <= now_line:
            return count

        puyo_status = self.__board[puyo[2] + now_line][puyo[1]]
        if puyo_status == 0:
            count += 1
        elif puyo_status > 0:
            return count
        now_line += y
        return self.__get_filled_puyo_y(puyo, y, count, now_line, max_line)


    def check_puyo_active(self, puyo_list):
        for puyo in puyo_list:
            if puyo[0] < 0:
                return True
        return False


    def contain_puyo_in_board(self, x, y):
        if 0 <= x < self.board_x:
            if 0 <= y < self.board_y:
                return self.__board[y][x] == 0
        return False

    def __contain_puyo_list(self, puyo_list, original_puyo_list):
        for puyo in original_puyo_list:
            if puyo[0] == puyo_list[0]:
                if puyo[1] == puyo_list[1]:
                    if puyo[2] == puyo_list[2]:
                        #print(puyo)
                        return True
        return False


    def __remove_overlapping_puyo(self, puyo_list):
        tmp_puyo_list = []
        for puyo in puyo_list:
            if not(self.__contain_puyo_list(puyo, tmp_puyo_list)):
                tmp_puyo_list.append(puyo)
        return tmp_puyo_list
    

    def __check_chain(self, x, y, color):
        for check_grid in self.__check_list:
            c_x = x + check_grid[0]
            c_y = y + check_grid[1]
            if (0 <= c_x < self.board_x) and (0 <= c_y < self.board_y):
                if self.__board[c_y][c_x] == color and not(self.__contain_puyo_list([color, c_x, c_y], self.removing_puyo_list)):
                    self.removing_puyo_list.append([color, c_x, c_y])
                    self.__check_chain(c_x, c_y, color)

    
    def check_gameover(self):
        if self.__board[0][2] > 0:
            return True
        else:
            return False


    def check_all_clear(self):
        for y in range(self.board_y):
            for x in range(self.board_x):
                color = self.__board[y][x]
                if color != 0:
                    if color != -8:
                        self.all_clear = False
                        return
        self.all_clear = True
        self.score = self.score + 2100


    def check_puyo_chain(self):
        puyo_list = []
        for y in range(self.board_y):
            for x in range(self.board_x):
                color = self.__board[y][x]
                if color > 1 and not(self.__contain_puyo_list([color, x, y], puyo_list)):
                    self.removing_puyo_list = []
                    self.__check_chain(x, y, color)
                    if len(self.removing_puyo_list) > 3:
                        puyo_list.extend(self.removing_puyo_list)

        #print("end: "+ str(puyo_list))
        return puyo_list


    def refresh_board(self):
        for x in range(self.board_x):
            line_puyo = ""
            for y in reversed(range(self.board_y)):
                line_puyo += str(self.__board[y][x])
                self.remove_puyo([[self.__board[y][x], x, y]])
            line_puyo_list = line_puyo.replace("0", "").ljust(self.board_y, "0")
            y3 = 0
            for y2 in reversed(range(self.board_y)):
                self.add_puyo([[int(line_puyo_list[y3]), x, y2]])
                y3 += 1


    def draw_ex(self):
        if self.__drawing:
            return
        self.__drawing = True

        space = "    "
        raw_data = [[["", "n", "n"]],[["", "n", "n"]], [[space, "n", "n"], ["+                        +", "n", "n"]]]
        for y in range(self.board_y):
            line_data = [[space, "n", "n"], ["|", "n", "w"]]
            for x in range(self.board_x):
                puyo = self.get_num2puyo(self.__board[y][x])
                if self.__board[y][x] > -8:
                    line_data.append([puyo[0:4], puyo[4], "n"])
                else:
                    line_data.append([puyo[0:4], puyo[4], "n"])
            line_data.append(["|", "n", "w"])
            raw_data.extend([line_data])
        raw_data.append([[space, "n", "n"], ["+------------------------+", "n", "w"]])
        
        puyo1_c1 = self.get_num2puyo(self.puyo1[0][0])
        puyo1_c2 = self.get_num2puyo(self.puyo1[1][0])
        puyo2_c1 = self.get_num2puyo(self.puyo2[0][0])
        puyo2_c2 = self.get_num2puyo(self.puyo2[1][0])

        raw_data[2].append(["   [1]", "n", "n"])
        raw_data[3].append(["   +----+", "n", "n"])
        raw_data[4].extend([["   |", "n", "n"], [puyo1_c2[0:4], "k", puyo1_c2[4]], ["|", "n", "n"]])
        raw_data[5].extend([["   |", "n", "n"], [puyo1_c1[0:4], "k", puyo1_c1[4]], ["|", "n", "n"]])
        raw_data[6].append(["   +----+", "n", "n"])
        raw_data[8].append(["   [2]", "n", "n"])
        raw_data[9].append(["   +----+", "n", "n"])
        raw_data[10].extend([["   |", "n", "n"], [puyo2_c2[0:4], "k", puyo2_c2[4]], ["|", "n", "n"]])
        raw_data[11].extend([["   |", "n", "n"], [puyo2_c1[0:4], "k", puyo2_c1[4]], ["|", "n", "n"]])
        raw_data[12].append(["   +----+", "n", "n"])  
        raw_data[14].append(["   "+ str(self.chain_val) + " Chain", "W", "n"]) 
        raw_data[16].append(["   [MAX: "+ str(self.max_chain_val) + " Chain]", "G", "n"]) 
        raw_data.append([["    ", "n", "n"], [" SCORE: "+ str(self.score) +" ", "k", "w"], ["", "", ""]])

        if self.all_clear:
            raw_data[18].extend([["   [ALL CLEAR!!]", "Y", "n"], ["", "", ""]])

        clear()

        #print(raw_data)
        cprint(raw_data)
        self.__drawing = False


    def draw(self):
        clear()
        print("                             ")
        print("   +                        +")
        for y in range(self.board_y):
            line = ""
            for x in range(self.board_x):
                line = line + self.get_num2puyo(self.__board[y][x])
            print("   |"+ line +"|")
        print("   +------------------------+")    


    def calc_score(self, puyo_chain_list):
        removing_puyo_val = len(puyo_chain_list)
        puyo_colors_bonus = 0
        puyo_link_bonus = 0

        # Make color count dict
        puyo_color_dict = {}
        for puyo in puyo_chain_list:
            if puyo[0] in puyo_color_dict.keys():
                puyo_color_dict[puyo[0]] += 1
            else:
                puyo_color_dict[puyo[0]] = 1
        puyo_colors_val = len(puyo_color_dict.keys())

        # Get color bonus
        if puyo_colors_val in self.color_bonus_dict.keys():
            puyo_colors_bonus = self.color_bonus_dict[puyo_colors_val]
        else:
            puyo_colors_bonus = self.color_bonus_dict[5]
        
        # Get link bonus
        for puyo_link in puyo_color_dict.values():
            if puyo_link in self.link_bonus_dict.keys():
               puyo_link_bonus += self.link_bonus_dict[puyo_link]
            else:
                puyo_link_bonus += self.link_bonus_dict[11]

        # Get chain bonus
        if self.chain_val in self.chain_bonus_dict.keys():
            chain_bonus = self.chain_bonus_dict[self.chain_val]
        else:
            chain_bonus = self.chain_bonus_dict[19]

        tmp_score = chain_bonus + puyo_link_bonus + puyo_colors_bonus

        if tmp_score > 0:
            self.score = self.score + (removing_puyo_val * 10 * tmp_score)
        else:
            self.score = self.score + (removing_puyo_val * 10)



    def replace_puyo(self, replace_direction):
        #((0, -1), (-1, 0), (0, 1), (1, 0))
        puyo_moving_list_l = ((-1, 0), (0, 1), (1, 0), (0, -1))
        puyo_moving_list_r = ((1, 0), (0, -1), (-1, 0), (0, 1))

        x = self.puyo[1][1] - self.puyo[0][1]
        y = self.puyo[1][2] - self.puyo[0][2]
        tmp_puyo_list = [[0, 0, 0], [0, 0, 0]]
        now_grid = self.__check_dic[(x, y)]
        exit_flag = 0
        
        while True:
            if now_grid == 4: now_grid = 0
            elif now_grid == -1: now_grid = 3
            #print(now_grid)
            #print(self.puyo)

            tmp_puyo_list[0] = self.puyo[0]
            tmp_puyo_list[1][0] = self.puyo[1][0]
            if replace_direction: # L
                tmp_puyo_list[1][1] = self.puyo[0][1] + puyo_moving_list_l[now_grid][0]
                tmp_puyo_list[1][2] = self.puyo[0][2] + puyo_moving_list_l[now_grid][1]
                now_grid = self.__check_dic[(x, y)] + 1
            else: # R
                tmp_puyo_list[1][1] = self.puyo[0][1] + puyo_moving_list_r[now_grid][0]
                tmp_puyo_list[1][2] = self.puyo[0][2] + puyo_moving_list_r[now_grid][1]  
                now_grid = self.__check_dic[(x, y)] - 1      
            
            #print(tmp_puyo_list)
            if self.contain_puyo_in_board(tmp_puyo_list[1][1], tmp_puyo_list[1][2]):
                break
            if not(self.moving_flag) or exit_flag > 3:
                return
            exit_flag += 1
        
        self.remove_puyo(self.puyo)
        self.puyo = copy.deepcopy(tmp_puyo_list)
        self.add_puyo(tmp_puyo_list)


    def add_puyo(self, puyo_list):
        self.__reload_gmaover_line()
        for puyo in puyo_list:
            self.__board[puyo[2]][puyo[1]] = puyo[0]


    def remove_puyo(self, puyo_list, effect=False):
        self.__board[0][2] = 0
        if effect:
            for puyo in puyo_list:
                self.__board[puyo[2]][puyo[1]] = 7
            self.draw_ex()
            time.sleep(0.4)
            for puyo in puyo_list:
                self.__board[puyo[2]][puyo[1]] = 0
            sys.stdout.write("\a")
            self.draw_ex()
            time.sleep(0.4)
        else:
            for puyo in puyo_list:
                self.__board[puyo[2]][puyo[1]] = 0

    
    def move_puyo(self, x, y):  
        tmp_puyo_list = copy.deepcopy(self.puyo)
        for i in range(len(self.puyo)):
            moving_x = 0
            moving_y = 0
            if x > 0:
                moving_x = self.__get_filled_puyo_x(self.puyo[i], x, 0, 1, self.board_x - self.puyo[i][1])
            elif x < 0:
                moving_x = self.__get_filled_puyo_x(self.puyo[i], x, 0, -1, (self.puyo[i][1] * -1) - 1)
            if moving_x > 0:
                tmp_puyo_list[i][1] += x   

            if y > 0:
                moving_y = self.__get_filled_puyo_y(self.puyo[i], y, 0, 1, self.board_y - self.puyo[i][2])
                if moving_y < 1 and self.puyo[i][0] < 0:
                    self.moving_flag = False
                    tmp_puyo_list[i][0] *= -1

            if moving_y > 0:
                tmp_puyo_list[i][2] += y

        self.remove_puyo(self.puyo)
        self.puyo = copy.deepcopy(tmp_puyo_list)
        self.add_puyo(tmp_puyo_list)
        return tmp_puyo_list


    def set_next_puyo(self, puyo_val=0):
        if 0 < puyo_val < 6:
            self.__puyo_color_list = random.sample(range(-6, -1), puyo_val)
        else:
            self.__puyo_color_list = random.sample(range(-6, -1), 4)


    def make_next_puyo(self):
        return [[random.choice(self.__puyo_color_list), 2, 1], [random.choice(self.__puyo_color_list), 2, 0]]


    def get_num2puyo(self, num):
        if num == 0: return "    n"
        elif num == 1 or num == -1: return "(**)w"
        elif num == 2 or num == -2: return "(><)R"
        elif num == 3 or num == -3: return "('')G"
        elif num == 4 or num == -4: return "(;;)B"
        elif num == 5 or num == -5: return "(^^)Y"
        elif num == 6 or num == -6: return "(--)M"
        elif num == 7 or num == -7: return "(oo)W"
        elif num == -8: return "><><R"
