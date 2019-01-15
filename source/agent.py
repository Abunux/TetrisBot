from tetris_engine import *
from random import *
from time import time
from stats import *

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
#    Classe Agent
#
#    Classe de base pour les agents
#
#-----------------------------------------------------


class Agent:
    def __init__(self, name="", description=""):
        self.name = name
        self.decription = description

#     def allMovesStats(self):
#         """ Renvoie les stats de chaque mouvement """
#         self.all_moves = {}
#         for (j, r) in self.engine.getPossibleMovesDirect():
#             engine = self.engine.copy()
#             engine.placeBlockDirect(j, r)
#             block_height = engine.getBlockHeight()
#             nb_lines = engine.board.processLines()
#             max_height = engine.board.getMaxHeight()
#             sum_heights = engine.board.getSumHeights()
#             nb_holes = engine.board.getNbHoles()
#             bumpiness = engine.board.getBumpiness()
#             self.all_moves[(j, r)] = {
#                 "block_height": block_height,
#                 "nb_lines": nb_lines,
#                 "max_height": max_height,
#                 "sum_heights": sum_heights,
#                 "nb_holes": nb_holes,
#                 "bumpiness": bumpiness
#             }
#         return self.all_moves

    def allMovesStats(self):
        """ Renvoie les stats de chaque mouvement """
        self.all_moves = {}
        for (j, r) in self.engine.getPossibleMovesDirect():
            engine = self.engine.copy()
            engine.placeBlockDirect(j, r)
            block_height = engine.getBlockHeight()
            nb_lines = engine.board.processLines()
            engine.board.updateStats()
            max_height = engine.board.max_height
            sum_heights = engine.board.sum_heights
            nb_holes = engine.board.nb_holes
            bumpiness = engine.board.bumpiness
            self.all_moves[(j, r)] = {
                "block_height": block_height,
                "nb_lines": nb_lines,
                "max_height": max_height,
                "sum_heights": sum_heights,
                "nb_holes": nb_holes,
                "bumpiness": bumpiness
            }
        return self.all_moves

    def playMove(self, move):
        """ Joue un coup (crée la commande pour engine) """
        return "P:%d:%d" % (move[0], move[1])


def benchAgent(AgentToTest, nb_samples=100, max_blocks=0):
    """ Réalise un bench de AgentToTest en jouant nb_samples parties """
    stats = {}
    scores = []
    start = time()
    print("Lancement du bench avec un échantillon de taille %d" % nb_samples)
    for k in range(nb_samples):
        if k == 1:
            print("Temps total estimé : %.0f sec" %
                  ((time() - start) * (nb_samples - 1)))
        if k > 0 and k % (nb_samples / 10) == 0:
            print("Avancement du bench: %.2f %% (Temps restant estimé : %.0f sec)" %
                  ((100 * k / nb_samples), (nb_samples - k) * (time() - start) / k))
        player = AgentToTest(silent=True)
        player.engine.max_blocks = max_blocks
        score = player.engine.run()
        scores.append(score)
    print("Avancement du bench : %.2f %%" % (100))
    total_time = time() - start
    total_score = sum(scores)
    stats["scores"] = scores
    stats["min_score"] = min(scores)
    stats["max_score"] = max(scores)
    stats["total_score"] = total_score
    stats["mean_score"] = total_score / nb_samples
    stats["total_time"] = total_time
    stats["mean_time"] = total_time / nb_samples
    print("Temps total : %.2f secondes" % total_time)
    return stats


def plotBench(AgentToTest, nb_samples, filename="", title="", nb_bars=10, max_blocks=0):
    """ Réalise un bench de AgentToTest en jouant nb_samples parties
        Affiche les réusltats sous la forme d'un histogramme avec nb_bars classes """
    s = benchAgent(AgentToTest, nb_samples=nb_samples, max_blocks=max_blocks)
    stats = Stats(data=s["scores"], mean_time=s["mean_time"],
                  filename=filename, title=title, nb_bars=nb_bars)
    stats.histogram()


def playGameWithAgent(AgentToTest, temporisation=0.1):
    """ Joue avec l'agent """
    input("Press enter to start")
    os.system("clear")
    while True:
        player = AgentToTest(temporisation=temporisation)
        player.engine.run()
        print("End of game")
        input("Press Enter to continue or CTRL+C to quit")
        os.system("clear")
