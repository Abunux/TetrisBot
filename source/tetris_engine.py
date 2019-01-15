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
#
#    Classe TetrisEngine
#
#    Gère le placement des pièces sur la grille
#
#-----------------------------------------------------

from tetramino import *
from board import *
from textutil import *
from random import *
from math import *
from time import *
import os
from copy import deepcopy


class TetrisEngine:
    def __init__(self, getMove, width=10, height=22, max_blocks=0, temporisation=0, silent=False):
        self.width = width
        self.height = height
        self.board = Board(width, height)
        self.fixed_board = Board(width, height)

        self.getMove = getMove

        self.generateNewBlockBag()
        self.block = None
        self.next_block = self.block_bag.pop()

        self.max_blocks = max_blocks
        self.nb_blocks_played = 0
        self.block_position = [0, 0]

        self.score = 0
        self.total_lines = 0

        self.isRunning = True

        self.temporisation = temporisation
        self.silent = silent

        self.time_for_move = 0
        self.time_total_for_moves = 0
        self.time_mean = 0
        self.time_start = time()
        self.time_total = 0

    #-------------------------------------------------------------------------
    # Initialisation des pièces
    #-------------------------------------------------------------------------
    def generateNewBlockBag(self):
        self.block_bag = BLOCK_BAG[:]
        shuffle(self.block_bag)

    def generateNewBlock(self):
        """ Remplace le bloc courant par le suivant et fabrique un nouveau bloc suivant """
        self.block = self.next_block.copy()
        if len(self.block_bag) == 0:
            self.generateNewBlockBag()
        self.next_block = self.block_bag.pop()

    def setBlockInitPosition(self):
        """ Position initiale pour un nouveau bloc """
        self.block_position[0] = self.board.height + 1
        self.block_position[1] = self.board.width // 2 - \
            ceil(self.block.size / 2)

    def getUsedCellsByBlock(self):
        """ Renvoie la liste des cases occupées par le bloc courant """
        self.used_cells_by_block = []
        for i in range(self.block.size):
            for j in range(self.block.size):
                if self.block.glyph[i][j] != 0:
                    self.used_cells_by_block.append(
                        [self.block_position[0] - i, self.block_position[1] + j])
        return self.used_cells_by_block

    #-------------------------------------------------------------------------
    # Déplacements et rotations des pièces
    #-------------------------------------------------------------------------
    def isMoveValid(self, block, new_position):
        """ Teste si une position est valide pour un bloc """
        (imin, jmin, imax, jmax) = block.getBoundingBox()
        if new_position[0] - imax < 0 or new_position[0] - imin > self.board.height + 1 \
                or new_position[1] + jmin < 0 or new_position[1] + jmax >= self.board.width:
            return False

        self.getUsedCellsByBlock()
        for i in range(block.size):
            for j in range(block.size):
                if block.glyph[i][j] != 0 \
                        and not self.board.isCellEmpty(new_position[0] - i, new_position[1] + j)\
                        and [new_position[0] - i, new_position[1] + j] not in self.used_cells_by_block:
                    return False
        return True

    def placeBlock(self, block, position):
        """ Place un bloc dans une position """
        for i in range(block.size):
            for j in range(block.size):
                if block.glyph[i][j] != 0:
                    self.board.setCell(
                        position[0] - i, position[1] + j, block.glyph[i][j])

    def eraseBlock(self):
        """ Efface le bloc de sa position """
        for i in range(self.block.size):
            for j in range(self.block.size):
                if self.block.glyph[i][j] != 0:
                    self.board.emptyCell(
                        self.block_position[0] - i, self.block_position[1] + j)

    def getNewBlock(self):
        """ Met un nouveau bloc en jeu """
        self.generateNewBlock()
        self.setBlockInitPosition()
        self.placeBlock(self.block, self.block_position)
        self.nb_blocks_played += 1

    def moveBlock(self, block, new_position):
        """ Déplace un bloc vers une nouvelle position """
        self.eraseBlock()
        self.placeBlock(block, new_position)
        self.block_position = new_position[:]

    def moveBlockInDirection(self, direction=''):
        """ Déplace le bloc dans une direction :
            - 'L' : Left
            - 'R' : Right
            - '' : Vers le bas par défaut 
        """
        if direction == 'L':
            new_position = [self.block_position[0], self.block_position[1] - 1]
        elif direction == 'R':
            new_position = [self.block_position[0], self.block_position[1] + 1]
        else:
            new_position = [self.block_position[0] - 1, self.block_position[1]]

        if self.isMoveValid(self.block, new_position):
            self.moveBlock(self.block, new_position)

            return True
        else:
            return False

    def dropBlock(self):
        """ Fais tomber le bloc en bas """
        while self.moveBlockInDirection(''):
            self.score += self.getScoreFromMove()

    def rotateBlockInDirection(self, direction='H'):
        """ Tourne le bloc dans une direction :
            - 'H' : Sens Horaire
            - 'T' : Sens Trigo
        """
        new_block = self.block.copy()
        new_block.rotate(direction)
        if self.isMoveValid(new_block, self.block_position):
            self.eraseBlock()
            self.block.rotate(direction)
            self.placeBlock(self.block, self.block_position)

    def canPlaceBlockDirect(self, column, rotation):
        """ Teste si on peut placer directement un bloc 
            dans la colonne et la rotation donnée """
        new_block = self.block.copy()
        new_block.setRotation(rotation)
        new_position = [self.block_position[0], column]
        if self.isMoveValid(new_block, new_position):
            return True
        return False

    def getPossibleMovesDirect(self):
        """ Renvoie la liste de tous les placements directs possibles
            sous la forme de tuples (column, rotation) """
        self.direct_placements = []
        for column in range(-2, self.width):
            for rotation in range(self.block.nb_rotations):
                if self.canPlaceBlockDirect(column, rotation):
                    self.direct_placements.append((column, rotation))
        return self.direct_placements

    def placeBlockDirect(self, column, rotation):
        """ Place directement un bloc dans la colonne et la rotation donnée """
        new_block = self.block.copy()
        new_block.setRotation(rotation)
        new_position = [self.block_position[0], column]
        if self.isMoveValid(new_block, new_position):
            self.eraseBlock()
            self.block_position = [self.block_position[0], column]
            self.block.setRotation(rotation)
            self.placeBlock(self.block, self.block_position)
            self.dropBlock()
            return True
        return False

    def getBlockHeight(self):
        """ Renvoie la hauteur du bloc """
#         print(self.getUsedCellsByBlock())
        return max(pos[0] for pos in self.getUsedCellsByBlock())

    #-------------------------------------------------------------------------
    # Commandes
    #-------------------------------------------------------------------------
    def playCommand(self, command='N'):
        """ Joue une commande :
            - 'L' : Move Left
            - 'R' : Move Right
            - 'D' : Drop
            - 'N' : Nothing (descend d'une case)
            - 'H' : Rotate Hours direction
            - 'T' : Rotate Trigo direction
            - 'P:j:r' : Place block in column j with rotation r
            - 'S' : Restart
            - 'Q' : Quit
        """
        if command in ['R', 'L']:
            self.moveBlockInDirection(command)
        elif command == 'D':
            self.dropBlock()
        elif command in ['H', 'T']:
            self.rotateBlockInDirection(command)
        elif len(command) > 1 and command[0] == 'P':
            self.placeBlockDirect(
                int(command.split(':')[1]), int(command.split(':')[2]))
        elif command == 'S':
            self.__init__(self.width, self.height)
        elif command == 'Q':
            self.isRunning = False
        else:
            pass

    def isEndGame(self):
        """ Teste la fin du jeu """
        return self.fixed_board.max_height > self.board.height

    #-------------------------------------------------------------------------
    # Score
    #-------------------------------------------------------------------------
    def getScoreFromLines(self, nb_lines):
        """ Renvoie le score suivant le nombre de lignes faites """
        if nb_lines == 0:
            return 0
        elif nb_lines == 1:
            return 40
        elif nb_lines == 2:
            return 100
        elif nb_lines == 3:
            return 300
        else:
            return 1200

    def getScoreFromMove(self):
        """ Renvoie le score pour chaque déplacement vers le bas """
        return 1

    #-------------------------------------------------------------------------
    # Affichage en mode console
    #-------------------------------------------------------------------------
    def getStrInfos(self):
        chain = "Score : %d\n" % self.score
        chain += "\n"
        chain += "BlocksBag : %s\n" % " ".join([str(b.id)
                                                for b in self.block_bag])
        chain += "\n"
        chain += "MaxHeight  : %d\n" % self.fixed_board.getMaxHeight()
        chain += "SumHeights : %d\n" % self.fixed_board.getSumHeights()
        chain += "Bumpiness  : %d\n" % self.fixed_board.getBumpiness()
        chain += "Holes      : %d\n" % self.fixed_board.getNbHoles()
        chain += "Nb blocks  : %d\n" % (self.nb_blocks_played - 1)
        chain += "Nb lines   : %d\n" % self.total_lines
        chain += "\n"
        chain += "Time for move         : %.4f s\n" % self.time_for_move
        chain += "Total time for moves  : %.4f s\n" % self.time_total_for_moves
        chain += "Mean time for moves   : %.4f s\n" % self.time_mean
        chain += "Total time            : %.4f s\n" % self.time_total

        return boxed(chain.strip(), window_width=38)

    def getStrNextBlock(self):
        return "NEXT : \n" + boxed(str(self.next_block), window_width=6, window_height=4)

    def printRightColumn(self):
        return self.getStrInfos() + "\n\n" + self.getStrNextBlock()

    def __str__(self):
        return mergeChains(str(self.board), self.printRightColumn())

    def copy(self):
        """ Renvoie une copie de l'environnement """
        return deepcopy(self)

    def updateTimes(self, start_time):
        """ Mets à jour les chronos """
        self.time_for_move = time() - start_time
        self.time_total_for_moves += self.time_for_move
        self.time_mean = self.time_total_for_moves / self.nb_blocks_played

    def run(self):
        """ Boucle principale du jeu """
        while self.isRunning and (self.max_blocks == 0 or self.nb_blocks_played < self.max_blocks):
            self.getNewBlock()
            self.time_total = time() - self.time_start
            while self.moveBlockInDirection('') and self.isRunning:
                self.score += self.getScoreFromMove()

                if not self.silent:
                    print(self)
                    start_time = time()
                    move = self.getMove()
                    self.updateTimes(start_time)
                    sleep(self.temporisation)
                    os.system("clear")
                else:
                    start_time = time()
                    move = self.getMove()
                    self.updateTimes(start_time)

                self.playCommand(move)

                nb_lines = self.board.processLines()
                self.total_lines += nb_lines
                self.score += self.getScoreFromLines(nb_lines)

            self.fixed_board = self.board.copy()
            self.fixed_board.updateStats()

            if self.isEndGame():
                if not self.silent:
                    print(self)
                self.isRunning = False
        return self.score


if __name__ == "__main__":
    def getMove():
        print("""L : Move Left
R : Move Right
D : Drop
H : Rotate Hours
T : Rotate Trigo
Enter : Down 
S : Restart
Q : Quit""")
        move = input("Mouvement : ")
        return move.upper()
    engine = TetrisEngine(getMove)
    engine.run()