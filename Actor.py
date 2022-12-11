import numpy as np
import json
import os

class Actor:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.exp_rate = exp_rate
        self.states_value_first = {}
        self.states_value_second = {}
        self.states_buffer = {}
        self.rewards = np.array([])

    def add_state(self, hash, symbol):
        if hash not in self.states_value_first.keys() and symbol == 1:
            self.states_value_first[hash] = 0
        elif hash not in self.states_value_second.keys() and symbol == -1:
            self.states_value_second[hash] = 0

    def add_state_buffer(self, hash):
        if hash not in self.states_buffer.keys():
            self.states_buffer[hash] = 0

    def choose_action(self, positions, current_board, symbol):
        action = None
        next_hash = None
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
            next_board = current_board.copy()
            next_board[positions[idx]] = symbol
            next_hash = str(next_board.reshape(9))
            self.add_state(next_hash, symbol)
        else:
            value_max = -1
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_board_hash = str(next_board.reshape(9))
                self.add_state(next_board_hash, symbol)
                if symbol == 1:
                    value = float(self.states_value_first.get(next_board_hash))
                else:
                    value = float(self.states_value_second.get(next_board_hash))
                if value >= value_max:
                    value_max = value
                    next_hash = next_board_hash
                    action = p
        self.add_state_buffer(next_hash)
        return action

    def feed_reward(self, reward, symbol):
        for st in self.states_buffer.keys():
            if symbol == 1:
                self.states_value_first[st] += self.exp_rate * (reward - self.states_value_first[st])
            else:
                self.states_value_second[st] += self.exp_rate * (reward - self.states_value_second[st])
        self.rewards = np.append(self.rewards, reward)


    def save_policy(self):
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/policy_first_{self.name}.json", "w") as write_file:
            json.dump(self.states_value_first, write_file)
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/policy_second_{self.name}.json", "w") as write_file:
            json.dump(self.states_value_second, write_file)

    def load_policy(self, first, sec):
        with open(first, "r") as read_file:
            self.states_value_first = json.load(read_file)
        with open(sec, "r") as read_file:
            self.states_value_second = json.load(read_file)

    def reset(self):
        self.states_buffer = {}