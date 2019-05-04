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
from random import *
from agent import *


class AgentFiltering(Agent):
    """ Agent proccédant par filtrage des coups """

    def __init__(self,  temporisation=0.1, silent=False):
        super().__init__(name="Filtering")
        self.engine = TetrisEngine(
            self.getMove, temporisation=temporisation, silent=silent, agent_name=self.name, agent_description=self.decription)

    def minStat(self, stat):
        """ Renvoie la valeur mini d'une stat """
        min_stat = self.engine.height * self.engine.width
        for move in self.all_moves.keys():
            if self.all_moves[move][stat] < min_stat:
                min_stat = self.all_moves[move][stat]
        return min_stat

    def maxStat(self, stat):
        """ Renvoie la valeur maxi d'une stat """
        max_stat = 0
        for move in self.all_moves.keys():
            if self.all_moves[move][stat] > max_stat:
                max_stat = self.all_moves[move][stat]
        return max_stat

    def filterMoves(self, stat, value):
        """ Filtre les mouvements en récupérant uniquement ceux
            dont la stat vaut value """
        all_moves = {}
        for move in self.all_moves.keys():
            if self.all_moves[move][stat] == value:
                all_moves[move] = self.all_moves[move]
        self.all_moves = all_moves

    def getMove(self):
        """ Optimisation en filtrant successivement les mouvements 
        suivant les différentes stats """
        self.allMovesStats()

        min_holes = self.minStat("nb_holes")
        self.filterMoves("nb_holes", min_holes)

        min_sum_heights = self.minStat("sum_heights")
        self.filterMoves("sum_heights", min_sum_heights)

        min_bumpiness = self.minStat("bumpiness")
        self.filterMoves("bumpiness", min_bumpiness)

        max_lines = self.maxStat("nb_lines")
        self.filterMoves("nb_lines", max_lines)

        best_move = choice(list(self.all_moves.keys()))
        return self.commandFromMove(best_move)


if __name__ == "__main__":
    player = AgentFiltering()
    playGame(player, temporisation=0.1)

#     benchAgent(AgentFiltering, 50)
