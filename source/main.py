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
from optimizer_algogen3 import *
from optimizer_algogen2 import *
import os


def inputInt(text, default=0):
    """ Demande un entier et renvoie default si pas de valeur entrée """
    n = input(text)
    if n:
        return int(n)
    else:
        return default


def inputFloat(text, default=0):
    """ Demande un float et renvoie default si pas de valeur entrée """
    x = input(text)
    if x:
        return float(x)
    else:
        return default


def menuMain():
    """ Menu principal """
    print("""Que voulez-vous faire :
    1 : Utiliser un agent
    2 : Optimisation
    """)
    choix = int(input("Votre choix : "))
    return choix


def menuAgentType():
    """ Menu choix de l'agent """
    print("""Choix de l'agent :
    1 : Humain
    2 : Aléatoire 1
    3 : Aléatoire 2
    4 : Filtrage
    5 : Évaluation
    """)
    agent = int(input("Votre choix : "))
    if agent == 1:
        player = AgentHuman()
    elif agent == 2:
        player = AgentRandom1()
    elif agent == 3:
        player = AgentRandom2()
    elif agent == 4:
        player = AgentFiltering()
    elif agent == 5:
        c1 = inputFloat("Coeff 1 [0.8] : ", 0.8)
        c2 = inputFloat("Coeff 2 [0.6] : ", 0.6)
        c3 = inputFloat("Coeff 3 [0.4] : ", 0.4)
        c4 = inputFloat("Coeff 4 [0.2] : ", 0.2)
        coeffs = [c1, c2, c3, c4]
        player = AgentEvaluation(eval_coeffs=coeffs)

    return (agent, player)


def menuOptimisationType():
    """ Menu choix de l'optimisation """
    print("""Choix de l'optimisation :
    1 : Algo génétique 1
    2 : Algo génétique 2
    """)
    algo = int(input("Votre choix : "))
    return algo


if __name__ == "__main__":
    choix = menuMain()
    if choix == 1:
        (agent, player) = menuAgentType()

        if agent == 1:
            playGame(player, temporisation=0)

        else:
            print("""Type de travail : 
    1 : Voir des parties
    2 : Satistiques (attention, peut être très long)""")
            work_type = int(input("Votre choix : "))
            if work_type == 1:
                temporisation = inputInt("Temporisation [0.1] : ", 0.1)
                playGame(player, temporisation=temporisation)
            else:
                nb_samples = inputInt("Nombre de parties [100] : ", 100)
                max_blocks = inputInt(
                    "Nombre de blocs maximum (0 pour illimité) [500] : ", 500)
                plotBenchPlayer(player, nb_samples=nb_samples,
                                max_blocks=max_blocks)
    elif choix == 2:
        ok = False
        while not ok:
            algo = menuOptimisationType()
            if algo == 1:
                population_size = inputInt(
                    "Taille de la population [20] : ", 20)
                nb_gen = inputInt("Nombre de générations [10] : ", 10)
                max_blocks = inputInt("Nombre max de blocs [500] : ", 500)
                nb_games = inputInt(
                    "Nombre de parties par évaluation [5] : ", 5)
                optimizer = OptimizerAlgoGen3(
                    population_size=population_size, nb_generations=nb_gen,
                    max_nb_blocks=max_blocks, nb_games_played=nb_games)
            elif choix == 2:
                population_size = inputInt(
                    "Taille de la population [20] : ", 20)
                nb_gen = inputInt("Nombre de générations [10] : ", 10)
                max_blocks = inputInt("Nombre max de blocs [500] : ", 500)
                nb_games = inputInt(
                    "Nombre de parties par évaluation [5] : ", 5)
                optimizer = OptimzerAlgoGen2(
                    population_size=population_size, nb_generations=nb_gen,
                    max_nb_blocks=max_blocks, nb_games_played=nb_games)
            print("Calul du temps estimé de l'optimisation....")
            estimated_time = population_size * max_blocks * \
                nb_games * nb_gen * benchTimePlayer(AgentEvaluation(), 50)
            print("Le temps estimé est de %d secondes" % int(estimated_time))
            ans = input("Voulez-vous continuer [O/n] : ")
            if ans.lower() != "n":
                ok = True
        os.system("clear")
        best_coeffs = optimizer.process()
        input("Press enter to see the agent in action...")
        os.system("clear")
        playGameWithAgentEvaluation(best_coeffs)
