import numpy as np

class State:
    def __init__(self, rows, cols, p1=None, p2=None):
        self.board = np.zeros((rows, cols))
        self.p1 = p1
        self.p2 = p2
        self.is_end = False
        self.board_hash = None
        self.player_symbol = 1
        self.start = 1

    def set_hash(self):
        self.board_hash = str(self.board.reshape(9))

    def available_positions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def update_state(self, position):
        self.board[position] = self.player_symbol
        self.player_symbol = -1 if self.player_symbol == 1 else 1

    def winner(self):
        for i in range(3):
            if sum(self.board[i, :]) == 3:
                self.is_end = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.is_end = True
                return -1

        for i in range(3):
            if sum(self.board[:, i]) == 3:
                self.is_end = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.is_end = True
                return -1

        d1 = sum([self.board[i, i] for i in range(3)])
        d2 = sum([self.board[i - 1, -i] for i in range(1, 4)])
        if d1 == 3 or d2 == 3:
            self.is_end = True
            return 1
        if d1 == -3 or d2 == -3:
            self.is_end = True
            return -1


        if len(self.available_positions()) == 0:
            self.is_end = True
            return 0
        self.is_end = False
        return None


    def give_reward(self):
        result = self.winner()
        if result == 1:
            if self.start == 1:
                self.p1.feed_reward(1, 1)
                self.p2.feed_reward(-1, -1)
            else:
                self.p1.feed_reward(1, -1)
                self.p2.feed_reward(-1, 1)
        elif result == -1:
            if self.start == 1:
                self.p1.feed_reward(-1, 1)
                self.p2.feed_reward(1, -1)
            else:
                self.p1.feed_reward(-1, -1)
                self.p2.feed_reward(1, 1)
        else:
            if self.start == 1:
                self.p1.feed_reward(0.2, 1)
                self.p2.feed_reward(0.5, -1)
            else:
                self.p1.feed_reward(0.5, -1)
                self.p2.feed_reward(0.2, 1)

    def play_with_human(self):
        while not self.is_end:
            if self.start == 1:
                # Player 1
                self.machine_step(self.p1)
                self.show_board()
                win = self.winner()
                if win is not None:
                    if win != 0:
                        print("machine wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

                # Player 2
                self.human_step()
                self.show_board()
                win = self.winner()
                if win is not None:
                    self.reset()
                    break
            else:
                # Player 2
                self.human_step()
                self.show_board()
                win = self.winner()
                if win is not None:
                    self.reset()
                    break
                # Player 1
                self.machine_step(self.p1)
                self.show_board()
                win = self.winner()
                if win is not None:
                    if win != 0:
                        print("machine wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

        ask = input('Continue?(Y/N)')
        if ask == 'Y' or ask == 'y':
            self.play_with_human()
        else:
            return
    def machine_step(self, agent):
        positions = self.available_positions()
        action = agent.choose_action(positions, self.board, self.player_symbol)
        self.set_hash()
        agent.add_state(self.board_hash, self.player_symbol)
        self.update_state(action)
        win = self.winner()
        if win is not None:
            self.give_reward()

    def human_step(self):
        positions = self.available_positions()
        p2_action = self.p2.choose_action(positions)
        self.update_state(p2_action)
        win = self.winner()
        if win is not None:
            self.give_reward()

    def training(self, rounds=100):
        for i in range(rounds):
            while not self.is_end:
                if self.start == 1:
                    # Player 1
                    self.machine_step(self.p1)
                    win = self.winner()
                    if win is not None:
                        self.reset()
                        break
                    # Player 2
                    self.machine_step(self.p2)
                    win = self.winner()
                    if win is not None:
                        self.reset()
                        break
                else:
                    # Player 2
                    self.machine_step(self.p2)
                    win = self.winner()
                    if win is not None:
                        self.reset()
                        break
                    # Player 1
                    self.machine_step(self.p1)
                    win = self.winner()
                    if win is not None:
                        self.reset()
                        break


    def reset(self):
        self.board = np.zeros((3, 3))
        self.is_end = False
        self.board_hash = None
        self.start = -1 if self.start == 1 else 1
        self.player_symbol = 1
        self.p1.reset()
        self.p2.reset()

    def show_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1.0:
                    print('X', end=' ')
                elif self.board[i][j] == 0.0:
                    print('_', end=' ')
                elif self.board[i][j] == -1.0:
                    print('O', end=' ')
            print('\n')
        print()
