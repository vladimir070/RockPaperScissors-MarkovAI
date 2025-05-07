import tkinter as tk
import random
import os

moves = ["камень", "ножницы", "бумага"]

class MarkovChain:
    def __init__(self):
        self.chain = {}

    def train(self, state, action, reward):
        if state not in self.chain:
            self.chain[state] = {}
        if action not in self.chain[state]:
            self.chain[state][action] = 0
        self.chain[state][action] += reward

    def predict(self, state):
        if state not in self.chain:
            return None

        best_action = None
        best_value = float('-inf')
        for action, value in self.chain[state].items():
            if value > best_value:
                best_action = action
                best_value = value
        return best_action

class MarkovAI:
    def __init__(self, exploration_rate=0.1):
        self.chains = {
            "камень": MarkovChain(),
            "ножницы": MarkovChain(),
            "бумага": MarkovChain()
        }
        self.exploration_rate = exploration_rate

    def ai_move_choice(self, last_move):
        """Выбор хода AI с учетом exploration."""
        if last_move is None:
            return random.choice(moves)

        # Exploration vs Exploitation
        if random.random() < self.exploration_rate:  # вероятность случайного хода
            return random.choice(moves)

        predicted_move = self.chains[last_move].predict(last_move)
        if predicted_move is None:
            return random.choice(moves)
        else:
            return predicted_move

    def train(self, last_move, ai_move, reward):
        """Обучаем цепь Маркова."""
        if last_move is not None:
            for move in moves:
                if move == ai_move:
                    self.chains[last_move].train(last_move, move, reward)
                else:
                    self.chains[last_move].train(last_move, move, -reward / 2)

def determine_winner(move1, move2):
    """Определяем победителя."""
    if move1 == move2:
        return "Ничья!"
    elif (move1 == "камень" and move2 == "ножницы") or \
         (move1 == "ножницы" and move2 == "бумага") or \
         (move1 == "бумага" and move2 == "камень"):
        return "Игрок"
    else:
        return "AI"

def ai_vs_ai(markov_ai, last_move):
    """Один раунд игры AI vs AI."""
    ai_move1 = markov_ai.ai_move_choice(last_move)
    ai_move2 = random.choice(moves)  # Простой случайный ход для второго AI

    winner = determine_winner(ai_move2, ai_move1)

    if winner == "AI": #Наказываем если проиграл, награждаем если выйграл
        markov_ai.train(last_move, ai_move1, 1) #Награждаем
    elif winner == "Игрок":
        markov_ai.train(last_move, ai_move1, -1) #Наказываем
    else:
        markov_ai.train(last_move, ai_move1, 0) #Ничья ничего не делаем

    return ai_move1

def pre_train_ai(markov_ai, num_games=20000):
    """Предварительное обучение Markov AI."""
    last_move = None
    for _ in range(num_games):
        last_move = ai_vs_ai(markov_ai, last_move) #Тренируем

class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Камень, Ножницы, Бумага")

        self.markov_ai = MarkovAI()
        pre_train_ai(self.markov_ai, num_games=20000)  # Предварительное обучение
        self.last_move = None
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0

        # Стиль
        font = ("Arial", 14)
        bg_color = "#f0f0f0"  # Светло-серый
        button_color = "#4CAF50"  # Зеленый
        label_color = "#333333"  # Темно-серый

        master.configure(bg=bg_color)

        # Элементы интерфейса
        self.label = tk.Label(master, text="Сделайте свой выбор:", font=font, bg=bg_color, fg=label_color)
        self.label.pack(pady=10)

        self.rock_button = tk.Button(master, text="Камень", font=font, bg=button_color, fg="white", command=lambda: self.play_round("камень"))
        self.rock_button.pack(pady=5)

        self.scissors_button = tk.Button(master, text="Ножницы", font=font, bg=button_color, fg="white", command=lambda: self.play_round("ножницы"))
        self.scissors_button.pack(pady=5)

        self.paper_button = tk.Button(master, text="Бумага", font=font, bg=button_color, fg="white", command=lambda: self.play_round("бумага"))
        self.paper_button.pack(pady=5)

        self.result_label = tk.Label(master, text="", font=font, bg=bg_color, fg=label_color)
        self.result_label.pack(pady=10)

        self.stats_label = tk.Label(master, text="Статистика: Игрок - 0, AI - 0, Ничьи - 0", font=font, bg=bg_color, fg=label_color)
        self.stats_label.pack(pady=10)

    def play_round(self, player_move):
        """Играем один раунд."""
        # Ход AI
        ai_move = self.markov_ai.ai_move_choice(self.last_move)

        # Определяем победителя
        winner = determine_winner(player_move, ai_move)

        # Обучаем MarkovAI
        if winner == "Игрок":
            self.markov_ai.train(self.last_move, ai_move, -1)
        elif winner == "AI":
            self.markov_ai.train(self.last_move, ai_move, 1)
        else:
            self.markov_ai.train(self.last_move, ai_move, 0)

        # Обновляем статистику
        if winner == "Игрок":
            self.player_wins += 1
        elif winner == "AI":
            self.ai_wins += 1
        else:
            self.draws += 1

        # Обновляем last_move
        self.last_move = ai_move

        # Выводим результат
        result_text = f"Вы выбрали: {player_move}\nAI выбрал: {ai_move}\nРезультат: {winner}"
        self.result_label.config(text=result_text)

        # Обновляем статистику
        stats_text = f"Статистика: Игрок - {self.player_wins}, AI - {self.ai_wins}, Ничьи - {self.draws}"
        self.stats_label.config(text=stats_text)

root = tk.Tk()
game_gui = GameGUI(root)
root.mainloop()