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


class Env(object):
    """
    wrapper for giving gym like functions
    """

    def __init__(self, game_type = "chests", 
                        grid_size = 10, 
                        max_eps_len = 500):

        if game_type not in ["chests","traps"]:
           raise Exception
        else:
            if game_type == "chests":
                self.gameClass = games.ChestKey
            elif game_type == "traps"
                self.gameClass = games.TrapKey
        
        

        game0 = curriculum.CurriculumWrappedGame(
            self.gameClass,
            curriculums={
                'map_size': games.curriculum.MapSizeCurriculum(
                    (grid_size,) * 4,
                    (grid_size,) * 4,
                    (grid_size,) * 4
                ),
            }
        )

        all_games = [game0]
        
        self.game = games.MazeGame(
            all_games,
            # featurizer=featurizers.SentenceFeaturesRelative(
            #   max_sentences=30, bounds=4)
            featurizer=featurizers.GridFeaturizer()
        )

        
        self.w, self.h = game.get_max_bounds()
        
        self.actions = self.game.all_possible_actions()
        self.action_dim = 1 
        self.num_action = len(self.actions)

        self.state_dim = ( self.w, self.h , len(self.game.all_possible_features()))

        # for ep len
        self.frame = 0

        self.max_frame = max_eps_len
        #
        #game.display()


    def reset(self):
        """
        reset the game and gives the first observation
        """
        self.game.reset()

        config = self.game.observe()
        
        obs, info = config['observation']
        featurizers.grid_one_hot(self.game, obs)
        obs = np.array(obs)
        
        return obs



    def act(self, action_idx):
        """
        takes an action and executes it 

        returns (next_state_observation, reward, done, extra_info)
        """

        # convert the action index into the actual action
        action_idx = int(action_idx)
        
        action = self.actions[action_idx]

        self.game.act(action)

        self.frame += 1
    
        r =  self.game.reward()

        config = self.game.observe()
        obs, info = config['observation']
        featurizers.grid_one_hot(self.game, obs)
        obs = np.array(obs)

       
        done = self.game.is_over() or self.frame >= self.max_frame

        total_reward = self.game.reward_so_far()

        return (obs, r, done, total_reward)

    def render(self):

        return self.game.display()