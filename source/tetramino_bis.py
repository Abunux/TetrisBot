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

# from copy import deepcopy
# import numpy as np


class Tetramino:
    def __init__(self, id, rotations, corners):
        self.id = id
#         self.rotations = np.array(rotations, dtype=np.int8)
        self.rotations = rotations
        self.nb_rotations = len(self.rotations)
        self.corners = None
#         self.corners = corners
#         self.getCorners()
        self.glyph_index = 0
        self.glyph = self.rotations[0]
        self.getCorner()
#         self.imax = self.getImax()
#         self.jmax = self.getJmax()

    def getCorner(self):
        #         (self.imax, self.jmax) = self.corners[self.glyph_index]
        (self.imax, self.jmax) = (self.getImax(), self.getJmax())

    def getImax(self):
        #         return np.max(self.glyph[:, 0])
        return max([self.glyph[k][0] for k in range(len(self.glyph))])
#         return self.corners[self.glyph_index][0]

    def getJmax(self):
        #         return np.max(self.glyph[:, 1])
        return max([self.glyph[k][1] for k in range(len(self.glyph))])
#         return self.corners[self.glyph_index][1]

#     def getCorners(self):
#         self.corners = []
#         for k in range(self.nb_rotations):
#             self.corners.append((max([self.rotations[k][i][0] for i in range(len(self.rotations[k]))]),
#                                  max([self.rotations[k][i][1]
#                                       for i in range(len(self.rotations[k]))])
#                                  ))

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
        self.getCorner()
#         self.imax = self.getImax()
#         self.jmax = self.getJmax()

    def setRotation(self, i):
        """ Tourne directement une pièce """
        i = i % self.nb_rotations
        self.glyph_index = i
        self.glyph = self.rotations[i]
        self.getCorner()
#         self.imax = self.getImax()
#         self.jmax = self.getJmax()

    def copy(self):
        """ Renvoie une copie de la pièce """
#         return deepcopy(self)
        new_block = Tetramino(self.id, self.rotations, self.corners)
        new_block.setRotation(self.glyph_index)
        new_block.getCorner()
        return new_block

    def __str__(self):
        """ Renvoie une représentation textuelle des blocs """
        self.getCorner()
        charsGlyph = [["."] * (self.jmax + 1) for i in range(self.imax + 1)]
        for (i, j) in self.glyph:
            charsGlyph[i][j] = str(self.id)
        strGlyph = ""
        for i in range(self.imax + 1):
            for j in range(self.jmax + 1):
                strGlyph += charsGlyph[i][j]
            strGlyph += "\n"
        return strGlyph


#=========================================================================
# Création des blocs
#=========================================================================
# I Block
ID_IBLOCK = 1
I0 = [[0, 0],
      [0, 1],
      [0, 2],
      [0, 3]]
I1 = [[0, 0],
      [1, 0],
      [2, 0],
      [3, 0]]
IBLOCK = Tetramino(ID_IBLOCK, [I0, I1], ((0, 3), (3, 0)))

# O Block
ID_OBLOCK = 2
O0 = [[0, 0],
      [0, 1],
      [1, 0],
      [1, 1]]
OBLOCK = Tetramino(ID_OBLOCK, [O0], ((1, 1),))

# T Block
ID_TBLOCK = 3
T0 = [[0, 1],
      [1, 0],
      [1, 1],
      [1, 2]]
T1 = [[0, 0],
      [1, 0],
      [1, 1],
      [2, 0]]
T2 = [[0, 0],
      [0, 1],
      [0, 2],
      [1, 1]]
T3 = [[0, 1],
      [1, 0],
      [1, 1],
      [2, 1]]
TBLOCK = Tetramino(ID_TBLOCK, [T0, T1, T2, T3], (
                   (1, 2), (2, 1), (1, 2), (2, 1)))

# S Block
ID_SBLOCK = 4
S0 = [[0, 1],
      [0, 2],
      [1, 0],
      [1, 1]]
S1 = [[0, 0],
      [1, 0],
      [1, 1],
      [2, 1]]
SBLOCK = Tetramino(ID_SBLOCK, [S0, S1], ((1, 2), (2, 1)))

# Z Block
ID_ZBLOCK = 5
Z0 = [[0, 0],
      [0, 1],
      [1, 1],
      [1, 2]]
Z1 = [[0, 1],
      [1, 0],
      [1, 1],
      [2, 0]]
ZBLOCK = Tetramino(ID_ZBLOCK, [Z0, Z1],  ((1, 2), (2, 1)))

# L Block
ID_LBLOCK = 6
L0 = [[0, 0],
      [1, 0],
      [1, 1],
      [1, 2]]
L1 = [[0, 0],
      [0, 1],
      [1, 0],
      [2, 0]]
L2 = [[0, 0],
      [0, 1],
      [0, 2],
      [1, 2]]
L3 = [[0, 1],
      [1, 1],
      [2, 0],
      [2, 1]]
LBLOCK = Tetramino(ID_LBLOCK, [L0, L1, L2, L3], (
                   (1, 2), (2, 1), (1, 2), (2, 1)))

# J Block
ID_JBLOCK = 7
J0 = [[0, 2],
      [1, 0],
      [1, 1],
      [1, 2]]
J1 = [[0, 0],
      [1, 0],
      [2, 0],
      [2, 1]]
J2 = [[0, 0],
      [0, 1],
      [0, 2],
      [1, 0]]
J3 = [[0, 0],
      [0, 1],
      [1, 1],
      [2, 1]]
JBLOCK = Tetramino(ID_JBLOCK, [J0, J1, J2, J3], (
                   (1, 2), (2, 1), (1, 2), (2, 1)))

BLOCK_BAG = [IBLOCK, OBLOCK, TBLOCK, SBLOCK, ZBLOCK, LBLOCK, JBLOCK]

#=========================================================================
# Création des blocs
#=========================================================================
# ID_IBLOCK = 1
# IBLOCK = Tetramino(ID_IBLOCK,
#                    [[0, 0, 0, 0],
#                     [1, 1, 1, 1],
#                     [0, 0, 0, 0],
#                     [0, 0, 0, 0]],
#                    2)
#
# ID_JBLOCK = 2
# JBLOCK = Tetramino(ID_JBLOCK,
#                    [[2, 0, 0],
#                     [2, 2, 2],
#                     [0, 0, 0]],
#                    4)
#
# ID_LBLOCK = 3
# LBLOCK = Tetramino(ID_LBLOCK,
#                    [[0, 0, 3],
#                     [3, 3, 3],
#                     [0, 0, 0]],
#                    4)
#
# ID_OBLOCK = 4
# OBLOCK = Tetramino(ID_OBLOCK,
#                    [[4, 4],
#                     [4, 4]],
#                    1)
#
# ID_SBLOCK = 5
# SBLOCK = Tetramino(ID_SBLOCK,
#                    [[0, 5, 5],
#                     [5, 5, 0],
#                     [0, 0, 0]],
#                    2)
#
# ID_ZBLOCK = 6
# ZBLOCK = Tetramino(ID_ZBLOCK,
#                    [[6, 6, 0],
#                     [0, 6, 6],
#                     [0, 0, 0]],
#                    2)
#
# ID_TBLOCK = 7
# TBLOCK = Tetramino(ID_TBLOCK,
#                    [[0, 7, 0],
#                     [7, 7, 7],
#                     [0, 0, 0]],
#                    4)
#
# BLOCK_BAG = [IBLOCK, JBLOCK, LBLOCK, OBLOCK, SBLOCK, ZBLOCK, TBLOCK]

if __name__ == "__main__":
    #     t = Tetramino(1,
    #                   [[[0, 0],
    #                     [1, 0],
    #                     [1, 1],
    #                     [1, 2]],
    #
    #                    [[2, 0],
    #                     [2, 1],
    #                     [1, 1],
    #                     [0, 1]]
    #                    ]
    #                   )
    #     t = Tetramino(1, [I0, I1])
    #     print(t.nb_rotations
    #           )
    #     print(t)
    #     print(t.imax())
    #     print(t.jmax())
    #
    #     t.rotate('H')
    #     print(t)
    #     print(t.imax())
    #     print(t.jmax())
    for t in BLOCK_BAG:
        #         print(t.id)
        for k in range(t.nb_rotations):
            print(t)
            print(t.imax, t.jmax)
            print()
            t.rotate("H")
