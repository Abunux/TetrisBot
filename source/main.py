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
from optimizer_algogen1 import *
from optimizer_algogen2 import *
import os


def menuMain():
    print("""Que voulez-vous faire :
    1 : Utiliser un agent
    2 : Optimisation
    """)
    choix = int(input("Votre choix : "))
    return choix


def menuAgentType():
    print("""Choix de l'agent :
    1 : Humain
    2 : Aléatoire 1
    3 : Aléatoire 2
    4 : Évaluation
    5 : Filtrage
    6 : Algorithme génétique""")
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


def menuOptimisationType():
    print("""Choix de l'optimisation :
    1 : Algo génétique 1
    2 : Algo génétique 2
    """)
    algo = int(input("Votre choix : "))
    return algo


if __name__ == "__main__":
    choix = menuMain()
    if choix == 1:
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

                plotBench(AgentType, nb_samples=nb_samples,
                          max_blocks=max_blocks)
    elif choix == 2:
        algo = menuOptimisationType()
        if algo == 1:
            population_size = input("Taille de la population [10] : ")
            if population_size:
                population_size = int(population_size)
            else:
                population_size = 10
            nb_gen = input("Nombre de générations [10] : ")
            if nb_gen:
                nb_gen = int(nb_gen)
            else:
                nb_gen = 10
            max_blocks = input("Nombre max de blocs [500] : ")
            if max_blocks:
                max_blocks = int(max_blocks)
            else:
                max_blocks = 500
            optimizer = OptimizerAlgoGen(
                population_size=population_size, nb_generations=nb_gen, max_nb_blocks=max_blocks)
            best_coeffs = optimizer.process()
            input("Press enter to see the agent in action...")
            os.system("clear")
            playGameWithAgentEvaluation(best_coeffs)
        elif choix == 2:
            population_size = input("Taille de la population [20] : ")
            if population_size:
                population_size = int(population_size)
            else:
                population_size = 20
            nb_gen = input("Nombre de générations [10] : ")
            if nb_gen:
                nb_gen = int(nb_gen)
            else:
                nb_gen = 10
            max_blocks = input("Nombre max de blocs [500] : ")
            if max_blocks:
                max_blocks = int(max_blocks)
            else:
                max_blocks = 500
            nb_games = input("Nombre de parties par évaluation [10] : ")
            if nb_games:
                nb_games = int(nb_games)
            else:
                nb_games = 10
            optimizer = OptimzerAlgoGen2(
                population_size=population_size, nb_generations=nb_gen,
                max_nb_blocks=max_blocks, nb_games_played=nb_games)
            best_coeffs = optimizer.process()
            input("Press enter to see the agent in action...")
            os.system("clear")
            playGameWithAgentEvaluation(best_coeffs)
