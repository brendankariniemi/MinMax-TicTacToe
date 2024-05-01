import tkinter as tk
import random


class TicTacToe:
    def __init__(self):
        self.buttons = None
        self.board = None
        self.game_active = False
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.result = tk.Label(self.window)
        self.result.grid(row=4, column=0, columnspan=3)
        self.button = tk.Button(self.window, text="Start Game", command=self.start_game)
        self.button.grid(row=5, column=0, columnspan=3)
        self.initialize_board()

    def start_game(self):
        self.game_active = True
        self.button.config(text="Restart Game", command=self.restart_game)
        self.initialize_board()
        if random.choice([True, False]):
            self.ai_move()

    def restart_game(self):
        self.game_active = True
        self.initialize_board()
        if random.choice([True, False]):
            self.ai_move()

    def initialize_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.create_buttons()
        self.result.config(text="")

    def create_buttons(self):
        self.buttons = [
            [tk.Button(self.window, text='', command=lambda row=row, col=col: self.click(row, col), height=3, width=6)
             for col in range(3)] for row in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].grid(row=row, column=col)

    def click(self, row, col):
        if self.game_active and self.board[row][col] == '' and not self.game_over_check(self.board):
            self.board[row][col] = 'X'
            self.buttons[row][col]['text'] = 'X'
            result = self.game_over_check(self.board)
            if not result:
                self.ai_move()
            else:
                self.show_result(f"{result} wins!" if result != 'Draw' else "It's a draw!")
                self.game_active = False

    def ai_move(self):
        if self.game_active and not self.game_over_check(self.board):
            move, score = self.minimax(self.board, 'O')
            if move is not None:
                row, col = move
                self.board[row][col] = 'O'
                self.buttons[row][col]['text'] = 'O'
            result = self.game_over_check(self.board)
            if result:
                self.show_result(f"{result} wins!" if result != 'Draw' else "It's a draw!")
                self.game_active = False

    def minimax(self, board, player):
        result = self.game_over_check(board)
        if result:
            if result == 'O':
                return None, 1
            elif result == 'X':
                return None, -1
            elif result == 'Draw':
                return None, 0

        moves = []
        opponent = 'X' if player == 'O' else 'O'
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = player
                    _, potential_score = self.minimax(board, opponent)
                    moves.append(((row, col), potential_score))
                    board[row][col] = ''

        if player == 'O':
            best_move = max(moves, key=lambda x: x[1])
        else:
            best_move = min(moves, key=lambda x: x[1])
        return best_move

    def game_over_check(self, board):
        lines = [
            board[0], board[1], board[2],
            [board[r][0] for r in range(3)], [board[r][1] for r in range(3)],
            [board[r][2] for r in range(3)],
            [board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]
        ]

        for line in lines:
            if line[0] == line[1] == line[2] != '':
                return line[0]

        if all(cell != '' for row in board for cell in row):
            return 'Draw'

        return None

    def show_result(self, result):
        self.result.config(text=result)
        self.game_active = False


if __name__ == "__main__":
    game = TicTacToe()
    game.window.mainloop()
