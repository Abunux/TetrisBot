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
#    Programe principal
#
#-----------------------------------------------------


from tetris_engine import *
from agent_human import *
from agent_random1 import *
from agent_random2 import *
from agent_evaluation import *
from agent_filtering import *
import os


def menuAgentType():
    print("""Choix de l'agent :
    1 : Humain
    2 : Aléatoire 1
    3 : Aléatoire 2
    4 : Évaluation
    5 : Filtrage""")
    agent = int(input("Votre choix : "))
    if agent == 1:
        AgentType = AgentHuman
    elif agent == 2:
        AgentType = AgentRandom1
    elif agent == 3:
        AgentType = AgentRandom2
    elif agent == 4:
        AgentType = AgentEvaluation
    elif agent == 5:
        AgentType = AgentFiltering
    return AgentType


if __name__ == "__main__":

    AgentType = menuAgentType()

    if AgentType == AgentHuman:
        playGameWithAgent(AgentType, temporisation=0)

    else:
        print("""Type de travail : 
        1 : Voir des parties
        2 : Satistiques (attention, peut être très long)""")
        work_type = int(input("Votre choix : "))
        if work_type == 1:
            temporisation = input("Temporisation [0.1] : ")
            if temporisation:
                temporisation = float(temporisation)
            else:
                temporisation = 0.1
            playGameWithAgent(AgentType, temporisation)
        else:
            nb_samples = input("Nombre de parties [100] : ")
            if nb_samples:
                nb_samples = int(nb_samples)
            else:
                nb_samples = 100
            max_blocks = input(
                "Nombre de blocs maximum (0 pour illimité) [500] : ")
            if max_blocks:
                max_blocks = int(max_blocks)
            else:
                max_blocks = 500

            plotBench(AgentType, nb_samples=nb_samples, max_blocks=max_blocks)
