import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.current_player = "X"  # Игрок начинает первым
        self.human_player = "X"  # Игрок играет за "X" или "O"
        self.board = [""] * 9
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def on_button_click(self, index):
        if self.board[index] == "" and self.current_player == self.human_player:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Победа!", f"Игрок {self.current_player} выиграл!")
                self.reset_board(switch_player=True)
            elif "" not in self.board:
                messagebox.showinfo("Ничья!", "Ничья!")
                self.reset_board(switch_player=True)
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.computer_move()

    def computer_move(self):
        if self.current_player != self.human_player:
            best_move = self.minimax(self.board, self.current_player)['index']
            self.board[best_move] = self.current_player
            self.buttons[best_move].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Победа!", f"Компьютер ({self.current_player}) выиграл!")
                self.reset_board(switch_player=True)
            elif "" not in self.board:
                messagebox.showinfo("Ничья!", "Ничья!")
                self.reset_board(switch_player=True)
            else:
                self.current_player = "X" if self.current_player == "O" else "O"

    def minimax(self, board, player):
        available_moves = [i for i, val in enumerate(board) if val == ""]

        # Проверяем, есть ли победитель или ничья
        if self.check_winner_board(board, self.human_player):
            return {'score': -10}
        elif self.check_winner_board(board, self.current_player):
            return {'score': 10}
        elif len(available_moves) == 0:
            return {'score': 0}

        # Собираем все возможные ходы
        moves = []
        for move in available_moves:
            new_board = board.copy()
            new_board[move] = player
            result = self.minimax(new_board, "O" if player == "X" else "X")
            moves.append({'index': move, 'score': result['score']})

        # Выбираем лучший ход
        if player == self.current_player:
            best_move = max(moves, key=lambda x: x['score'])
        else:
            best_move = min(moves, key=lambda x: x['score'])

        return best_move

    def check_winner(self):
        return self.check_winner_board(self.board, self.current_player)

    def check_winner_board(self, board, player):
        win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]
        for combo in win_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
                return True
        return False

    def reset_board(self, switch_player=False):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="")
        if switch_player:
            self.human_player = "O" if self.human_player == "X" else "X"
        self.current_player = self.human_player
        # Если бот становится "X", он должен сделать первый ход
        if self.current_player != "X":
            self.computer_move()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()