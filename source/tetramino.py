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


class Tetramino:
    """ Classe de gestion des pièces """

    def __init__(self, id, rotations, corners):
        self.id = id
        self.rotations = rotations
        self.nb_rotations = len(self.rotations)
        self.corners = corners
        self.glyph_index = 0
        self.glyph = self.rotations[0]
        self.getCorners()
        self.size = max(self.imax + 1, self.jmax + 1)

    def getCorners(self):
        """ Renvoie les coordonées des coins de la pièce """
        (self.imin, self.jmin, self.imax,
            self.jmax) = self.corners[self.glyph_index]
        return (self.imin, self.jmin, self.imax, self.jmax)

    def getLowerCell(self, j):
        """ Renvoie la ligne de la cellule la plus en bas dans la colonne j """
        return max([g[0] for g in self.glyph if g[1] == j])

    def getBottomCells(self):
        """ Renvoie les coordonnées des cellules les plus en bas """
        self.getCorners()
        self.bottom_cells = []
        for j in range(self.jmin, self.jmax + 1):
            self.bottom_cells.append([self.getLowerCell(j), j])
        return self.bottom_cells

    def rotate(self, direction='H'):
        """ Tourne la pièce dans la direction donnée 
            - 'H' : Sens Horaire
            - 'T' : Sens Trigo
        """
        if direction == 'H':
            self.glyph_index = (self.glyph_index + 1) % self.nb_rotations
        else:
            self.glyph_index = (self.glyph_index - 1) % self.nb_rotations
        self.glyph = self.rotations[self.glyph_index]
        self.getCorners()

    def setRotation(self, i):
        """ Tourne directement une pièce """
        i = i % self.nb_rotations
        self.glyph_index = i
        self.glyph = self.rotations[i]
        self.getCorners()

    def copy(self):
        """ Renvoie une copie de la pièce """
        new_block = Tetramino(self.id, self.rotations, self.corners)
        new_block.setRotation(self.glyph_index)
        return new_block

    def toArray(self):
        """ Renvoie la représentation du bloc sous forme de matrice carrée """
        self.getCorners()
        self.array = [[0] * self.size for i in range(self.size)]
        for (i, j) in self.glyph:
            self.array[i][j] = self.id
        return self.array

    def __str__(self):
        """ Renvoie une représentation textuelle des blocs """
        self.getCorners()
        self.array = self.toArray()
        return "\n".join(
            ["".join([str(self.array[i][j]) if self.array[i][j] else "."
                      for j in range(self.size)])
             for i in range(self.size)])


#=========================================================================
# Création des blocs
#=========================================================================
# Chaque bloc est défini par :
#    - Son id
#    - La liste de ses rotations : un tableau contenant les coordonnées de toutes ses cellules
#    - La liste de ses coins sous la forme (imin, jmin, imax, jmax)
#
# Par exemple, le T sur le dos :
#
#   0 1 2
# 0 . # .
# 1 # # #
# 2 . . .
#
# sera codé par ma liste [[0,1],[1,0],[1,1],[2,1]]
# et aura pour coins (0,0,1,2)
#
# Avantage : avoir un même système de codage pour les blocs rapides (coin
# en haut à gauche toujours en (0,0) et nombre minimum de rotations)
# et les blocs classiques (4 rotations autour du centre de leur matrice)

ID_IBLOCK = 1
ID_OBLOCK = 2
ID_TBLOCK = 3
ID_SBLOCK = 4
ID_ZBLOCK = 5
ID_LBLOCK = 6
ID_JBLOCK = 7

#------------------------------------------------------------------------------
# Blocs rapides
#  - Coins en haut à gauche en (0,0)
#  - Nombre minimum de rotations
#------------------------------------------------------------------------------
# I Block (rapid)
RAPID_I0 = [[0, 0],
            [0, 1],
            [0, 2],
            [0, 3]]
RAPID_I1 = [[0, 0],
            [1, 0],
            [2, 0],
            [3, 0]]
RAPID_IBLOCK = Tetramino(ID_IBLOCK,
                         [RAPID_I0, RAPID_I1],
                         ((0, 0, 0, 3), (0, 0, 3, 0))
                         )

# O Block
RAPID_O0 = [[0, 0],
            [0, 1],
            [1, 0],
            [1, 1]]
RAPID_OBLOCK = Tetramino(ID_OBLOCK,
                         [RAPID_O0],
                         ((0, 0, 1, 1),)
                         )

# T Block
RAPID_T0 = [[0, 1],
            [1, 0],
            [1, 1],
            [1, 2]]
RAPID_T1 = [[0, 0],
            [1, 0],
            [1, 1],
            [2, 0]]
RAPID_T2 = [[0, 0],
            [0, 1],
            [0, 2],
            [1, 1]]
RAPID_T3 = [[0, 1],
            [1, 0],
            [1, 1],
            [2, 1]]
RAPID_TBLOCK = Tetramino(ID_TBLOCK,
                         [RAPID_T0, RAPID_T1, RAPID_T2, RAPID_T3],
                         ((0, 0, 1, 2), (0, 0, 2, 1), (0, 0, 1, 2), (0, 0, 2, 1))
                         )

# S Block
RAPID_S0 = [[0, 1],
            [0, 2],
            [1, 0],
            [1, 1]]
RAPID_S1 = [[0, 0],
            [1, 0],
            [1, 1],
            [2, 1]]
RAPID_SBLOCK = Tetramino(ID_SBLOCK,
                         [RAPID_S0, RAPID_S1],
                         ((0, 0, 1, 2), (0, 0, 2, 1))
                         )

# Z Block
RAPID_Z0 = [[0, 0],
            [0, 1],
            [1, 1],
            [1, 2]]
RAPID_Z1 = [[0, 1],
            [1, 0],
            [1, 1],
            [2, 0]]
RAPID_ZBLOCK = Tetramino(ID_ZBLOCK,
                         [RAPID_Z0, RAPID_Z1],
                         ((0, 0, 1, 2), (0, 0, 2, 1))
                         )

# L Block
RAPID_L0 = [[0, 0],
            [1, 0],
            [1, 1],
            [1, 2]]
RAPID_L1 = [[0, 0],
            [0, 1],
            [1, 0],
            [2, 0]]
RAPID_L2 = [[0, 0],
            [0, 1],
            [0, 2],
            [1, 2]]
RAPID_L3 = [[0, 1],
            [1, 1],
            [2, 0],
            [2, 1]]
RAPID_LBLOCK = Tetramino(ID_LBLOCK,
                         [RAPID_L0, RAPID_L1, RAPID_L2, RAPID_L3],
                         ((0, 0, 1, 2), (0, 0, 2, 1), (0, 0, 1, 2), (0, 0, 2, 1))
                         )

# J Block
RAPID_J0 = [[0, 2],
            [1, 0],
            [1, 1],
            [1, 2]]
RAPID_J1 = [[0, 0],
            [1, 0],
            [2, 0],
            [2, 1]]
RAPID_J2 = [[0, 0],
            [0, 1],
            [0, 2],
            [1, 0]]
RAPID_J3 = [[0, 0],
            [0, 1],
            [1, 1],
            [2, 1]]
RAPID_JBLOCK = Tetramino(ID_JBLOCK,
                         [RAPID_J0, RAPID_J1, RAPID_J2, RAPID_J3],
                         ((0, 0, 1, 2), (0, 0, 2, 1), (0, 0, 1, 2), (0, 0, 2, 1))
                         )

# Block bag
RAPID_BLOCK_BAG = [
    RAPID_IBLOCK,
    RAPID_OBLOCK,
    RAPID_TBLOCK,
    RAPID_SBLOCK,
    RAPID_ZBLOCK,
    RAPID_LBLOCK,
    RAPID_JBLOCK
]

#------------------------------------------------------------------------------
# Blocs classiques
#  - Rotations dans une matrice carrée
#  - 4 rotations par pièce (sauf le O qui n'en n'a qu'une)
#------------------------------------------------------------------------------
# I Block
CLASSIC_I0 = [[1, 0],
              [1, 1],
              [1, 2],
              [1, 3]]
CLASSIC_I1 = [[0, 2],
              [1, 2],
              [2, 2],
              [3, 2]]
CLASSIC_I2 = [[2, 0],
              [2, 1],
              [2, 2],
              [2, 3]]
CLASSIC_I3 = [[0, 1],
              [1, 1],
              [2, 1],
              [3, 1]]
CLASSIC_IBLOCK = Tetramino(ID_IBLOCK,
                           [CLASSIC_I0, CLASSIC_I1, CLASSIC_I2, CLASSIC_I3],
                           ((1, 0, 1, 3), (0, 2, 3, 2), (2, 0, 2, 3), (0, 1, 3, 1))
                           )

# O Block
CLASSIC_O0 = [[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]]
CLASSIC_OBLOCK = Tetramino(ID_OBLOCK,
                           [CLASSIC_O0],
                           ((0, 0, 1, 1),)
                           )

# T Block
CLASSIC_T0 = [[0, 1],
              [1, 0],
              [1, 1],
              [1, 2]]
CLASSIC_T1 = [[0, 1],
              [1, 1],
              [1, 2],
              [2, 1]]
CLASSIC_T2 = [[1, 0],
              [1, 1],
              [1, 2],
              [2, 1]]
CLASSIC_T3 = [[0, 1],
              [1, 0],
              [1, 1],
              [2, 1]]
CLASSIC_TBLOCK = Tetramino(ID_TBLOCK,
                           [CLASSIC_T0, CLASSIC_T1, CLASSIC_T2, CLASSIC_T3],
                           ((0, 0, 1, 2), (0, 1, 2, 2), (1, 0, 2, 2), (0, 0, 2, 1))
                           )

# S Block
CLASSIC_S0 = [[0, 1],
              [0, 2],
              [1, 0],
              [1, 1]]
CLASSIC_S1 = [[0, 1],
              [1, 1],
              [1, 2],
              [2, 2]]
CLASSIC_S2 = [[1, 1],
              [1, 2],
              [2, 0],
              [2, 1]]
CLASSIC_S3 = [[0, 0],
              [1, 0],
              [1, 1],
              [2, 1]]
CLASSIC_SBLOCK = Tetramino(ID_SBLOCK,
                           [CLASSIC_S0, CLASSIC_S1, CLASSIC_S2, CLASSIC_S3],
                           ((0, 0, 1, 2), (0, 1, 2, 2), (1, 0, 2, 2), (0, 0, 2, 1))
                           )

# Z Block
CLASSIC_Z0 = [[0, 0],
              [0, 1],
              [1, 1],
              [1, 2]]
CLASSIC_Z1 = [[0, 2],
              [1, 1],
              [1, 2],
              [2, 1]]
CLASSIC_Z2 = [[1, 0],
              [1, 1],
              [2, 1],
              [2, 2]]
CLASSIC_Z3 = [[0, 1],
              [1, 0],
              [1, 1],
              [2, 0]]
CLASSIC_ZBLOCK = Tetramino(ID_ZBLOCK,
                           [CLASSIC_Z0, CLASSIC_Z1, CLASSIC_Z2, CLASSIC_Z3],
                           ((0, 0, 1, 2), (0, 1, 2, 2), (1, 0, 2, 2), (0, 0, 2, 1))
                           )

# L Block
CLASSIC_L0 = [[0, 0],
              [1, 0],
              [1, 1],
              [1, 2]]
CLASSIC_L1 = [[0, 1],
              [0, 2],
              [1, 1],
              [2, 1]]
CLASSIC_L2 = [[1, 0],
              [1, 1],
              [1, 2],
              [2, 2]]
CLASSIC_L3 = [[0, 1],
              [1, 1],
              [2, 0],
              [2, 1]]
CLASSIC_LBLOCK = Tetramino(ID_LBLOCK,
                           [CLASSIC_L0, CLASSIC_L1, CLASSIC_L2, CLASSIC_L3],
                           ((0, 0, 1, 2), (0, 1, 2, 2), (1, 0, 2, 2), (0, 0, 2, 1))
                           )

# J Block
CLASSIC_J0 = [[0, 2],
              [1, 0],
              [1, 1],
              [1, 2]]
CLASSIC_J1 = [[0, 1],
              [1, 1],
              [2, 1],
              [2, 2]]
CLASSIC_J2 = [[1, 0],
              [1, 1],
              [1, 2],
              [2, 0]]
CLASSIC_J3 = [[0, 0],
              [0, 1],
              [1, 1],
              [2, 1]]
CLASSIC_JBLOCK = Tetramino(ID_JBLOCK,
                           [CLASSIC_J0, CLASSIC_J1, CLASSIC_J2, CLASSIC_J3],
                           ((0, 0, 1, 2), (0, 1, 2, 2), (1, 0, 2, 2), (0, 0, 2, 1))
                           )

# Block bag
CLASSIC_BLOCK_BAG = [
    CLASSIC_IBLOCK,
    CLASSIC_OBLOCK,
    CLASSIC_TBLOCK,
    CLASSIC_SBLOCK,
    CLASSIC_ZBLOCK,
    CLASSIC_LBLOCK,
    CLASSIC_JBLOCK
]

#------------------------------------------------------------------------------
# Dominos
#------------------------------------------------------------------------------
ID_DOMINO = 1
DOMINO_0 = [[0, 0], [0, 1]]
DOMINO_1 = [[0, 0], [1, 0]]
DOMINO_BLOCK = Tetramino(
    ID_DOMINO, [DOMINO_0, DOMINO_1], ((0, 0, 0, 1), (0, 0, 1, 0)))

DOMINO_BLOCK_BAG = [DOMINO_BLOCK]

if __name__ == "__main__":
    for t in DOMINO_BLOCK_BAG:
        for k in range(t.nb_rotations):
            print(t)
            print(t.imin, t.jmin, t.imax, t.jmax)
            print(t.getBottomCells())
#             print(t.toArray())
            print()
            t.rotate("H")
