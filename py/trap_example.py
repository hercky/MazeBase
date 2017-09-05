from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from random import choice, randint
from time import sleep
from os import system
from pprint import PrettyPrinter
from six.moves import input
import numpy as np

import mazebase.games as games
from mazebase.games import featurizers
from mazebase.games import curriculum

import logging
logging.getLogger().setLevel(logging.DEBUG)

player_mode = True

tk = curriculum.CurriculumWrappedGame(
    games.TrapKey,
    curriculums={
        'map_size': games.curriculum.MapSizeCurriculum(
            (10, 10, 10, 10),
            (10, 10, 10, 10),
            (20, 20, 20, 20)
        ),
    }
)



ck = curriculum.CurriculumWrappedGame(
    games.ChestKey,
    curriculums={
        'map_size': games.curriculum.MapSizeCurriculum(
            (10, 10, 10, 10),
            (10, 10, 10, 10),
            (20, 20, 20, 20)
        ),
    }
)


#all_games = [bd, lk]
all_games = [tk]
game = games.MazeGame(
    all_games,
    # featurizer=featurizers.SentenceFeaturesRelative(
    #   max_sentences=30, bounds=4)
    featurizer=featurizers.GridFeaturizer()
)
max_w, max_h = game.get_max_bounds()

pp = PrettyPrinter(indent=2, width=160)
# all_actions = game.all_possible_actions()
# all_features = game.all_possible_features()
# print("Actions:", all_actions)
# print("Features:", all_features)
# sleep(2)


def action_func(actions):
    if not player_mode:
        return choice(actions)
    else:
        print(list(enumerate(actions)))
        ind = -1
        while ind not in range(len(actions)):
            ind = input("Input number for action to take: ")
            try:
                ind = int(ind)
            except ValueError:
                ind = -1
        return actions[ind]


frame = 0
game.display()
sleep(.1)
system('clear')
while True:
    print("r: {}\ttr: {} \tguess: {}".format(
        game.reward(), game.reward_so_far(), game.approx_best_reward()))
    config = game.observe()
    pp.pprint(config['observation'][1])
    # Uncomment this to featurize into one-hot vectors
    obs, info = config['observation']
    featurizers.grid_one_hot(game, obs)
    obs = np.array(obs)
    featurizers.vocabify(game, info)
    info = np.array(obs)
    config['observation'] = obs, info
    game.display()

    id = game.current_agent()
    actions = game.all_possible_actions()
    action = action_func(actions)
    game.act(action)

    sleep(.1)
    system('clear')
    print("\n")
    frame += 1
    if game.is_over() or frame > 300:
        frame = 0
        print("Final reward is: {}, guess was {}".format(
            game.reward_so_far(), game.approx_best_reward()))
        game.make_harder()
        game.reset()
        break
