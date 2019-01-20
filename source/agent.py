from tetris_engine import *
from random import *
from time import time
from stats import *
# from queue import Queue
# import threading

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
        # Dictionnaire content les stats de chaque mouvement
        self.all_moves = {}
#         self.q = Queue()

    def getMoveStats(self, move):
        """ Remplit le dictionnaire contenant les statistiques de la grille
            après que le mouvement move ait été joué """
        (j, r) = move
        engine = self.engine.copy()
        engine.placeBlockDirect(j, r)
        nb_lines = engine.board.processLines()
        engine.board.updateStats()
        max_height = engine.board.max_height
        sum_heights = engine.board.sum_heights
        nb_holes = engine.board.nb_holes
        bumpiness = engine.board.bumpiness
        self.all_moves[move] = {
            "nb_lines": nb_lines,
            "max_height": max_height,
            "sum_heights": sum_heights,
            "nb_holes": nb_holes,
            "bumpiness": bumpiness
        }

    def allMovesStats(self):
        """ Renvoie un dictionnaire contenant les stats de chaque mouvement possible 
            Les clefs sont les mouvements et les valeurs sont els stats de ce mouvement """
        self.all_moves = {}
        possible_moves_direct = self.engine.getPossibleMovesDirect()
        for (j, r) in possible_moves_direct:
            self.getMoveStats((j, r))
        return self.all_moves

    #=========================================================================
    # Essais de multithreading, pas concluant (perd en performances)
    #=========================================================================
#     def allMovesStats(self):
#         """ Renvoie les stats de chaque mouvement """
#         self.all_moves = {}
#         threads = []
#         for (j, r) in self.engine.getPossibleMovesDirect():
#             t = threading.Thread(target=self.getMoveStats, args=((j, r),))
#             threads.append(t)
#         for t in threads:
#             t.start()
#         for t in threads:
#             t.join()
#         return self.all_moves
#-----------------------------------------------------------------------------
# Autre essai (marche pas)
#-----------------------------------------------------------------------------
#     def createQueue(self):
#         for (j, r) in self.engine.getPossibleMovesDirect():
#             self.q.put((j, r))
#
#     def worker(self):
#         while True:
#             move = self.q.get()
#             self.getMoveStats(move)
#             self.q.task_done()
#
#     def allMovesStats(self):
#         """ Renvoie les stats de chaque mouvement """
#         self.all_moves = {}
#         self.createQueue()
#         threads = []
#         for i in range(2):
#             t = threading.Thread(target=self.worker)
# #             t.daemon = True
#             t.start()
#             threads.append(t)
#         self.q.join()
#         for i in range(2):
#             self.q.put(None)
#         for t in threads:
#             t.join()
#         return self.all_moves

    def commandFromMove(self, move):
        """ Renvoie la commande d'un mouvement à passer à l'engine """
        return "P:%d:%d" % (move[0], move[1])


#=========================================================================
# Fonctions pour lancer des parties
#=========================================================================
def playGameWithAgent(AgentToTest, temporisation=0.1):
    """ Lance des parties avec l'agent """
    input("Press enter to start")
    os.system("clear")
    while True:
        player = AgentToTest(temporisation=temporisation, silent=False)
        player.engine.run()
        print("End of game")
        input("Press Enter to continue or CTRL+C to quit")
        os.system("clear")


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
        Affiche les résultats sous la forme d'un histogramme avec nb_bars classes """
    s = benchAgent(AgentToTest, nb_samples=nb_samples, max_blocks=max_blocks)
    stats = Stats(data=s["scores"], mean_time=s["mean_time"],
                  filename=filename, title=title, nb_bars=nb_bars)
    stats.histogram()
