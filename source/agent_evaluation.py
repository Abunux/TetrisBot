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
#    Classe AgentEvaluation
#
#    Agent qui procède par évaluation des coups
#
#-----------------------------------------------------

# from tetris_engine import *
from random import *
import itertools
from time import *
from agent import *


class AgentEvaluation(Agent):
    """ Agent procédant par évaluation des coups """

    # Coefficients qui vont bien :
    # eval_coeffs=[0.0615, 0.1197, 0.940, 0.1373]
    # eval_coeffs=[0.8, 0.6, 0.4, 0.2]
    def __init__(self, eval_coeffs=[0.548, 0.5218, 0.6267, 0.1862], temporisation=0.1, silent=False):
        super().__init__(name="Evaluation %s" % str(eval_coeffs))
        self.eval_coeffs = eval_coeffs
        self.engine = TetrisEngine(
            self.getMove,
            base_blocks_bag=RAPID_BLOCK_BAG,
            temporisation=temporisation, silent=silent,
            agent_name=self.name, agent_description=self.decription)

    def moveEvaluation(self, move):
        """ Évalue le mouvement move=(j, r) """
        # Si le mouvement fait perdre la partie, on lui donne une évaluation
        # fortement négative
#         if self.all_moves[move]["max_height"] > self.engine.height:
#             return -10000000
        # Sinon l'évaluation est une combinaaison linéaires de critères
        return self.eval_coeffs[0] * self.all_moves[move]["nb_lines"] \
            - self.eval_coeffs[1] * self.all_moves[move]["sum_heights"] \
            - self.eval_coeffs[2] * self.all_moves[move]["nb_holes"] \
            - self.eval_coeffs[3] * self.all_moves[move]["bumpiness"]

    def getMove(self):
        """ Optimisation à partir de la fonction d'évaluation """
        all_moves = self.allMovesStats()
        best_move = list(all_moves.keys())[0]
        best_eval = self.moveEvaluation(best_move)
        for move in all_moves.keys():
            move_eval = self.moveEvaluation(move)
            if move_eval > best_eval:
                best_eval = move_eval
                best_move = move
        return self.commandFromMove(best_move)


def playGameWithAgentEvaluation(coeffs, temporisation=0):
    """ Joue des parties avec l'agent par évaluation et les coeffs donnés """
    os.system("clear")
    while True:
        player = AgentEvaluation(
            eval_coeffs=coeffs, temporisation=temporisation, silent=False)
        player.engine.run()
        print("End of game")
        input("Press Enter to continue or CTRL+C to quit")
        os.system("clear")


if __name__ == "__main__":
    pass
    player = AgentEvaluation()
    playGame(player, temporisation=0)
    input()
    quit()

    s = 0
    n = 10
    for k in range(n):
        player = AgentEvaluation()
        t = benchTimePlayer(player, 500)
        print(t)
        s += t
    print("Moyenne :", s / n)
#     playGame(player, temporisation=0)
    input()
    quit()
