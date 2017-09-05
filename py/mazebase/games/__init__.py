from .mazegame import (
    MazeGame,
    BaseMazeGame,
    WithWaterAndBlocksMixin,
    RewardOnEndMixin,
    AbsoluteLocationVocabulary,
    BaseVocabulary,
    WithWaterBlocksTrapsMixin,
    WithWaterBlocksChestsMixin,
)
from .goal_based_games import (
    SingleGoal,
    MultiGoals,
    ConditionedGoals,
    Exclusion,
    Goto,
    GotoHidden,
)
from .blocks_switches_games import (
    PushBlock,
    PushBlockCardinal,
    Switches,
    LightKey,
    BlockedDoor,
    TrapKey,
    ChestKey,
)
