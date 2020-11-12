import gym
from gym import error, spaces, utils
from gym.utils import seeding

from minichess.games.gardner.board import GardnerChessBoard, LEN_ACTION_SPACE

from minichess.games.abstract.piece import PieceColor
from minichess.games.abstract.board import AbstractBoardStatus
from minichess.games.abstract.action import AbstractActionFlags
from minichess.players.gardner import RandomPlayer


import logging
logger = logging.getLogger(__name__)

CHECKMATE_REWARD = 25_000
CHECK_REWARD = 500

class GardnerMiniChessEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, adversary=None):
        self.board = GardnerChessBoard()
        self.action_space = spaces.Discrete(LEN_ACTION_SPACE)
        self.observation_space = spaces.Box(0, 1, shape=(self.board.height, self.board.width, 12))

    def step(self, action):

        self.board.push(action)

        # provide result of move before opponent moves
        observation = self.board.state_vector()

        reward = 0

        # reward checking moves
        if AbstractActionFlags.CHECK in self.board.peek().modifier_flags:
            reward += CHECK_REWARD

        # have opponent move
        proposed_action = self.adversary.propose_action(self.board, self.board.active_color, self.board.legal_action_mask())

        # apply a legal action to our board, if able
        if proposed_action != None:
            self.board.push(proposed_action)

            # penalize opponent checking moves
            if AbstractActionFlags.CHECK in self.board.peek().modifier_flags:
                reward -= CHECK_REWARD

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
        self.board = GardnerChessBoard()

        return self.board.state_vector()

    def render(self, mode='human'):
        if mode == 'rgb_array':
            raise NotImplementedError('RGB has not yet been implemented.')
        elif mode == 'human':
            print(self.board)
        else:
            super(GardnerMiniChessEnv, self).render(mode=mode) # just raise an exception

    def legal_actions(self):
        '''
            Returns a numpy array of the indices of legal moves.
        '''

        mask = self.board.legal_action_mask()

        return mask.nonzero()[0]

    def close(self):
        pass