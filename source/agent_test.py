#!/usr/bin/env python3

from tetris_engine import *
from random import *
from time import time


class AgentTest:
    def __init__(self, temporisation=0.1, optimisation=1, silent=False):
        if optimisation == 1:
            self.engine = TetrisEngine(
                self.getMove, temporisation=temporisation, silent=silent)
        elif optimisation == 2:
            self.engine = TetrisEngine(
                self.getMove2, temporisation=temporisation, silent=silent)
        elif optimisation == 3:
            self.engine = TetrisEngine(
                self.getMove3, temporisation=temporisation, silent=silent)
        elif optimisation == 4:
            self.engine = TetrisEngine(
                self.getMove4, temporisation=temporisation, silent=silent)
        elif optimisation == 5:
            self.engine = TetrisEngine(
                self.getMove5, temporisation=temporisation, silent=silent)
        elif optimisation == 6:
            self.engine = TetrisEngine(
                self.getMove6, temporisation=temporisation, silent=silent)

    def getMove(self):
        """ Optimisation par le nombre de trous """
        min_holes = self.engine.width * self.engine.height
        best_move = (0, 0)
        for (j, r) in self.engine.getPossibleMovesDirect():
            engine = self.engine.copy()
            engine.placeBlockDirect(j, r)
            nb_holes = engine.board.getNbHoles()
            if nb_holes < min_holes:
                min_holes = nb_holes
                best_move = (j, r)

        return "P:%d:%d" % best_move

    def getMove2(self):
        """ Optimisation par la hauteur max """
        min_height = self.engine.height
        best_move = (0, 0)
        for (j, r) in self.engine.getPossibleMovesDirect():
            engine = self.engine.copy()
            engine.placeBlockDirect(j, r)
            engine.board.processLines()
            max_height = engine.board.getMaxHeight()
            if max_height < min_height:
                min_height = max_height
                best_move = (j, r)

        return "P:%d:%d" % best_move

    def getMove3(self):
        """ Optimisation par le nombre de lignes,
            puis la hauteur max,
            et enfin par le nombre de trous """
        min_holes = self.engine.width * self.engine.height
        min_height = self.engine.height
        max_lines = 0
        best_move = (0, 0)
        for (j, r) in self.engine.getPossibleMovesDirect():
            engine = self.engine.copy()
            engine.placeBlockDirect(j, r)
            nb_lines = engine.board.processLines()
            max_height = engine.board.getMaxHeight()
            nb_holes = engine.board.getNbHoles()
            if nb_lines > max_lines:
                max_lines = nb_lines
                best_move = (j, r)
            elif max_lines == 0 and max_height < min_height:
                min_height = max_height
                best_move = (j, r)
            elif max_lines == 0 and max_height == min_height and nb_holes < min_holes:
                min_holes = nb_holes
                best_move = (j, r)

        return "P:%d:%d" % best_move

    def getMove4(self):
        """ Optimisation par la hauteur max,
            puis par le nombre de trous """
        min_holes = self.engine.width * self.engine.height
        min_height = self.engine.height
        best_move = (0, 0)
        for (j, r) in self.engine.getPossibleMovesDirect():
            engine = self.engine.copy()
            engine.placeBlockDirect(j, r)
            engine.board.processLines()
            max_height = engine.board.getMaxHeight()
            nb_holes = engine.board.getNbHoles()
            if max_height < min_height:
                min_height = max_height
                best_move = (j, r)
            elif max_height == min_height and nb_holes < min_holes:
                min_holes = nb_holes
                best_move = (j, r)

        return "P:%d:%d" % best_move

    def getMove5(self):
        """ Optimisation par le nombre de trous,
            puis par la hauteur max """
        min_holes = self.engine.width * self.engine.height
        min_height = self.engine.height
        best_move = (0, 0)
        for (j, r) in self.engine.getPossibleMovesDirect():
            engine = self.engine.copy()
            engine.placeBlockDirect(j, r)
            engine.board.processLines()
            max_height = engine.board.getMaxHeight()
            nb_holes = engine.board.getNbHoles()
            if nb_holes < min_holes:
                min_holes = nb_holes
                best_move = (j, r)
            if nb_holes == min_holes and max_height < min_height:
                min_height = max_height
                best_move = (j, r)

        return "P:%d:%d" % best_move

    def getMove6(self):
        """ Optimisation par la hauteur max,
            puis par le nombre de trous 
            puis par le bumpiness"""
        min_holes = self.engine.width * self.engine.height
        min_height = self.engine.height
        min_bumpiness = self.engine.width * self.engine.height
        best_move = (0, 0)
        for (j, r) in self.engine.getPossibleMovesDirect():
            engine = self.engine.copy()
            engine.placeBlockDirect(j, r)
            engine.board.processLines()
            max_height = engine.board.getMaxHeight()
            nb_holes = engine.board.getNbHoles()
            bumpiness = engine.board.getBumpiness()
            if max_height < min_height:
                min_height = max_height
                best_move = (j, r)
            elif max_height == min_height and nb_holes < min_holes:
                min_holes = nb_holes
                best_move = (j, r)
            elif max_height == min_height and nb_holes == min_holes and bumpiness < min_bumpiness:
                min_bumpiness = bumpiness
                best_move = (j, r)

        return "P:%d:%d" % best_move


if __name__ == "__main__":
    while True:
        player = AgentTest(optimisation=6)
        player.engine.run()
        print("End of game")
        input("Press Enter to continue")
        os.system("clear")

#     s1, s2, s3, s4, s5, s6 = 0, 0, 0, 0, 0, 0
#     n = 10
#     t0 = time()
#     for k in range(n):
#         print("%.2f %%" % (100 * k / n))
#         player = AgentTest(optimisation=1, temporisation=0, silent=True)
#         s1 += player.engine.run()
#     t1 = time()
#     for k in range(n):
#         print("%.2f %%" % (100 * k / n))
#         player = AgentTest(optimisation=2, temporisation=0, silent=True)
#         s2 += player.engine.run()
#     t2 = time()
#     for k in range(n):
#         print("%.2f %%" % (100 * k / n))
#         player = AgentTest(optimisation=3, temporisation=0, silent=True)
#         s3 += player.engine.run()
#     t3 = time()
#     for k in range(n):
#         print("%.2f %%" % (100 * k / n))
#         player = AgentTest(optimisation=4, temporisation=0, silent=True)
#         s4 += player.engine.run()
#     t4 = time()
#     t5 = time()
#     for k in range(n):
#         print("%.2f %%" % (100 * k / n))
#         player = AgentTest(optimisation=6, temporisation=0, silent=True)
#         s6 += player.engine.run()
#     t6 = time()
#     print("%.2f - %.2f sec " % (s1 / n, (t1 - t0) / n))
#     print("%.2f - %.2f sec " % (s2 / n, (t2 - t1) / n))
#     print("%.2f - %.2f sec " % (s3 / n, (t3 - t2) / n))
#     print("%.2f - %.2f sec " % (s4 / n, (t4 - t3) / n))
#     print("%.2f - %.2f sec " % (s6 / n, (t6 - t5) / n))
