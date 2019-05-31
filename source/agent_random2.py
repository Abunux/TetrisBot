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
#    Classe AgentRandom2
#
#    Agent qui joue de manière aléatoire
#    avec les blocs rapides
#
#-----------------------------------------------------

from tetris_engine import *
from agent import *
from random import *
import os


class AgentRandom2(Agent):
    """ Agent aléatoire jouant directement les pièces """

    def __init__(self, temporisation=0.1, silent=False):
        super().__init__(name="Random 2")
        self.engine = TetrisEngine(
            self.getMove, temporisation=temporisation, silent=silent, agent_name=self.name, agent_description=self.decription)

    def getMove(self):
        """ Renvoie un mouvement direct aléatoire """
        (j, r) = choice(self.engine.getPossibleMovesDirect())
        return "P:%d:%d" % (j, r)


if __name__ == "__main__":
    player = AgentRandom2()
    playGame(player, temporisation=0.1)
