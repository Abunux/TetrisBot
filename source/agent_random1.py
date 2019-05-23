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
#    Classe AgentRandom1
#
#    Agent qui joue de manière aléatoire
#    avec les blocs classiques
#
#-----------------------------------------------------

from tetris_engine import *
from agent import *
from random import *
import os


class AgentRandom1(Agent):
    """ Agent aléatoire jouant avec les touches du clavier """

    def __init__(self, temporisation=0.1, silent=False):
        super().__init__(name="Random 1")
        self.engine = TetrisEngine(
            self.getMove, base_blocks_bag=CLASSIC_BLOCK_BAG,
            temporisation=temporisation, silent=silent,
            agent_name=self.name, agent_description=self.decription)

    def getMove(self):
        """ Renvoie un mouvement de touche aléatoire """
        move = choice(['L', 'R', 'N', 'T', 'H', 'D'])
        return move


if __name__ == "__main__":
    player = AgentRandom1()
    playGame(player, temporisation=0.1)
