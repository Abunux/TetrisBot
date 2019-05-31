#!/usr/bin/env python3
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
from ag_optimizer import *
from qRL_optimizer import *
from textutil import *
import os


def inputInt(text, default=0):
    """ Demande un entier et renvoie default si pas de valeur entrée """
    n = input(text + " [" + str(default) + "] : ")
    if n:
        try:
            return int(n)
        except:
            print("Entrée invalide")
            return inputInt(text, default)
    else:
        return default


def inputFloat(text, default=0):
    """ Demande un float et renvoie default si pas de valeur entrée """
    x = input(text + " [" + str(default) + "] : ")
    if x:
        try:
            return float(x)
        except:
            print("Entrée invalide")
            return inputFloat(text, default)
    else:
        return default


def menuMain():
    """ Menu principal """
    print("""Que voulez-vous faire :
    1 : Utiliser un agent
    2 : Optimisation par algorithme génétique
    3 : Optimisation par simple Q-learning """)
    choix = inputInt("Votre choix", 1)
    while choix not in [1, 2, 3]:
        print("Choix invalide")
        choix = inputInt("Votre choix", 1)
    return choix


def menuFiltering():
    filters = ["holes", "sum_heights", "bumpiness", "lines"]
    nb_filters = len(filters)
    order = []
    for k in range(nb_filters - 1):
        print("Filtre n° %d :" % (k + 1))
        for i in range(len(filters)):
            print("  %d : %s" % (i + 1, filters[i]))
        c = inputInt("Votre choix", 1)
        while c not in list(range(1, len(filters) + 1)):
            print("Choix invalide")
            c = inputInt("Votre choix", 1)
        order.append(filters.pop(c - 1))
    order.append(filters[0])
    return AgentFiltering(order=order)


def menuEvaluation():
    c1 = inputFloat("Coeff 0 (nb_lines)", 0.8)
    c2 = inputFloat("Coeff 1 (sum_heights)", 0.6)
    c3 = inputFloat("Coeff 2 (nb_holes)", 0.4)
    c4 = inputFloat("Coeff 3 (bumpiness)", 0.2)
    coeffs = [c1, c2, c3, c4]
    return AgentEvaluation(eval_coeffs=coeffs)


def menuAgentType():
    """ Menu choix de l'agent """
    print("""Choix de l'agent :
    1 : Humain
    2 : Aléatoire 1
    3 : Aléatoire 2
    4 : Filtrage
    5 : Évaluation""")
    agent = inputInt("Votre choix", 5)
    while agent not in [1, 2, 3, 4, 5]:
        print("Choix invalide")
        agent = inputInt("Votre choix", 5)
    if agent == 1:
        player = AgentHuman()
    elif agent == 2:
        player = AgentRandom1()
    elif agent == 3:
        player = AgentRandom2()
    elif agent == 4:
        player = menuFiltering()
    elif agent == 5:
        player = menuEvaluation()

    return (agent, player)


def menuAG():
    """ Menu des algos génétiques """
    print("""Encodage des vecteurs :
    1 : Binaire
    2 : Réel """)
    choix = inputInt("Votre choix", 2)
    while choix not in [1, 2]:
        print("Choix invalide")
        choix = inputInt("Votre choix", 2)
    if choix == 1:
        vector_encoding = "bin"
    else:
        vector_encoding = "float"

    if vector_encoding == "float":
        mutation_rate = inputFloat("Taux de mutation", 0.2)
    else:
        mutation_rate = 0

    print("""Méthode de sélection des parents :
    1 : Roue
    2 : Tournoi""")
    choix = inputInt("Votre choix", 2)
    while choix not in [1, 2]:
        print("Choix invalide")
        choix = inputInt("Votre choix", 2)
    if choix == 1:
        parents_selection_method = "wheel"
    else:
        parents_selection_method = "tournament"

    if parents_selection_method == "tournament":
        percentage_for_tournament = inputFloat(
            "Pourcentage de participants", 0.1)
    else:
        percentage_for_tournament = 0

    print("""Conservation des anciens individus :
    1 : Élitisme
    2 : Meilleurs
    3 : Aucun""")
    choix = inputInt("Votre choix", 2)
    while choix not in [1, 2, 3]:
        print("Choix invalide")
        choix = inputInt("Votre choix", 2)
    if choix == 1:
        old_generation_policy = "elitism"
    elif choix == 2:
        old_generation_policy = "best"
    else:
        old_generation_policy = "none"

    if old_generation_policy == "elitism":
        elitism_percentage = inputFloat("Pourcentage d'élitisme", 0.05)
    else:
        elitism_percentage = 0

    if old_generation_policy == "best":
        percentage_new_offspring = inputFloat(
            "Pourcentage de nouveaux individus", 0.30)
    else:
        percentage_new_offspring = 0

    proba_mutation = inputFloat("Probabilité de mutation", 0.05)
    population_size = inputInt("Taille de la population", 20)
    nb_generations = inputInt("Nombre de générations", 10)
    max_nb_blocks = inputInt("Nombre max de blocs", 500)
    nb_games_played = inputInt("Nombre de parties par évaluation", 5)

    print("""Critère d'évaluation :
    1 : Lignes
    2 : Score""")
    choix = inputInt("Votre choix", 1)
    while choix not in [1, 2]:
        print("Choix invalide")
        choix = inputInt("Votre choix", 1)
    if choix == 1:
        evaluation_criteria = "lines"
    else:
        evaluation_criteria = "score"

    return AGOptimizer(population_size=population_size, nb_generations=nb_generations,
                       max_nb_blocks=max_nb_blocks, nb_games_played=nb_games_played,
                       proba_mutation=proba_mutation, mutation_rate=mutation_rate,
                       percentage_for_tournament=percentage_for_tournament, percentage_new_offspring=percentage_new_offspring,
                       elitism_percentage=elitism_percentage,
                       vector_encoding=vector_encoding, parents_selection_method=parents_selection_method,
                       old_generation_policy=old_generation_policy, evaluation_criteria=evaluation_criteria)


def menuQRL():
    width = inputInt("Largeur de la grille", 5)
    height = inputInt("Hauteur de la grille", 5)
    max_episodes = inputInt("Nombre d'épisodes", 2000)
    max_blocks = inputInt("Nombre max de blocs (0 pour illimité)", 500)
    alpha = inputFloat("alpha (learning rate)", 0.1)
    gamma = inputFloat("gamma (discount factor)", 0.9)
    epsilon_delta = inputFloat("epsilon_delta", 0.001)

    return QRLOptimizer(width=width, height=height,
                        max_episodes=max_episodes, max_blocks=max_blocks,
                        alpha=alpha, gamma=gamma, epsilon_delta=epsilon_delta)


def title():
    input("Veuillez passer en plein écran et appuyer sur entrée...")
    os.system("clear")
    # Les polices ASCII art proviennent de : http://patorjk.com/software/taag/
    print(textColor("""
╔═════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                             ║
║         ████████╗███████╗████████╗██████╗ ██╗███████╗    ██████╗  ██████╗ ████████╗         ║
║         ╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝         ║
║            ██║   █████╗     ██║   ██████╔╝██║███████╗    ██████╔╝██║   ██║   ██║            ║
║            ██║   ██╔══╝     ██║   ██╔══██╗██║╚════██║    ██╔══██╗██║   ██║   ██║            ║
║            ██║   ███████╗   ██║   ██║  ██║██║███████║    ██████╔╝╚██████╔╝   ██║            ║
║            ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝            ║
║                                                                                             ║
║                                                                                             ║
║       _____      _____     _ _                   __         _____         _                 ║
║      |   __|    |     |_ _| | |___ ___    ___   |  |       |  _  |___ ___| |_ ___ ___       ║
║      |   __|_   | | | | | | | | -_|  _|  |___|  |  |__ _   |   __| . |   |  _| . |   |      ║
║      |__|  |_|  |_|_|_|___|_|_|___|_|           |_____|_|  |__|  |___|_|_|_| |___|_|_|      ║
║                                                                                             ║
║                                                                                             ║
║                 Projet Maths-infos du DU CCIE de l'université d'Aix-Marseille               ║
║                                                                                             ║
║                 Version finale : 31/05/2019                                                 ║
║                 Code du projet : https://github.com/Abunux/tetrisbot                        ║
║                                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════════════════════╝
""", bg=CBLACK, fg=CWHITE))
    input("Press enter to continue...")
    os.system("clear")


if __name__ == "__main__":
    title()
    choix = menuMain()
    if choix == 1:
        (agent, player) = menuAgentType()

        if agent == 1:
            playGame(player, temporisation=0)

        else:
            print("""Type de travail : 
    1 : Voir des parties
    2 : Satistiques (attention, peut être très long)""")
            work_type = inputInt("Votre choix", 1)
            while work_type not in [1, 2]:
                print("Choix invalide")
                work_type = inputInt("Votre choix", 1)
            if work_type == 1:
                temporisation = inputFloat("Temporisation", 0.1)
                playGame(player, temporisation=temporisation)
            else:
                nb_samples = inputInt("Nombre de parties", 100)
                max_blocks = inputInt(
                    "Nombre de blocs maximum (0 pour illimité)", 500)
                plotBenchPlayer(player, nb_samples=nb_samples,
                                max_blocks=max_blocks)
    elif choix == 2:
        ok = False
        while not ok:
            optimizer = menuAG()
            print(optimizer.stringOfParameters())
            print("Calul du temps estimé de l'optimisation....")
            estimated_time = optimizer.population_size * optimizer.max_nb_blocks * \
                optimizer.nb_games_played * optimizer.nb_generations * \
                benchTimePlayer(AgentEvaluation(), 50)
            print("Le temps estimé est de %d secondes" % int(estimated_time))
            ans = input("Voulez-vous continuer [O/n] : ")
            if ans.lower() != "n":
                ok = True
        os.system("clear")
        best_coeffs = optimizer.process()
        input("Press enter to see the agent in action...")
        os.system("clear")
        playGameWithAgentEvaluation(best_coeffs)

    elif choix == 3:
        optimizer = menuQRL()
        optimizer.learn()
        input("Press enter to see the agent in action...")
        os.system("clear")
        while True:
            optimizer.play()
            input("Press enter to continue...")
