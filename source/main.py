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
from ag_optimizer import *
import os


def inputInt(text, default=0):
    """ Demande un entier et renvoie default si pas de valeur entrée """
    n = input(text + " [" + str(default) + "] : ")
    if n:
        return int(n)
    else:
        return default


def inputFloat(text, default=0):
    """ Demande un float et renvoie default si pas de valeur entrée """
    x = input(text + " [" + str(default) + "] : ")
    if x:
        return float(x)
    else:
        return default


def menuMain():
    """ Menu principal """
    print("""Que voulez-vous faire :
    1 : Utiliser un agent
    2 : Optimisation par algorithme génétique""")
    choix = int(input("Votre choix : "))
    return choix


def menuAgentType():
    """ Menu choix de l'agent """
    print("""Choix de l'agent :
    1 : Humain
    2 : Aléatoire 1
    3 : Aléatoire 2
    4 : Filtrage
    5 : Évaluation""")
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
        c1 = inputFloat("Coeff 0 (nb_lines)", 0.8)
        c2 = inputFloat("Coeff 1 (sum_heights)", 0.6)
        c3 = inputFloat("Coeff 2 (nb_holes)", 0.4)
        c4 = inputFloat("Coeff 3 (bumpiness)", 0.2)
        coeffs = [c1, c2, c3, c4]
        player = AgentEvaluation(eval_coeffs=coeffs)

    return (agent, player)


def menuAG():
    """ Menu des algos génétiques """
    print("""Encodage des vecteurs :
    1 : Binaire
    2 : Réel """)
    choix = inputInt("votre choix", 1)
    if choix == 1:
        vector_encoding = "bin"
    else:
        vector_encoding = "float"

    if vector_encoding == "float":
        mutation_rate = inputFloat("Taux de mutation", 0.2)
    else:
        mutation_rate = 0

    print("""Méthode de sélection des parents :
    1 : Sélection
    2 : Tournoi""")
    choix = inputInt("votre choix", 1)
    if choix == 1:
        parents_selection_method = "selection"
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
    choix = inputInt("votre choix", 2)
    if choix == 1:
        old_generation_policy = "elitism"
    elif choix == 2:
        old_generation_policy = "best"
    else:
        old_generation_policy = "none"

    if old_generation_policy == "elitism":
        elitism_percentage = inputFloat(
            "Pourcentage d'élitisme", 0.05)
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

    return AGOptimizer(population_size=population_size, nb_generations=nb_generations,
                       max_nb_blocks=max_nb_blocks, nb_games_played=nb_games_played,
                       proba_mutation=proba_mutation, mutation_rate=mutation_rate,
                       percentage_for_tournament=percentage_for_tournament, percentage_new_offspring=percentage_new_offspring,
                       elitism_percentage=elitism_percentage,
                       vector_encoding=vector_encoding, parents_selection_method=parents_selection_method,
                       old_generation_policy=old_generation_policy)


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
                temporisation = inputInt("Temporisation", 0.1)
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
