# -----------------------------------------------------------------------------
# Name:       tictac
# Purpose:    Implement a game of Tic Tac Toe
#
# Author:   Zaw Mai (20005349)
# Data:     Dec 6, 2017
# -----------------------------------------------------------------------------
'''
Player vs Computer Tic-Tac-Toe Game using minimax decision rule algorithm
'''
import tkinter

import math


class Game(object):
    WINNING_STATES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # row
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # column
                      (0, 4, 8), (2, 4, 6))  # diagonal

    def __init__(self, parent):
        parent.title('Tic Tac Toe')
        # Create the restart button widget
        restart_btn = tkinter.Button(parent, text='RESTART',
                                     height=2, width=10, command=self.restart)
        restart_btn.grid()

        # Creates canvas and its rectangles objects for the tic-tac-toe
        # game board and store their references in a tuple. Loop by row.
        canvas = tkinter.Canvas(parent, width=600, height=600, bg='white')
        for i in range(3):
            y0 = i * 200
            y1 = (i + 1) * 200
            canvas.create_rectangle(0, y0, 200, y1)
            canvas.create_rectangle(200, y0, 400, y1)
            canvas.create_rectangle(400, y0, 600, y1)
        canvas.grid()
        canvas.bind("<Button-1>", self.play)

        # Create a label widget for the win/lose message
        result_string = tkinter.StringVar()
        tkinter.Label(parent, height=2, textvariable=result_string).grid()

        # initialize instance variables
        self.result = result_string # Tkinter string var to display game result
        self.canvas = canvas # Tkinter canvas widget object
        self.filled = set() # filled canvas rectangle object reference
        self.tiles = set(range(9)) # free tiles indices on board board
        self.maxAgent = set() # maximizing player's filled tiles index
        self.minAgent = set() # minimizing player's filled tiles index
        self.isMaxAgent = True # True if player's turn. False, if computer's.

    def restart(self):
        # This method is invoked when the user clicks on the RESTART button.
        for filled_tile in self.canvas.find_all():
            self.canvas.itemconfigure(filled_tile, fill='')

        # reinitialize game instance variables
        self.result.set('')
        self.filled = set()
        self.tiles = set(range(9))
        self.maxAgent = set()
        self.minAgent = set()
        self.isMaxAgent = True

    def play(self, event):
        # This method is invoked when the user clicks on a square.
        # Player Move
        score = Game.__evaluate_win(self.maxAgent, self.minAgent)
        if score == 0 and self.tiles and self.isMaxAgent:
            tile = (event.y // 200) * 3 + (event.x // 200)
            self.__update_board_canvas(tile)
            self.__update_game_state(tile)
            self.__update_result_label()

        # Computer Move
        score = Game.__evaluate_win(self.maxAgent, self.minAgent)
        if score == 0 and self.tiles and not self.isMaxAgent:
            tile = Game\
                .get_computer_move(self.maxAgent, self.minAgent, self.tiles)
            self.__update_board_canvas(tile)
            self.__update_game_state(tile)
            self.__update_result_label()

    # ------------------------------------------------------------------------
    #  Instance Helper Functions: Updating and Checking Game States
    # ------------------------------------------------------------------------
    def __update_game_state(self, tile):
        try:
            self.tiles.remove(tile)
            if self.isMaxAgent:
                self.maxAgent.add(tile)
            else:
                self.minAgent.add(tile)
            self.isMaxAgent = not self.isMaxAgent
        except KeyError as key_error:
            pass

    # ------------------------------------------------------------------------
    #  Instance Helper Functions: Setting and Getting Board
    # ------------------------------------------------------------------------
    def __update_board_canvas(self, tile):
        if tile not in self.maxAgent and tile not in self.minAgent:
                self.__paint_tile(tile)

    def __update_result_label(self):
        score = Game.__evaluate_win(self.maxAgent, self.minAgent)
        if score == 10:
            self.result.set('You Win!')
        elif score == -10:
            self.result.set('You Lost')
        elif score == 0 and len(self.tiles) == 0:
            self.result.set('Draw')

    def __paint_tile(self, tile):
            color = 'purple' if self.isMaxAgent else 'blue'
            canvas_rectangle = self.canvas.find_all()[tile]
            self.canvas.itemconfigure(canvas_rectangle, fill=color)

    # ------------------------------------------------------------------------
    #  Static Helper Functions: Computing NPC's Move, Minimax and Evaluator
    # ------------------------------------------------------------------------
    @staticmethod
    def get_computer_move(player, computer, tiles):
        best_move = -1
        min_score = math.inf

        for move in tiles:
            new_computer = computer | {move}
            new_tiles = tiles - {move}
            score = Game.__minimax(player, new_computer, new_tiles, True)
            if score < min_score:
                min_score = score
                best_move = move

        return best_move

    @staticmethod
    def __minimax(max_agent, min_agent, tiles, is_max_agent):
        score = Game.__evaluate_win(max_agent, min_agent)
        if not tiles or score !=0:
            val = Game.__evaluate_win(max_agent, min_agent)
            return val

        if is_max_agent:
            max_val = -math.inf
            for move in tiles:
                new_agent = max_agent | {move}
                new_tiles = tiles - {move}
                val = Game.__minimax(new_agent, min_agent, new_tiles, False)
                max_val = max(max_val, val)
            return max_val
        else:  # min player
            min_val = math.inf
            for move in tiles:
                new_agent = min_agent | {move}
                new_tiles = tiles - {move}
                val = Game.__minimax(max_agent, new_agent, new_tiles, True)
                min_val = min(min_val, val)
            return min_val

    @staticmethod
    def __evaluate(max_player, min_player, available, is_max_player):
        bonus = len(available)
        score = Game.__evaluate_win(max_player, min_player)
        if score != 0:
            score = (score * bonus) + len(max_player) - len(min_player)

        return score


    # ------------------------------------------------------------------------
    #  Static Helper Functions: Evaluating Win or Draw
    # ------------------------------------------------------------------------
    @staticmethod
    def __evaluate_win(max_player, min_player):
        for win in Game.WINNING_STATES:
            if set(win).issubset(max_player):
                return 10
            elif set(win).issubset(min_player):
                return -10
        return 0


def main():
    computer = {0,7,5}
    player = {1,2,3,4}
    available = {6,8}
    print(Game.get_computer_move(player, computer, available))

    # Instantiate a root window
    root = tkinter.Tk()
    # Instantiate a Game object
    game = Game(root)
    # Enter the main event loop
    root.mainloop()


if __name__ == '__main__':
    main()