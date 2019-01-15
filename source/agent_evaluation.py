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
import itertools
from time import *
from agent import *


class AgentEvaluation(Agent):
    def __init__(self, eval_coeffs=[0.2, 0.2, 1, 0.2], temporisation=0.1, silent=False):
        super().__init__(name="Evaluation %s" % str(eval_coeffs))
        self.eval_coeffs = eval_coeffs
        self.engine = TetrisEngine(
            self.getMove, temporisation=temporisation, silent=silent)

    def moveEvaluation(self, move):
        """ Évalue un mouvement """
        if self.all_moves[move]["max_height"] > self.engine.height - 1:
            return -100000
        return self.eval_coeffs[0] * self.all_moves[move]["nb_lines"] \
            - self.eval_coeffs[1] * self.all_moves[move]["sum_heights"] \
            - self.eval_coeffs[2] * self.all_moves[move]["nb_holes"] \
            - self.eval_coeffs[3] * self.all_moves[move]["bumpiness"]

    def getMove(self):
        """ Optimistaion à partir de la fonction d'évaluation """
        all_moves = self.allMovesStats()
        best_move = list(all_moves.keys())[0]
        best_eval = self.moveEvaluation(best_move)
        for move in all_moves.keys():
            move_eval = self.moveEvaluation(move)
            if move_eval > best_eval:
                best_eval = move_eval
                best_move = move
        return self.playMove(best_move)


if __name__ == "__main__":
    playGameWithAgent(AgentEvaluation, temporisation=0)
    quit()

    print("End of game")
    input("Press Enter to continue or CTRL+C to quit")
    os.system("clear")

    quit()

    max_score = 0
    best_coeffs = [0, 0, 0, 0]
    best_liste = []
    coeffs = [0.2, 0.4, 0.6, 0.8, 1]
    nb_samples = 3
    nb_samples2 = 100
    max_nb_blocks = 500
    max_nb_blocks2 = 1000
#     coeffs = [0.2, 0.4]
#     nb_samples = 1
#     nb_samples2 = 1
#     max_nb_blocks = 100
#     max_nb_blocks2 = 100

    rest = len(coeffs)**4 - 1

    for c in list(itertools.product(coeffs, coeffs, coeffs, coeffs)):
        eval_coeffs = c
        dumb = False
        m = 0
        start = time()
        for k in range(nb_samples):
            player = AgentEvaluation(eval_coeffs=eval_coeffs, silent=True)
            player.engine.max_blocks = max_nb_blocks
            score = player.engine.run()
            m += score
        end = time()
        m = m / nb_samples
        if m > max_score:
            max_score = m
            best_coeffs = eval_coeffs
        if len(best_liste) <= 5:
            best_liste.append((m, c))
        else:
            best_liste.sort()
            for i in range(len(best_liste)):
                if m > best_liste[i][0]:
                    best_liste[0] = (m, c)
        print("%3d - Moyenne : %d, Coeffs : %s, Time : %.2f" %
              (rest, m, eval_coeffs, end - start))
        rest -= 1
    print("MaxMoyenne : %d, BestCoeffs : %.2f, %.2f, %.2f, %.2f" % (
        max_score, best_coeffs[0], best_coeffs[1], best_coeffs[2], best_coeffs[3]))
    print("\nWinners :\n")
    best_liste.sort()
    print(best_liste)
    print()
    max_score = 0
    best_coeffs = [0, 0, 0, 0]
    for (s, c) in best_liste:
        eval_coeffs = c
        m = 0
        start = time()
        for k in range(nb_samples2):
            player = AgentEvaluation(eval_coeffs=eval_coeffs, silent=True)
            player.engine.max_blocks = max_nb_blocks2
            score = player.engine.run()
            m += score
        end = time()
        m = m / nb_samples2
        if m > max_score:
            max_score = m
            best_coeffs = eval_coeffs
        print("Moyenne : %d, Coeffs : %s, Time : %.2f" %
              (score, eval_coeffs, end - start))
    print("MaxMoyenne : %d, BestCoeffs : %.2f, %.2f, %.2f, %.2f" % (
        max_score, best_coeffs[0], best_coeffs[1], best_coeffs[2], best_coeffs[3]))
    print("\nWinner :\n")
    print(best_coeffs)
    input()

#     max_score = 0
#     best_coeffs = [0, 0, 0, 0]
#     nb_samples = 10
#     max_nb_blocks = 100
#     while True:
#         eval_coeffs = [random() for _ in range(4)]
#         m = 0
#         for k in range(nb_samples):
#             player = AgentEvaluation(eval_coeffs=eval_coeffs, silent=True)
#             player.engine.max_blocks = max_nb_blocks
#             score = player.engine.run()
#             m += score
#
#         if m > max_score:
#             max_score = m
#             best_coeffs = eval_coeffs
#         print("Score : %d, Coeffs : %s" % (score, eval_coeffs))
#         print("MaxScore : %d, BestCoeffs : %.2f, %.2f, %.2f, %.2f" % (
# max_score, best_coeffs[0], best_coeffs[1], best_coeffs[2],
# best_coeffs[3]))

#     input("Press enter to start")
#     os.system("clear")
#     while True:
#         eval_coeffs = [random() for _ in range(4)]
#         print(eval_coeffs)
#         player = AgentEvaluation(eval_coeffs=eval_coeffs, temporisation=0)
#         player.engine.run()
#         print(eval_coeffs)
#         print("End of game")
#         input("Press Enter to continue or CTRL+C to quit")
#         os.system("clear")