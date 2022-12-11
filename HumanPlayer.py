class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def choose_action(self, positions):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row - 1, col - 1)
            if action in positions:
                return action

    # append a hash state
    def add_state(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feed_reward(self, reward, symbol):
        pass

    def reset(self):
        pass