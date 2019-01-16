#!/usr/bin/env python3

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

from tetris_engine import *
from agent import *
from random import *
import os


class AgentRandom1(Agent):
    def __init__(self, temporisation=0.1, silent=False):
        super().__init__(name="Random 1")
        self.engine = TetrisEngine(
            self.getMove, temporisation=temporisation, silent=silent)

    def getMove(self):
        move = choice(['L', 'R', 'N', 'T', 'H'])
        return move


if __name__ == "__main__":
    playGameWithAgent(AgentRandom1)
