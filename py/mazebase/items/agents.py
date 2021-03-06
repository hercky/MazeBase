from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from random import choice
import sys

from mazebase.utils import mazeutils
import mazebase.items as mi


class Agent(mi.MazeItem):
    '''
    Agents are special items that can perform actions. We use a mix-ins model
    to specify Agent traits. To combine traits, simply subclass both
    Agent classes:

    # This agent can move and drop bread crumbs
    class SingleGoalAgent(mi.SingleTileMovable, mi.BreadcrumbDropping):
        pass

    To make a new agent trait, create the class, subclass from Agent, create
    the actions, and call self._add_action('id', self.__action)

    IMPORTANT: Any attributes defined outside of this module will not be
    featurized. Agents are featurized as a list of what they can 'do'
    '''
    __properties = dict(
        # Speed allows some agents to move faster than others
        speed=1
    )

    def __init__(self, **kwargs):
        mazeutils.populate_kwargs(self, self.__class__.__properties, kwargs)
        super(Agent, self).__init__(**kwargs)

        self.actions = {'pass': self._pass}
        self.PRIO = 100
        self._all_agents = [x[1] for x in
                            mazeutils.all_classes_of(sys.modules[__name__])]

    def _pass(self):
        pass

    def _add_action(self, id, func):
        assert id not in self.actions, "Duplicate action id"
        self.actions[id] = func

    def featurize(self):
        features = list(set(self.__get_all_superclasses(self.__class__)))
        return features

    def __get_all_superclasses(self, cls):
        all_superclasses = []
        for superclass in cls.__bases__:
            if superclass in self._all_agents:
                all_superclasses.append(superclass.__name__)
            all_superclasses.extend(self.__get_all_superclasses(superclass))
        return all_superclasses

    def _get_display_symbol(self):
        return (u' A ', None, None, None)


class NPC(Agent):
    ''' NPC Agents cannot be controlled by the player and moves randomly '''
    def get_npc_action(self):
        return (self.id, choice(self.actions))


class SingleTileTriggerMovable(Agent):
    ''' Can move up, down, left, and right 1 tile per turn '''
    def __init__(self, **kwargs):
        super(SingleTileTriggerMovable, self).__init__(**kwargs)

        self._add_action("up", self.__up)
        self._add_action("down", self.__down)
        self._add_action("left", self.__left)
        self._add_action("right", self.__right)

    def __dmove(self, dx, dy):
        x, y = self.location
        nloc = x + dx, y + dy
        # Cannot walk into blocks, agents, or closed doors
        if (self.game._tile_get_block(nloc, mi.Block) is None and
                self.game._tile_get_block(nloc, Agent) is None ):
            self.game._move_item(self.id, location=nloc)

            # if you can move to the new block then trigger chest or trap here
            # if self.game._tile_get_block(nloc, mi.Chest) is not None:
            #     chest = self.game._tile_get_block(nloc, mi.Chest)
            #     chest.pick()
            #     # can delete the item here also
            #     # self.game._remove_item(chest_id)

            # elif self.game._tile_get_block(nloc, mi.Trap) is not None:
            #     trap = self.game._tile_get_block(nloc, mi.Trap)
            #     trap.pick()

                # delete the trap after one use
                #self.game._remove_item(trap.id)

    def __up(self):
        self.__dmove(0, 1)

    def __down(self):
        self.__dmove(0, -1)

    def __left(self):
        self.__dmove(-1, 0)

    def __right(self):
        self.__dmove(1, 0)