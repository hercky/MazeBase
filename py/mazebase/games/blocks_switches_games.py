from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from random import randint

from mazebase.games import (
    WithWaterAndBlocksMixin,
    WithWaterBlocksTrapsMixin,
    WithWaterBlocksChestsMixin,
    RewardOnEndMixin,
)
from mazebase.utils import creationutils
from mazebase.utils.mazeutils import populate_kwargs, MazeException, choice
from mazebase.items import agents
import mazebase.items as mi



class PBS2Type(RewardOnEndMixin, WithWaterBlocksTrapsMixin):
    pass


class TriggerAgent(agents.SingleTileTriggerMovable):
    pass


def _est(game, s, e):
    '''shorthand to estimate reward for an agent to move from s to e'''
    visited, path = creationutils.dijkstra(
        game, s, creationutils.agent_movefunc, True)
    return -visited[e]  # Returns distance, which is negation of reward


def pbwps(p, start, end):
    path = [end]
    while path[-1] != start:
        path.append(p[path[-1]])
    waypoints = []
    path.reverse()
    for i, j in zip(path[:-1], path[1:]):
        x, y = i
        nx, ny = j
        waypoints.append((2 * x - nx, 2 * y - ny))
    return waypoints



def add_4_walls(game, margin = 1 ):
    """
    creates a vertical and horizontal wall openings in each wall 
    for dividing the game into 4 walls
    """
    size = (game.width, game.height)
    
    x_line = randint(margin, (size[0] - 1) - margin )
    y_line = randint(margin, (size[1] - 1) - margin )

    #intersecting point will be
    # x_line, y _line 

    # get the four opening here
    wall_openings = [   (randint(0, x_line - 1), y_line), 
                        (randint(x_line + 1, size[0] - 1), y_line),
                        (x_line, randint(0, y_line - 1)),
                        (x_line, randint(y_line + 1, size[1] - 1)),
                    ]

    # fill the horizontal wall
    for i in range(size[0]):
        if (i, y_line) not in wall_openings:
            loc = [i, y_line]
            game._add_item(mi.Block(location=loc))
        
    # fill the vertical wall
    for i in range(size[1]):
        if (x_line, i) not in wall_openings:
            loc = [x_line, i]
            game._add_item(mi.Block(location=loc))
        

    # return the intersection point
    # dunno why ?
    loc = [x_line, y_line]
    
    return loc, wall_openings


class TrapKey(PBS2Type): 
    ''' Agent must open a door with a switch and go to the goal '''
    
    # def __init__(self, **kwargs):
    #     populate_kwargs(self, self.__class__.__properties, kwargs)
    #     super(TrapKey, self).__init__(**kwargs)

    def _reset(self):
        intersection, holes = add_4_walls(self)

        # No doors for now 
        # self.door = mi.Door(location=hole,
        #                     state=choice(range(1, self.switch_states)))
        # self._add_item(self.door)

        # ad blocks on the holes temporarily
        blocked_holes = []
        for i in range(len(holes)):
            blocked_holes.append(mi.Block(location= holes[i]))
            self._add_item(blocked_holes[i])

        # Add additional blocks and waters 
        # only blocks and water have reset methods, and that sprinkles blocs and waters around
        super(TrapKey, self)._reset()


        # empty the wall opening if they have been blocked
        for i in range(len(holes)):
            self._remove_item(blocked_holes[i].id)

        
        # Add the goal
        loc = choice(creationutils.empty_locations(
            self, bad_blocks=[mi.Block, mi.Trap, mi.Water])) # bad blocks where the goal can't be placed
        self.goal = mi.Goal(location=loc)
        self._add_item(self.goal)
        

        # # no switches for now
        # side = choice([-1, 1])
        # # for adding switch to the opposite side of the goal
        # def mask_func(x, y):
        #     return side * ((x, y)[1 - dim] - hole[1 - dim]) > 0

        # loc = choice(creationutils.empty_locations(
        #     self, bad_blocks=[mi.Block, mi.Door, mi.Goal], mask=mask_func))
        # self.sw = mi.Switch(location=loc, nstates=self.switch_states)
        # self._add_item(self.sw)

        # add agent 
        loc = choice(creationutils.empty_locations(
            self, bad_blocks=[mi.Block, mi.Trap]))
        self.agent = TriggerAgent(location=loc)
        self._add_agent(self.agent, "TrapKeyAgent")

        # check if goal can be visited or not 
        visited, _ = creationutils.dijkstra(self, loc,
                                            creationutils.agent_movefunc)
        
        if self.goal.location not in visited :
            raise MazeException("No path to goal")

    def _finished(self):
        # when the episode is finished
        return self.agent.location == self.goal.location


    def _calculate_approximate_reward(self):
        # doesnt take into account the traps or waters

        r = _est(self, self.agent.location, self.goal.location)
        
        return super(TrapKey, self)._calculate_approximate_reward() + r






class ChestKey(RewardOnEndMixin, WithWaterBlocksChestsMixin): 
    ''' Agent must open a door with a switch and go to the goal '''
    
    # def __init__(self, **kwargs):
    #     populate_kwargs(self, self.__class__.__properties, kwargs)
    #     super(ChestKey, self).__init__(**kwargs)

    def _reset(self):
        intersection, holes = add_4_walls(self)

        # No doors for now 
        # self.door = mi.Door(location=hole,
        #                     state=choice(range(1, self.switch_states)))
        # self._add_item(self.door)

        # ad blocks on the holes temporarily
        blocked_holes = []
        for i in range(len(holes)):
            blocked_holes.append(mi.Block(location=  holes[i]))
            self._add_item(blocked_holes[i])

        # Add additional blocks and waters 
        # only blocks and water have reset methods, and that sprinkles blocs and waters around
        super(ChestKey, self)._reset()


        # empty the wall opening if they have been blocked
        for i in range(len(holes)):
            self._remove_item(blocked_holes[i].id)

        
        # Add the goal
        loc = choice(creationutils.empty_locations(
            self, bad_blocks=[mi.Block, mi.Chest])) # bad blocks where the goal can't be placed
        self.goal = mi.Goal(location=loc)
        self._add_item(self.goal)
        

        # # no switches for now
        # side = choice([-1, 1])
        # # for adding switch to the opposite side of the goal
        # def mask_func(x, y):
        #     return side * ((x, y)[1 - dim] - hole[1 - dim]) > 0

        # loc = choice(creationutils.empty_locations(
        #     self, bad_blocks=[mi.Block, mi.Door, mi.Goal], mask=mask_func))
        # self.sw = mi.Switch(location=loc, nstates=self.switch_states)
        # self._add_item(self.sw)

        # add agent 
        loc = choice(creationutils.empty_locations(
            self, bad_blocks=[mi.Block, mi.Chest]))
        self.agent = TriggerAgent(location=loc)
        self._add_agent(self.agent, "TrapKeyAgent")

        # check if goal can be visited or not 
        visited, _ = creationutils.dijkstra(self, loc,
                                            creationutils.agent_movefunc)
        
        if self.goal.location not in visited :
            raise MazeException("No path to goal")

    def _finished(self):
        # when the episode is finished
        return self.agent.location == self.goal.location

    def _calculate_approximate_reward(self):
        # doesnt take into account the traps or waters

        r = _est(self, self.agent.location, self.goal.location)
        
        return super(ChestKey, self)._calculate_approximate_reward() + r