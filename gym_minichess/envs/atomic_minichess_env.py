from gym import spaces
from minichess.games.abstract.action import AbstractActionFlags
from minichess.games.abstract.board import AbstractBoardStatus
from minichess.games.abstract.piece import PieceColor
from minichess.games.gardner.action import LEN_ACTION_SPACE
import numpy as np
from gym_minichess.envs.gardner_minichess_env import GardnerMiniChessEnv
from minichess.games.atomic.board import AtomicChessBoard
from minichess.games.atomic.action import AtomicChessAction

CHECKMATE_REWARD = 25_000
CHECK_REWARD = 500

class RifleMiniChessEnv(GardnerMiniChessEnv):
    def __init__(self, adversary=None) -> None:
        super().__init__(adversary)
        self.board = AtomicChessBoard()
        self.action_space = spaces.Discrete(LEN_ACTION_SPACE)
        self.observation_space = spaces.Box(0, 1, shape=(self.board.height, self.board.width, 12))

        if adversary == None:
            self.adversary = None

    def step(self, action):

        # we must convert the action (an integer) to an appropriate chess action
        action_idx = action
        action_vector = np.zeros(self.action_space.n)
        action_vector[action_idx] = 1
        action = AtomicChessAction.decode(action_vector, self.board)

        self.board.push(action)

        # provide result of move before opponent moves
        observation = self.board.state_vector()

        reward = 0

        # reward checking moves
        if AbstractActionFlags.CHECK in self.board.peek().modifier_flags:
            if self.board.active_color == PieceColor.WHITE: # black just moved
                reward -= CHECK_REWARD
            else:
                reward += CHECK_REWARD

        # give reward after opponent move
        reward += self.board.reward()

        done = self.board.status != AbstractBoardStatus.ONGOING
        if done: # reward / penalize greatly for checkmates
            if self.board.status == AbstractBoardStatus.WHITE_WIN:
                reward += CHECKMATE_REWARD
            elif self.board.status == AbstractBoardStatus.BLACK_WIN:
                reward -= CHECKMATE_REWARD
        
        info = {} # TODO maybe

        return observation, reward, done, info

    def reset(self):
        self.board = AtomicChessBoard()

        return self.board.state_vector()