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
from agent import *
import os


class AgentHuman(Agent):
    def __init__(self, temporisation=0, silent=False):
        self.engine = TetrisEngine(
            self.getMove, temporisation=temporisation, silent=silent)

    def getMove(self):
        print("""L : Move Left
R : Move Right
D : Drop
H : Rotate Hours
T : Rotate Trigo
Enter : Down 
P:j:r : Direct placement in column j with rotation r
S : Restart
Q : Quit""")
        move = input("Mouvement : ")
        return move.upper()


if __name__ == "__main__":
    player = AgentHuman()
    player.engine.run()
    print("End of game")
    input("Press Enter to continue or CTRL+C to quit")
    os.system("clear")