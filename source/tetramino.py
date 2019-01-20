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


class Tetramino:
    def __init__(self, id, base_glyph, nb_rotations=4):
        self.id = id
        self.base_glyph = base_glyph
        assert(len(base_glyph[0]) == len(base_glyph))
        self.size = len(base_glyph[0])
        self.nb_rotations = nb_rotations
        self.makeRotations()
        self.glyph_index = 0
        self.glyph = self.rotations[0]

    def getBoundingBox(self):
        """ Renvoie un tuple contenant les coordonnées des coins internes de la pièce 
            de la forme (imin, jmin, imax, jmax) """
        glyph = self.glyph
        n = self.size

        # Parcours des lignes
        i = 0
        while i < n and glyph[i] == [0] * n:
            i += 1
        imin = i
        while i < n and glyph[i] != [0] * n:
            i += 1
        imax = i - 1

        # Parcours des colonnes
        jmin = n
        jmax = 0

        for i in range(imin, imax + 1):
            j = 0
            while j < n and glyph[i][j] == 0:
                j += 1
            if j < jmin:
                jmin = j
            while j < n and glyph[i][j] != 0:
                j += 1
            if j > jmax:
                jmax = j - 1
        self.bounding_box = (imin, jmin, imax, jmax)
        return self.bounding_box

    def makeRotations(self):
        """ Crée les differentes rotations de la pièce """
        def rotateRight(glyph):
            n = self.size
            rotated_glyph = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    rotated_glyph[i][j] = glyph[n - 1 - j][i]
            return rotated_glyph

        glyph = self.base_glyph
        self.rotations = [glyph]

        for _ in range(self.nb_rotations - 1):
            glyph = rotateRight(glyph)
            self.rotations.append(glyph)

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

    def setRotation(self, i):
        """ Tourne directement une pièce """
        i = i % self.nb_rotations
        self.glyph_index = i
        self.glyph = self.rotations[i]

    def copy(self):
        """ Renvoie une copie de la pièce """
        return deepcopy(self)

    def __str__(self):
        """ Renvoie une représentation textuelle des blocs """
        n = self.size
        strGlyph = ""
        for i in range(n):
            for j in range(n):
                if (self.glyph[i][j] != 0):
                    strGlyph += str(self.id)
                else:
                    strGlyph += '.'
            strGlyph += '\n'
        return strGlyph.strip()


#=========================================================================
# Création des blocs
#=========================================================================
ID_IBLOCK = 1
IBLOCK = Tetramino(ID_IBLOCK,
                   [[0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]],
                   2)

ID_JBLOCK = 2
JBLOCK = Tetramino(ID_JBLOCK,
                   [[2, 0, 0],
                    [2, 2, 2],
                    [0, 0, 0]],
                   4)

ID_LBLOCK = 3
LBLOCK = Tetramino(ID_LBLOCK,
                   [[0, 0, 3],
                    [3, 3, 3],
                    [0, 0, 0]],
                   4)

ID_OBLOCK = 4
OBLOCK = Tetramino(ID_OBLOCK,
                   [[4, 4],
                    [4, 4]],
                   1)

ID_SBLOCK = 5
SBLOCK = Tetramino(ID_SBLOCK,
                   [[0, 5, 5],
                    [5, 5, 0],
                    [0, 0, 0]],
                   2)

ID_ZBLOCK = 6
ZBLOCK = Tetramino(ID_ZBLOCK,
                   [[6, 6, 0],
                    [0, 6, 6],
                    [0, 0, 0]],
                   2)

ID_TBLOCK = 7
TBLOCK = Tetramino(ID_TBLOCK,
                   [[0, 7, 0],
                    [7, 7, 7],
                    [0, 0, 0]],
                   4)

BLOCK_BAG = [IBLOCK, JBLOCK, LBLOCK, OBLOCK, SBLOCK, ZBLOCK, TBLOCK]

if __name__ == "__main__":
    for t in BLOCK_BAG:
        print(t)
        print(t.getBoundingBox())
        print()
        t.rotate("H")
        print(t)
        print(t.getBoundingBox())
        print()
        t.rotate("H")
        print(t)
        print(t.getBoundingBox())
        print()
        t.rotate("H")
        print(t)
        print(t.getBoundingBox())
        print()
