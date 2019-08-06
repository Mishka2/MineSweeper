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
                self.board[row_num].append(EmptyPiece())

        # print("Bomb_coor: " + str(self.bombs))

        for bomb_coor in self.bombs:
            # print("board coor: " + str(self.board[0][0].get_char()))
            self.board[bomb_coor[0]][bomb_coor[1]] = Bomb()
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
        #original = board[bomb[0]][bomb[1]]
        # print("board coor: " + str(board[0][0]) + " coor: " + str([bomb[0]-1,bomb[1]-1]) + " In board? " + str([bomb[0]-1,bomb[1]-1] in board))
        # print("HELLO")
        if(bomb[0]-1 in self.get_x_dim() and bomb[1]-1 in self.get_y_dim() and board[bomb[0]-1][bomb[1]-1].get_name() != 'bomb'):
            #top left
            if board[bomb[0]-1][bomb[1]-1].get_name() != 'number':
                board[bomb[0]-1][bomb[1]-1] = NumberPiece()

            board[bomb[0]-1][bomb[1]-1].add_near_bomb()

        if(bomb[0]-1 in self.get_x_dim() and bomb[1] in self.get_y_dim() and board[bomb[0]-1][bomb[1]].get_name() != 'bomb'):
            #top mid
            if board[bomb[0]-1][bomb[1]].get_name() != 'number':
                board[bomb[0]-1][bomb[1]] = NumberPiece()

            board[bomb[0]-1][bomb[1]].add_near_bomb()


        if(bomb[0]-1 in self.get_x_dim() and bomb[1]+1 in self.get_y_dim() and board[bomb[0]-1][bomb[1]+1].get_name() != 'bomb'):
            #top right
            if board[bomb[0]-1][bomb[1]+1].get_name() != 'number':
                board[bomb[0]-1][bomb[1]+1]= NumberPiece()

            board[bomb[0]-1][bomb[1]+1].add_near_bomb()

        if(bomb[0] in self.get_x_dim() and bomb[1]-1 in self.get_y_dim() and board[bomb[0]][bomb[1]-1].get_name() != 'bomb'):
            #left
            if board[bomb[0]][bomb[1]-1].get_name() != 'number':
                board[bomb[0]][bomb[1]-1]= NumberPiece()

            board[bomb[0]][bomb[1]-1].add_near_bomb()

        if(bomb[0] in self.get_x_dim() and bomb[1]+1 in self.get_y_dim() and board[bomb[0]][bomb[1]+1].get_name() != 'bomb'):
            #right
            if board[bomb[0]][bomb[1]+1].get_name() != 'number':
                board[bomb[0]][bomb[1]+1] = NumberPiece()

            board[bomb[0]][bomb[1]+1].add_near_bomb()

        if(bomb[0]+1 in self.get_x_dim() and bomb[1]-1 in self.get_y_dim() and board[bomb[0]+1][bomb[1]-1].get_name() != 'bomb'):
            #bottom left
            if board[bomb[0]+1][bomb[1]-1].get_name() != 'number':
                board[bomb[0]+1][bomb[1]-1] = NumberPiece()

            board[bomb[0]+1][bomb[1]-1].add_near_bomb()

        if(bomb[0]+1 in self.get_x_dim() and bomb[1] in self.get_y_dim() and board[bomb[0]+1][bomb[1]].get_name() != 'bomb'):
            #bottom mid
            if board[bomb[0]+1][bomb[1]].get_name() != 'number':
                board[bomb[0]+1][bomb[1]] = NumberPiece()

            board[bomb[0]+1][bomb[1]].add_near_bomb()

        if(bomb[0]+1 in self.get_x_dim() and bomb[1]+1 in self.get_y_dim() and board[bomb[0]+1][bomb[1]+1].get_name() != 'bomb'):
            #bottom right
            if board[bomb[0]+1][bomb[1]+1].get_name() != 'number':
                board[bomb[0]+1][bomb[1]+1] = NumberPiece()

            board[bomb[0]+1][bomb[1]+1].add_near_bomb()


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
                print(Style.RESET_ALL, end = '')
            elif(item.get_hidden_state()):
                #if the item is hidden
                print(Fore.BLUE + ' ' + str(item.get_hidden_name()) + ' ', end = end)
                print(Style.RESET_ALL, end = '')
            else:
                #if the item is not hidden
                item.print_color()
                print(' ' + str(item.get_hidden_name()) + ' ', end = end)
                print(Style.RESET_ALL, end = '')

        else:
            #if the cursor is on the item
            if(item.get_flagged_state()):
                print(Back.CYAN + Fore.RED + ' ' + str(item.get_hidden_name()) , end = end)
                print(Style.RESET_ALL + ' ', end = '')
            elif(item.get_name() == 'bomb' and not item.get_hidden_state()):
                print(Style.BRIGHT + Fore.RED + ' ' + str(item.get_hidden_name()) + ' ', end = end)
                print(Style.RESET_ALL, end = '')
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
                if( not item.get_hidden_state() and (item.get_name() == 'number' or item.get_name() == 'empty')):
                    count_not_bombs += 1
                counter += 1
            print(' ')

        if count_not_bombs == (self.rows * self.columns) - self.num_bombs:
            self.board_win = True

        if self.display_rules:
            print(' ')
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

#
class Bomb():

    def __init__(self):
        self.char = '\u203B'
        self.cursor_state = False
        self.flagged_state = False
        self.hidden_state = True
        self.name = "bomb"
        self.display_name = '?'
        self.previous_display_name = ''

    def get_flagged_state(self):
        return self.flagged_state

    def switch_flagged_state(self):
        # print("previous: " + self.display_name)

        self.flagged_state = not self.flagged_state
        if(self.flagged_state):
            self.previous_display_name = self.display_name
            self.display_name = '\u2691'
        else:
            self.display_name = self.previous_display_name

    def print_color(self):
        print(Fore.RED, end = '')

    def get_name(self):
        return self.name

    def set_hidden_state(self, bool):
        self.hidden_state = bool

    def get_hidden_state(self):
        return self.hidden_state

    def get_cursor_state(self):
        return self.cursor_state

    def set_cursor_state(self, state):
        self.cursor_state = state

    def get_char(self):
        return self.char

    def get_hidden_name(self):
        return self.display_name

    def set_display_name(self):
        self.display_name = self.char

class EmptyPiece():

    def __init__(self):
        self.char = '\u25A2'
        # self.char = ' '
        self.cursor_state = False
        self.flagged_state = False
        self.hidden_state = True
        self.name = "empty"
        self.display_name = '?'

    def get_flagged_state(self):
        return self.flagged_state

    def switch_flagged_state(self):
        # print("previous: " + self.display_name)

        self.flagged_state = not self.flagged_state
        if(self.flagged_state):
            self.previous_display_name = self.display_name
            self.display_name = '\u2691'
        else:
            self.display_name = self.previous_display_name

    def get_name(self):
        return self.name

    def print_color(self):
        print(Fore.WHITE, end = '')

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

    def set_hidden_state(self, bool):
        self.hidden_state = bool

    def set_cursor_state(self, state):
        self.cursor_state = state

class NumberPiece():

    def __init__(self):
        self.char = 0
        self.name = "number"
        self.cursor_state = False
        self.flagged_state = False
        self.hidden_state = True
        self.display_name = '?'

    def get_flagged_state(self):
        return self.flagged_state

    def switch_flagged_state(self):
        # print("previous: " + self.display_name)

        self.flagged_state = not self.flagged_state
        if(self.flagged_state):
            self.previous_display_name = self.display_name
            self.display_name = '\u2691'
        else:
            self.display_name = self.previous_display_name

    def get_name(self):
        return self.name

    def print_color(self):
        print(Fore.GREEN, end = '')

    def get_hidden_state(self):
        return self.hidden_state

    def set_hidden_state(self, bool):
        self.hidden_state = bool

    def get_cursor_state(self):
        return self.cursor_state

    def get_char(self):
        return self.char

    def set_cursor_state(self, state):
        self.cursor_state = state

    def add_near_bomb(self):
        self.char += 1

    def get_hidden_name(self):
        return self.display_name

    def set_display_name(self):
        self.display_name = self.char


class MineGame():

    def __init__(self, xdim, ydim, num_bombs):
        self.rows = xdim
        self.columns = ydim

        self.board = Board(xdim,ydim, num_bombs)
        self.cursor_coor = [0,0]

        self.moving_cursor = False
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
        self.check_endgame()
        self.board.display_board()


    def check_win(self):
        self.win = self.board.get_board_win()
        print(self.win)

    def check_cursor_movement(self):
        arrows = ["up", "down", "left", "right", "r"]
        pressed = False
        for arrow in arrows:
            pressed = keyboard.is_pressed(arrow)
            if pressed:
                self.move_cursor(arrow)
                self.moving_cursor = True
            else:
                self.moving_cursor = False

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
        # self.lose = True

    def enter_play(self, coor):
        self.board.board[coor[0]][coor[1]].set_display_name()
        self.board.board[coor[0]][coor[1]].set_hidden_state(False)

        if (self.board.board[coor[0]][coor[1]].get_name() == 'bomb'):
            self.board.expose_board()
            self.board.display_board()
            self.lose = True
        elif (self.board.board[coor[0]][coor[1]].get_name() == 'empty'):
            self.clear_surrounding_squares(coor, 0)

    def clear_surrounding_squares(self, coor, num_numbers):

        if(self.board.board[coor[0]][coor[1]].get_name() == 'empty' or
            (self.board.board[coor[0]][coor[1]].get_name() == 'number' and
            num_numbers == 0)):

            self.board.board[coor[0]][coor[1]].set_display_name()
            self.board.board[coor[0]][coor[1]].set_hidden_state(False)

            if(self.board.board[coor[0]][coor[1]].get_name() == 'number'):
                num_numbers += 1
            if(self.board.board[coor[0]][coor[1]].get_name() == 'empty'):
                num_numbers = 0
            # print("times: " + str(self.recursion))

            ###CHECKING TOP BOTTOM LEFT RIGHT

            #check middle top
            if(coor[0]-1 in self.board.get_x_dim() and
                coor[1] in self.board.get_y_dim() and
                self.board.board[coor[0]-1][coor[1]].get_hidden_state()):
                self.clear_surrounding_squares([coor[0]-1,coor[1]], num_numbers)

            #check left
            if(coor[0] in self.board.get_x_dim() and coor[1]-1 in self.board.get_y_dim() and
                self.board.board[coor[0]][coor[1]-1].get_hidden_state()):
                self.clear_surrounding_squares([coor[0],coor[1]-1], num_numbers)

            #check right
            if(coor[0] in self.board.get_x_dim() and coor[1]+1 in self.board.get_y_dim() and
                self.board.board[coor[0]][coor[1]+1].get_hidden_state()):
                self.clear_surrounding_squares([coor[0],coor[1]+1], num_numbers)

            #check middle bottom
            if(coor[0]+1 in self.board.get_x_dim() and coor[1] in self.board.get_y_dim() and
                self.board.board[coor[0]+1][coor[1]].get_hidden_state()):
                self.clear_surrounding_squares([coor[0]+1,coor[1]], num_numbers)


            ###CHECKING DIAGONALS FOR NUMBERS ONLY
            if(self.board.board[coor[0]][coor[1]].get_name() == 'empty'):
                #check left bottom
                if(coor[0]+1 in self.board.get_x_dim() and coor[1]-1 in self.board.get_y_dim() and
                    self.board.board[coor[0]+1][coor[1]-1].get_name() == 'number'):

                    self.board.board[coor[0]+1][coor[1]-1].set_display_name()
                    self.board.board[coor[0]+1][coor[1]-1].set_hidden_state(False)

                #check right bottom
                if(coor[0]+1 in self.board.get_x_dim() and coor[1]+1 in self.board.get_y_dim() and
                    self.board.board[coor[0]+1][coor[1]+1].get_name() == 'number'):

                    self.board.board[coor[0]+1][coor[1]+1].set_display_name()
                    self.board.board[coor[0]+1][coor[1]+1].set_hidden_state(False)

                #check top left
                if(coor[0]-1 in self.board.get_x_dim() and coor[1]-1 in self.board.get_y_dim() and
                    self.board.board[coor[0]-1][coor[1]-1].get_name() == 'number'):

                    self.board.board[coor[0]-1][coor[1]-1].set_display_name()
                    self.board.board[coor[0]-1][coor[1]-1].set_hidden_state(False)

                #check top right
                if(coor[0]-1 in self.board.get_x_dim() and coor[1]+1 in self.board.get_y_dim() and
                    self.board.board[coor[0]-1][coor[1]+1].get_name() == 'number'):

                    self.board.board[coor[0]-1][coor[1]+1].set_display_name()
                    self.board.board[coor[0]-1][coor[1]+1].set_hidden_state(False)


    def add_to_cursor(self, points):
        #if the cursor CAN move there
        old_cursor_coor = [self.cursor_coor[0],self.cursor_coor[1]]
        above = self.cursor_coor[0] + points[0]
        side = self.cursor_coor[1] + points[1]
        if( (0 <= above and above < self.rows) and (0 <= side and side < self.columns)):
            self.cursor_coor[0] += points[0]
            self.cursor_coor[1] += points[1]
            new_cursor_coor = [self.cursor_coor[0],self.cursor_coor[1]]

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
    #rows, columns
    game = MineGame(10,10, 2)

    # game.run_game()

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
