#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------
#
#        Tetris Bot
#
#    Projet maths infos du DU CCIE 2ème année
#    de l'université d'Aix-Marseille
#
#    Frédéric Muller - Lionel Ponton
#
#    Licence : CC By-NC-SA
#
#    Projet démarré le 25/11/2018
#
#-----------------------------------------------------
#
#    Classe TetrisEnv
#
#    Environnement à la OpenAi Gym
#    pour le reinforcement learning
#
#-----------------------------------------------------

from tetris_engine import *
from random import *
from time import *


class TetrisEnv(TetrisEngine):
    """ Environnement à la OpenAI Gym pour implémenter le reinforcement learning """

    def __init__(self, width=10, height=22, max_blocks=0, base_blocks_bag=CLASSIC_BLOCK_BAG,
                 random_generator_seed=None, agent_name="", agent_description=""):
        super().__init__(width=width, height=height, max_blocks=max_blocks,
                         base_blocks_bag=base_blocks_bag,
                         temporisation=0, silent=True, random_generator_seed=random_generator_seed,
                         agent_name=agent_name, agent_description=agent_description)
        self.action_space = ['L', 'R', 'D', 'H', 'T', 'N']
        self.nb_actions = len(self.action_space)
        self.done = False
        self.time_start = time()

    def reset(self):
        """ Réinitialise l'environnement """
        self.__init__(width=self.width, height=self.height, max_blocks=self.max_blocks,
                      base_blocks_bag=self.base_blocks_bag,
                      random_generator_seed=self.random_generator_seed,
                      agent_name=self.agent_name, agent_description=self.agent_description)
        self.getNewBlock()
        self.moveBlockInDirection('')
        self.getState()

    def getState(self):
        """ Renvoie l'état de la grille """
        self.state = self.board.npBinaryRepresentation()
        return self.state

    def getStateCode(self):
        """ Renoie de code entier de l'état de la grille """
        self.stateCode = self.board.encodeToInt()
        return self.stateCode

    def sampleAction(self):
        """ Renvoie une action aléatoire """
        return choice(self.action_space)

    def step(self, action):
        """ Effectue une action (joue un coup)
            Met à jour les informations (done, state) """
        self.time_total = time() - self.time_start
        start_time = time()
        self.playCommand(action)
        self.updateTimes(start_time)
        nb_lines = self.board.processLines()
        self.total_lines += nb_lines
        self.lines_combo[nb_lines] += 1
        self.score += self.getScoreFromLines(nb_lines)

        # Reward = (nombre de lignes faites)^2
        self.reward = nb_lines**2

        if not self.moveBlockInDirection(''):
            self.fixed_board = self.board.copy()
            self.fixed_board.updateStats()
            self.getNewBlock()
        self.done = self.isEndGame() or (self.max_blocks != 0 and
                                         self.nb_blocks_played == self.max_blocks)

        self.state = self.getState()

    def render(self):
        """ Affiche le jeu """
        os.system("clear")
        print(self)


if __name__ == "__main__":
    input("Press enter to start")
    env = TetrisEnv(width=5, height=6, base_blocks_bag=DOMINO_BLOCK_BAG)
    env.reset()
    for i in range(10000):
        sleep(0.01)
        env.render()
        env.step(env.sampleAction())
        if env.done:
            env.reset()
    env.render()
    input()
