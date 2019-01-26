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

from copy import deepcopy
from tetramino import *


class Board:
    def __init__(self, width=10, height=22):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height + 2)]

        self.column_heights = [0] * self.width
        self.max_height = 0
        self.sum_heights = 0
        self.bumpiness = 0
        self.nb_holes = 0
        self.nb_lines = 0

    #=========================================================================
    # Gestion des cellules de la grille
    #=========================================================================
    def getCell(self, i, j):
        """ Renvoie le contenu de la cellule (i,j) """
        return self.grid[i][j]

    def setCell(self, i, j, value):
        """ Met value dans la cellule (i,j) """
        self.grid[i][j] = value

    def emptyCell(self, i, j):
        """ Vide la cellule (i,j) """
        self.setCell(i, j, 0)

    def isCellEmpty(self, i, j):
        """ Teste si la cellule (i,j) est vide """
        return self.getCell(i, j) == 0

    def isLineFull(self, i):
        """ Teste si une ligne est pleine """
        for j in range(self.width):
            if self.isCellEmpty(i, j):
                return False
        return True

    def removeLine(self, i):
        """ Supprime la ligne i """
        del self.grid[i]
        self.grid.append([0] * self.width)

    #=========================================================================
    # Satistiques de la grille
    #=========================================================================
    def columnHeight(self, j):
        """ Renvoie la hauteur de la colonne j 
            Attention, cette fonction renvoie la hauteur et non l'indice de la dernière pièce """
        i = self.height + 1
        while i >= 0 and self.isCellEmpty(i, j):
            i -= 1
        return i + 1

    def getColumnHeights(self):
        """ Renvoie la liste des hauteurs des colonnes """
        self.column_heights = [self.columnHeight(j) for j in range(self.width)]
        return self.column_heights

    def getMaxHeight(self):
        """ Renvoie la hauteur maximum des pièces du jeu """
        self.max_height = max(self.column_heights)
        return self.max_height

    def getSumHeights(self):
        """ Renvoie la somme des hauteurs des colonnes """
        self.sum_heights = sum(self.column_heights)
        return self.sum_heights

    def getBumpiness(self):
        """ Renvoie la somme des valeurs absolues des différences
            de hauteurs entre les colonnes consécutives """
        self.bumpiness = 0
        for j in range(1, self.width):
            self.bumpiness += abs(self.column_heights[j] -
                                  self.column_heights[j - 1])
        return self.bumpiness

    def isDominated(self, i, j):
        """ Teste si une case est vide et est dominée par une case au-dessus """
        return self.isCellEmpty(i, j) and i < self.column_heights[j]
#         if not self.isCellEmpty(i, j):
#             return False
#         else:
#             for k in range(i + 1, self.column_heights[j]):
#                 if not self.isCellEmpty(k, j):
#                     return True
#             return False

    def getNbHoles(self):
        """ Renvoie le nombre de trous dans la grille
            (en fait ici juste les cases dominées) """
        self.nb_holes = 0
        for j in range(self.width):
            for i in range(self.column_heights[j]):
                if self.isDominated(i, j):
                    self.nb_holes += 1
        return self.nb_holes

    def updateStats(self):
        """ Met à jour tous les paramètres de la grille """
        self.getColumnHeights()
        self.getMaxHeight()
        self.getSumHeights()
        self.getBumpiness()
        self.getNbHoles()

    #=========================================================================
    # Gestion des lignes
    #=========================================================================
    def processLines(self):
        """ Enlève les lignes finies et renvoie le nombre de lignes enlevées """
        self.nb_lines = 0
        max_height = self.height
        i = 0
        while i < max_height:
            if self.isLineFull(i):
                self.removeLine(i)
                max_height -= 1
                self.nb_lines += 1
            else:
                i += 1
        return self.nb_lines

    #=========================================================================
    # Méthodes utilitaires
    #=========================================================================
    def copy(self):
        """ Renvoie une copie de la grille """
        return deepcopy(self)

    def __str__(self):
        """ Renvoie une représentation textuelle de la grille """
        chain = ""
        """
        for i in range(self.height + 2 - 1, -1, -1):
            chain += "%2d ║ %s ║\n" % \
                (i, " ".join([str(self.grid[i][j]) if self.grid[i][j] else "."
                              for j in range(self.width)]))
#             chain += "%2d ║ %s ║\n" % \
#                 (i, " ".join(["█" if self.grid[i][j] else "."
#                               for j in range(self.width)]))
        """
        for i in range(self.height + 2 - 1, -1, -1):
            colors = {ID_IBLOCK: "\033[48;5;50m",
                      ID_JBLOCK: "\033[48;5;27m",
                      ID_LBLOCK: "\033[48;5;202m",
                      ID_OBLOCK: "\033[48;5;226m",
                      ID_SBLOCK: "\033[48;5;82m",
                      ID_ZBLOCK: "\033[48;5;196m",
                      ID_TBLOCK: "\033[48;5;165m"
                      }
            chain += "%2d \033[48;5;232m\033[97m║\033[0m" % i
            for j in range(self.width):
                if self.grid[i][j]:
                    #                     chain += colors[self.grid[i][j]
                    #                                     ] + str(self.grid[i][j]) + "\033[0m"
                    chain += colors[self.grid[i][j]
                                    ] + "." + "\033[0m"
                else:
                    chain += "\033[48;5;232m\033[97m.\033[0m"
            chain += "\033[48;5;232m\033[97m║\033[0m\n"
            if i == self.height:
                chain += "   \033[48;5;232m\033[97m║\033[0m" + \
                    "\033[48;5;237m\033[97m-\033[0m" * \
                    (self.width) + "\033[48;5;232m\033[97m║\033[0m\n"
        chain += "   \033[48;5;232m\033[97m╚" + \
            "═" * (self.width) + "╝\033[0m\n"
        chain += "    "
        for j in range(self.width):
            chain += "%d" % j
        chain += "\n"
#             chain += "%2d ║ %s ║\n" % \
#                 (i, " ".join([str(self.grid[i][j]) if self.grid[i][j] else "."
#                               for j in range(self.width)]))
#             if i == self.height:
#                 chain += "   ║" + "-" * (2 * self.width + 1) + "║\n"
#         chain += "   ╚" + "═" * (2 * self.width + 1) + "╝\n"
#         chain += "     "
#         for j in range(self.width):
#             chain += "%d " % j
#         chain += "\n"
        return chain

    def printInfos(self):
        """ Affiche les infos de la grille (pour tests) """
        self.updateStats()
        print(self)
        for j in range(self.width):
            print("Column %d Height : %d" % (j, self.column_heights[j]))
        print("MaxHeight : %d " % self.max_height)
        print("SumHeights : %d " % self.sum_heights)
        print("Bumpiness : %d" % self.bumpiness)
        print("Holes : %d" % self.nb_holes)
        print()


if __name__ == "__main__":
    board = Board(width=3, height=5)
    board.printInfos()

    board.setCell(0, 0, 1)
    board.setCell(0, 1, 1)
    board.setCell(0, 2, 1)
    board.setCell(1, 0, 2)
    board.setCell(1, 1, 0)
    board.setCell(1, 2, 2)
    board.setCell(2, 0, 3)
    board.setCell(2, 1, 0)
    board.setCell(2, 2, 3)
    board.setCell(3, 0, 0)
    board.setCell(3, 1, 4)
    board.setCell(3, 2, 4)

    board.printInfos()

    board.processLines()
    board.printInfos()
