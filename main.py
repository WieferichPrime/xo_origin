from State import State
from Actor import Actor
from HumanPlayer import HumanPlayer
import matplotlib.pyplot as plt
import numpy as np
import os

def training(AI):
    AI_2 = Actor('machine_2')
    AI_2.exp_rate = 0.05
    try:
        AI_2.load_policy(f'{os.path.dirname(os.path.abspath(__file__))}/policy_first_{AI_2.name}.json', f'{os.path.dirname(os.path.abspath(__file__))}/policy_second_{AI_2.name}.json')
    except BaseException as e:
        print(e)
    game = State(3, 3, AI, AI_2)
    game.training(1000)
    AI_2.save_policy()
    AI.save_policy()

def main():
    human = HumanPlayer('human')
    AI = Actor('machine')
    try:
        AI.load_policy(f'{os.path.dirname(os.path.abspath(__file__))}/policy_first_{AI.name}.json', f'{os.path.dirname(os.path.abspath(__file__))}/policy_second_{AI.name}.json')
    except BaseException as e:
        print(e)

    ask = input('Training?(Y/N)')
    if ask == 'Y' or ask == 'y':
        training(AI)
        rew_intervals = np.split(AI.rewards, 200)
        y = [sum(rew)/len(rew) for rew in rew_intervals]
        x = [i for i in range(len(rew_intervals))]
        plt.bar(x, y)
        plt.savefig('training.png')
        plt.show()
    AI.exp_rate = 0.05

    game = State(3, 3, AI, human)
    game.play_with_human()
    AI.save_policy()


if __name__ == "__main__":
    main()
