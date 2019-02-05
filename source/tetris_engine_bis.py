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

from tetramino_bis import *
from board_bis import *
from textutil import *
from random import *
from math import *
from time import *
import os


class TetrisEngine:
    def __init__(self, getMove, width=10, height=22, max_blocks=0,
                 base_blocks_bag=RAPID_BLOCK_BAG,
                 temporisation=0, silent=False, random_generator_seed=None,
                 agent_name="", agent_description=""):
        self.width = width
        self.height = height

        # La grille "dynamique" dans laquelle les pièces tombent
        self.board = Board(width, height)
        # La grille constituée des pièces placées
        self.fixed_board = self.board.copy()
        # La fonction de callback à appeler pour jouer un coup
        self.getMove = getMove

        # Gestion des blocs
        seed(random_generator_seed)
        self.base_blocks_bag = base_blocks_bag
        self.blocks_bag = []
        self.generateNewBlockBag()
        self.block = None
        self.block_position = [0, 0]
        self.next_block = self.blocks_bag.pop()

        self.max_blocks = max_blocks
        self.nb_blocks_played = 0

        # Scores
        self.score = 0
        self.score_on_move = 0
        self.total_lines = 0

        # Lancement du moteur
        self.isRunning = True

        # Affichage ou non
        self.silent = silent

        # Nom de l'agent
        self.agent_name = agent_name
        self.agent_description = agent_description

        # Timings
        self.temporisation = temporisation
        self.time_for_move = 0
        self.time_total_for_moves = 0
        self.time_mean = 0
        self.time_start = time()
        self.time_total = 0

    #=========================================================================
    # Initialisation des pièces
    #=========================================================================
    def generateNewBlockBag(self):
        """ Génère un nouveau sac de pièces """
        # On utilise la règle du "7-random bag" :
        # On crée un sac de 7 pièces qu'on mélange
        # Dès qu'il est vide, on regénère un nouveau sac
        self.blocks_bag = self.base_blocks_bag[:]
        shuffle(self.blocks_bag)

    def generateNewBlock(self):
        """ Remplace le bloc courant par le suivant et fabrique un nouveau bloc suivant """
        self.block = self.next_block.copy()
        # Si le sac est vide, on en recrée un nouveau
        if len(self.blocks_bag) == 0:
            self.generateNewBlockBag()
        self.next_block = self.blocks_bag.pop()

    def setBlockInitPosition(self):
        """ Position initiale pour un nouveau bloc """
        # Un nouveau bloc est placé sur la ligne cachée au milieu
        self.block_position[0] = self.board.height + 1
        self.block_position[1] = self.board.width // 2 - \
            ceil((self.block.jmax + 1) / 2)

    def getNewBlock(self):
        """ Met un nouveau bloc en jeu """
        self.generateNewBlock()
        self.setBlockInitPosition()
        self.placeBlock(self.block, self.block_position)
        self.nb_blocks_played += 1

    #=========================================================================
    # Déplacements et rotations des pièces
    #=========================================================================
    def isMoveValid(self, block, new_position):
        """ Teste si une position est valide pour un bloc """
        # Teste si le bloc sort de la grille
        if new_position[1] + block.jmax >= self.board.width or new_position[0] - block.imax < 0 \
                or new_position[0] - block.imin > self.board.height + 1 or new_position[1] + block.jmin < 0:
            return False

        # Teste si les nouvelles cases occupées par le bloc sont vides
        for (i, j) in block.glyph:
            if not self.fixed_board.isCellEmpty(new_position[0] - i, new_position[1] + j):
                return False
        return True

    def placeBlock(self, block, position):
        """ Place un bloc dans une position """
        for (i, j) in block.glyph:
            self.board.setCell(position[0] - i, position[1] + j, block.id)

    def eraseBlock(self):
        """ Efface le bloc de sa position """
        for (i, j) in self.block.glyph:
            self.board.emptyCell(
                self.block_position[0] - i, self.block_position[1] + j)

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
        """ Fait tomber le bloc en bas """
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
        # On essaie de placer le bloc sur sa ligne dans la colonne donnée
        new_position = [self.block_position[0], column]
        return self.isMoveValid(new_block, new_position)

    def getPossibleMovesDirect(self):
        """ Renvoie la liste de tous les placements directs possibles
            sous la forme de tuples (column, rotation) """
        self.direct_placements = []
        index = self.block.glyph_index
        for rotation in range(self.block.nb_rotations):
            self.block.setRotation(rotation)
            jmin = self.block.jmin
            jmax = self.block.jmax
            for column in range(0 - jmin, self.width - jmax):
                if self.isMoveValid(self.block, [self.block_position[0], column]):
                    self.direct_placements.append((column, rotation))
        self.block.setRotation(index)
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

    #=========================================================================
    # Commandes
    #=========================================================================
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

    #=========================================================================
    # Scores
    #=========================================================================
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

    #=========================================================================
    # Affichage en mode console
    #=========================================================================
    def getStrInfos(self):
        """ Renvoie une chaîne contenant les informations de la partie """
        chain = "Score : %d\n" % self.score
        chain += "\n"
        chain += "BlocksBag : %s\n" % " ".join([str(b.id)
                                                for b in self.blocks_bag])
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
        """ Renvoie une chaîne pour afficher le bloc suivant """
        return "NEXT : \n" + boxed(str(self.next_block), window_width=6, window_height=4)

    def printRightColumn(self):
        """ Renvoie la chaîne correspondant au côté droit de l'affichage """
        return self.getStrInfos() + "\n\n" + self.getStrNextBlock()

    def getStrAgentName(self):
        """ Renvoie la chaîne contenant les nom et la description de l'agent """
        if not self.agent_name:
            return ""
        return boxed(self.agent_name) + "\n\n"

    def __str__(self):
        """ Renvoie une chaîne représentant l'état de la partie """
        return self.getStrAgentName() + mergeChains(str(self.board), self.printRightColumn())

    #=========================================================================
    # Méthodes utilitaires
    #=========================================================================
    def copy(self):
        """ Renvoie une copie de l'environnement """
        return self.minimalCopy()

    def minimalCopy(self):
        """ Renvoie une copie minimale de l'environnement
            (grilles et pièces) pour tester les différents coups """
        engine = TetrisEngine(
            self.getMove, width=self.width, height=self.height)
        engine.board = self.board.copy()
        engine.fixed_board = self.fixed_board.copy()
        engine.block = self.block.copy()
        engine.next_block = self.next_block.copy()
        engine.block_position = self.block_position[:]
        return engine

    def updateTimes(self, start_time):
        """ Met à jour les chronos """
        self.time_for_move = time() - start_time
        self.time_total_for_moves += self.time_for_move
        self.time_mean = self.time_total_for_moves / self.nb_blocks_played

    #=========================================================================
    # Boucle principale
    #=========================================================================
    def run(self):
        """ Boucle principale du jeu """
        # L'algo est le suivant :
        # -----------------------
        # Tant que le jeu tourne :
        #     Met un nouveau bloc en jeu
        #     Tant que la pièce peut descendre et que le jeu tourne :
        #         Descendre la pièce d'un cran
        #         Met à jour le score sur un mouvement
        #         Met à jour l'affichage
        #         Récupère le prochain mouvement
        #         Joue ce mouvement
        #         Traite les lignes faites
        #         Met à jour le score sur les lignes
        #     Fixe la grille
        #     Teste la fin du jeu
        # Retourne le score
        while self.isRunning and (self.max_blocks == 0 or self.nb_blocks_played <= self.max_blocks):
            self.getNewBlock()
            self.time_total = time() - self.time_start
            self.score_on_move = 0
            while self.moveBlockInDirection('') and self.isRunning:
                self.score_on_move += self.getScoreFromMove()

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
                self.score_on_move += self.getScoreFromLines(nb_lines)

                self.score += self.score_on_move

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
    engine = TetrisEngine(getMove, agent_name="Toto")
    engine.run()
