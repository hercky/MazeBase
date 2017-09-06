from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from mazebase.items import MazeItem


class HasStatesMixin(object):
    _MAX_STATES = 10
    STATE_FEATURE = ["state{0}".format(i) for i in range(_MAX_STATES)]

    @classmethod
    def all_features(cls):
        return super(HasStatesMixin, cls).all_features() + cls.STATE_FEATURE


class Block(MazeItem):
    """
    an impassible obstacle that does not allow the agent to move to that grid location
    """
    def __init__(self, **kwargs):
        super(Block, self).__init__(passable=False, **kwargs)

    def _get_display_symbol(self):
        return (None, None, 'on_white', None)


class Water(MazeItem):
    """
    the agent may move to a grid location with water, but incurs an additional cost of for doing so.
    """
    def __init__(self, **kwargs):
        super(Water, self).__init__(**kwargs)
        self.PRIO = -100

    def _get_display_symbol(self):
        return (None, None, 'on_blue', None)


class Corner(MazeItem):
    """
    This item simply marks a corner of the board.
    """
    def __init__(self, **kwargs):
        super(Corner, self).__init__(**kwargs)

    def _get_display_symbol(self):
        return (u'   ', None, None, None)


class Goal(MazeItem):
    """
     depending on the task, one or more goals may exist, each named individually.
    """
    __MAX_GOAL_IDS = 1

    def __init__(self, id=0, **kwargs):
        super(Goal, self).__init__(**kwargs)
        self.goal_id = id
        assert self.goal_id < self.__MAX_GOAL_IDS,\
            "cannot create goal with id >{0}".format(
                self.__MAX_GOAL_IDS)

    def _get_display_symbol(self):
        return (u'*{0}*'.format(self.goal_id), 'red', None, None)

    def featurize(self):
        return super(Goal, self).featurize() +\
            ["goal_id" + str(self.goal_id)]

    @classmethod
    def all_features(cls):
        return super(Goal, cls).all_features() +\
            ["goal_id" + str(k) for k in range(cls.__MAX_GOAL_IDS)]


class Chest(MazeItem):
    """
    have an action pick pick / toggle which agent can use to pick stuff 
    """
    def __init__(self, **kwargs):
        super(Chest, self).__init__(**kwargs)
        
    def _get_display_symbol(self):
        return (u'$ $', 'grey', 'on_yellow', None)


class Trap(MazeItem):
    """
    oppposite of chest
    have an action pick pick / toggle which agent can use to pick stuff 
    """
    def __init__(self, **kwargs):
        super(Trap, self).__init__(**kwargs)
        
    def _get_display_symbol(self):
        return (u'x x', 'grey', 'on_magenta', None)