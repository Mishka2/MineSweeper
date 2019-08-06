"""
Author: Michelle Loven https://github.com/Mishka2/MineSweeper
Date created: Augut 2, 2019
Last edited: August 5, 2019

Mine sweeper game!
>>> *pip install keyboard*
>>> sudo python mine_sweeper.py
"""

import random
import os
import keyboard
from colorama import Fore, Back, Style
import time


class Board():

    def __init__(self, rows, columns, num_bombs):
        self.rows = rows
        self.columns = columns
        self.num_bombs = num_bombs
        self.board = []
        self.board_win = False
        self.cursor = [0,0]

        self.display_rules = True

        self.bombs = self.make_random_bombs(num_bombs)

        for row_num in range(rows):
            self.board.append([])

        for row_num in range(len(self.board)):
            for column_num in range(columns):
                self.board[row_num].append(TilePiece('empty'))

        for bomb_coor in self.bombs:
            self.board[bomb_coor[0]][bomb_coor[1]] = TilePiece('bomb')
            self.set_num_pieces(self.board, bomb_coor)

    def get_board_win(self):
        return self.board_win

    def get_x_dim(self):
        x_arr = []
        for index in range(self.rows):
            x_arr.append(index)

        return x_arr

    def get_y_dim(self):
        y_arr = []
        for index in range(self.columns):
            y_arr.append(index)

        return y_arr

    def set_num_pieces(self, board, bomb):
        """
        Checks every bomb and adds number pieces around each bomb coordinate
        board: the board array
        bomb: bomb coordinate
        """
        #direction_array = top left, middle top, top right, left, right, left bottom, middle bottom, right bottom
        direction_array = [[-1,-1], [-1, 0], [-1, 1], [0,-1], [0,1], [1, -1], [1,0], [1,1]]

        for direction in direction_array:
            x_dir = bomb[0] + direction[0]
            y_dir = bomb[1] + direction[1]

            if x_dir in self.get_x_dim() and y_dir in self.get_y_dim():
                if board[x_dir][y_dir].get_name() != 'bomb':
                    if board[x_dir][y_dir].get_name() != 'number':
                        board[x_dir][y_dir] = TilePiece('number')
                    board[x_dir][y_dir].add_near_bomb()

    def make_random_bombs(self, num):
        bombs = []

        for bomb in range(num):
            repeat = True

            while repeat:
                rand_x_num = random.randint(0,self.rows-1)
                rand_y_num = random.randint(0,self.columns-1)
                if not [rand_x_num, rand_y_num] in bombs:
                    repeat = False
            bombs.append([rand_x_num, rand_y_num])
        return bombs

    def set_color(self, item, end):
        if(not item.get_cursor_state()):
            #if the cursor is not on the item
            if(item.get_flagged_state()):
                print(Fore.RED + ' ' + str(item.get_hidden_name()) + ' ', end = end)
            elif(item.get_hidden_state()):
                #if the item is hidden
                print(Fore.BLUE + ' ' + str(item.get_hidden_name()) + ' ', end = end)
            else:
                #if the item is not hidden
                item.print_color()
                print(' ' + str(item.get_hidden_name()) + ' ', end = end)
        else:
            #if the cursor is on the item
            if(item.get_flagged_state()):
                print(Back.CYAN + Fore.RED + ' ' + str(item.get_hidden_name()) +  ' ', end = end)
            elif(item.get_name() == 'bomb' and not item.get_hidden_state()):
                print(Style.BRIGHT + Fore.RED + ' ' + str(item.get_hidden_name()) + ' ', end = end)
            else:
                print(Back.CYAN + Fore.WHITE + Style.BRIGHT + ' ' + str(item.get_hidden_name()) + ' ' + Style.RESET_ALL, end = end)

        print(Style.RESET_ALL, end = '')

        ###########FOR TESTING ONLY#################
        # if type(item.get_char())== int:
        #     if(not item.get_cursor_state()):
        #         print(Fore.GREEN + ' ' + str(item.get_hidden_name()) + ' ', end = end)
        #     else:
        #         print(Back.CYAN + Fore.WHITE + Style.BRIGHT + ' ' + str(item.get_hidden_name()) + ' ' + Style.RESET_ALL, end = end)
        # elif item.get_char() == 'B':
        #     if(not item.get_cursor_state()):
        #         print(Fore.RED + ' ' + item.get_hidden_name() + ' ', end = end)
        #     else:
        #         print(Back.RED + Fore.WHITE + Style.BRIGHT + ' ' + str(item.get_hidden_name()) + ' ' + Style.RESET_ALL, end = end)
        # elif item.get_char() == '\u25A2':
        #     if(not item.get_cursor_state()):
        #         print(Fore.WHITE + ' ' + item.get_hidden_name() + ' ', end = end)
        #     else:
        #         print(Back.CYAN + Fore.WHITE + Style.BRIGHT + ' ' + str(item.get_hidden_name()) + ' ' + Style.RESET_ALL, end = end)

    def display_board(self):
        count_not_bombs = 0
        os.system("clear")
        for row in range(len(self.board)):
            counter = 0
            for item in self.board[row]:
                if counter < self.columns-1:
                    self.set_color(item,' ')
                else:
                    self.set_color(item, None)
                if( not item.get_hidden_state() and (item.get_name() != 'bomb')):
                    count_not_bombs += 1
                counter += 1
            print(' ')

        if count_not_bombs == (self.rows * self.columns) - self.num_bombs:
            self.board_win = True

        if self.display_rules:
            print(Fore.GREEN + "Flag the " + Style.BRIGHT + Fore.RED +
                str(len(self.bombs)) + Style.RESET_ALL + Fore.GREEN + " bombs with 'space'!")

    def expose_board(self):
        self.display_rules = False
        for row in range(len(self.board)):
            counter = 0
            for item in self.board[row]:
                if counter < self.columns:
                    if item.get_name() == 'bomb':
                        item.set_display_name()
                        item.set_hidden_state(False)
                counter += 1

    def apply_cursor(self, old_coor, new_coor):
        self.board[old_coor[0]][old_coor[1]].set_cursor_state(False)
        self.board[new_coor[0]][new_coor[1]].set_cursor_state(True)


class TilePiece():

    def __init__(self, name):
        self.char = ''
        # self.char = ' '
        self.cursor_state = False
        self.flagged_state = False
        self.hidden_state = True
        self.name = name
        self.display_name = '?'

        self.set_char(name)

    def set_char(self, name):
        if name == 'empty':
            self.char = '\u25A2'
        elif name == 'bomb':
            self.char = '\u203B'
        elif name == 'number':
            self.char = 0

    def get_flagged_state(self):
        return self.flagged_state

    def switch_flagged_state(self):
        self.flagged_state = not self.flagged_state
        if(self.flagged_state):
            self.previous_display_name = self.display_name
            self.display_name = '\u2691'
        else:
            self.display_name = self.previous_display_name

    def get_name(self):
        return self.name

    def print_color(self):
        if self.name == 'empty':
            print(Fore.WHITE, end = '')
        elif self.name == 'bomb':
            print(Fore.RED, end = '')
        elif self.name == 'number':
            print(Fore.GREEN, end = '')

    def add_near_bomb(self):
        self.char += 1

    def get_hidden_state(self):
        return self.hidden_state

    def get_cursor_state(self):
        return self.cursor_state

    def get_char(self):
        return self.char

    def get_hidden_name(self):
        return self.display_name

    def set_display_name(self):
        self.display_name = self.char
        self.set_hidden_state(False)

    def set_hidden_state(self, bool):
        self.hidden_state = bool

    def set_cursor_state(self, state):
        self.cursor_state = state


class MineGame():

    def __init__(self, xdim, ydim, num_bombs):
        self.rows = xdim
        self.columns = ydim

        self.board = Board(xdim,ydim, num_bombs)
        self.cursor_coor = [0,0]

        self.lose = False
        self.win = False
        self.endgame = False

    def get_win(self):
        return self.win

    def check_endgame(self):
        return self.lose or self.win

    def get_lose(self):
        return self.lose

    def run_game(self):
        self.check_cursor_movement()
        self.board.display_board()
        self.check_enter()
        self.check_win()
        if(self.check_endgame()):
            self.board.display_board()

    def check_win(self):
        self.win = self.board.get_board_win()

    def check_cursor_movement(self):
        arrows = ["up", "down", "left", "right", "r"]
        pressed = False
        for arrow in arrows:
            pressed = keyboard.is_pressed(arrow)
            if pressed:
                self.move_cursor(arrow)

    def check_enter(self):
        coor = self.cursor_coor
        pressed_enter = keyboard.is_pressed("enter")
        pressed_space = keyboard.is_pressed("space")

        if pressed_enter:
            if not self.board.board[coor[0]][coor[1]].get_flagged_state():
                self.enter_play(coor)

        if pressed_space:
            self.space_play(coor)

    def space_play(self, coor):
        self.board.board[coor[0]][coor[1]].switch_flagged_state()

    def enter_play(self, coor):
        self.board.board[coor[0]][coor[1]].set_display_name()

        if (self.board.board[coor[0]][coor[1]].get_name() == 'bomb'):
            self.board.expose_board()
            self.board.display_board()
            self.lose = True
        elif (self.board.board[coor[0]][coor[1]].get_name() == 'empty'):
            self.clear_surrounding_squares(coor, 0)

    def clear_surrounding_squares(self, coor, num_numbers):
        current_coordinate = self.board.board[coor[0]][coor[1]]

        if(current_coordinate.get_name() == 'empty' or
            (current_coordinate.get_name() == 'number' and num_numbers == 0)):

            current_coordinate.set_display_name()

            if(current_coordinate.get_name() == 'number'):
                num_numbers += 1
            if(current_coordinate.get_name() == 'empty'):
                num_numbers = 0

            ###CHECKING ALL DIRECTIONS
            # all_dir = CHECKING TOP, LEFT, RIGHT, BOTTOM and then CHECKING DIAGONALS FOR NUMBERS ONLY
            all_directions = [[-1,0],[0,-1],[0,1],[1,0],   [1,-1],[1,1],[-1,-1],[-1,1]]

            for direction in all_directions:
                x_coor = coor[0] + direction[0]
                y_coor = coor[1] + direction[1]
                if(x_coor in self.board.get_x_dim() and y_coor in self.board.get_y_dim()):
                    if(direction in all_directions[:4] and self.board.board[x_coor][y_coor].get_hidden_state()):
                        self.clear_surrounding_squares([x_coor,y_coor], num_numbers)
                    elif(self.board.board[x_coor][y_coor].get_name() == 'number'):
                        self.board.board[x_coor][y_coor].set_display_name()

    def add_to_cursor(self, points):
        #if the cursor CAN move there
        old_cursor_coor = [self.cursor_coor[0],self.cursor_coor[1]]
        next_x = self.cursor_coor[0] + points[0]
        next_y = self.cursor_coor[1] + points[1]
        if( next_x in self.board.get_x_dim() and next_y in self.board.get_y_dim()):
            self.cursor_coor[0] = next_x
            self.cursor_coor[1] = next_y
            new_cursor_coor = self.cursor_coor

            self.board.apply_cursor(old_cursor_coor,new_cursor_coor)

    def move_cursor(self, dir):
        if dir == 'up':
            self.add_to_cursor([-1,0])
        elif dir == 'down':
            self.add_to_cursor([1,0])
        elif dir == 'right':
            self.add_to_cursor([0,1])
        elif dir == 'left':
            self.add_to_cursor([0,-1])


if __name__ == '__main__':
    #rows, columns, number of bombs
    game = MineGame(10,10, 10)

    while(not game.check_endgame()):
        game.run_game()
        time.sleep(.1)
        print(" ")

    if game.get_win():
        print(Fore.GREEN + "YOU WIN!")
    else:
        print(Fore.RED + "YOU LOSE!")

    while(True):
        time.sleep(10)
