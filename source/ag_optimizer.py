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

from agent_evaluation import *
from textutil import *
from random import *
from time import time
from math import sqrt
import matplotlib.pyplot as plt

# Taille du vecteur de coefficients
VECTOR_SIZE = 4


# Fonctions utilitaires de calcul
def binToFloat(bits):
    """ Renvoie la représentation entre 0 et 1 d'une liste binaire 
    Le chiffre des unités étant considéré comme le 1er élément de la liste
    (ça n'a aucune importance vu qu'on va partir de listes aléatoires)"""
    x = 0
    m = 1
    for bit in bits:
        m *= 0.5
        x += m * bit
    return x


def binVectorToFloat(bin_vector):
    """ Convertit un vecteur de listes binaires en vecteur de float """
    return [binToFloat(bin_vector[k]) for k in range(VECTOR_SIZE)]


def normalize(vector):
    """ Normalise un vecteur """
    norm = sqrt(sum([v**2 for v in vector]))
    if norm != 0:
        return [v / norm for v in vector]
    else:
        return normalize([1] * VECTOR_SIZE)


def linearCombination(a1, vector1, a2, vector2):
    """ Renvoie la combinaison linéaire de deux vecteurs """
    return [a1 * vector1[k] + a2 * vector2[k] for k in range(VECTOR_SIZE)]


class AGOptimizer:
    """ Optimisation des coefficients par algorithme génétique """

    def __init__(self, population_size=20, nb_generations=2, nb_bits=16,
                 max_nb_blocks=5, nb_games_played=1,
                 proba_mutation=0.05, mutation_rate=0.2,
                 percentage_for_tournament=0.10, percentage_new_offspring=0.30,
                 elitism_percentage=0.20,
                 vector_encoding="float", parents_selection_method="tournament",
                 old_generation_policy="best", evaluation_criteria="lines"
                 ):
        # Paramètres de l'algo génétique
        self.population_size = population_size
        self.nb_generations = nb_generations
        self.nb_bits = nb_bits
        self.max_nb_blocks = max_nb_blocks
        self.nb_games_played = nb_games_played
        self.proba_mutation = proba_mutation
        self.mutation_rate = mutation_rate
        self.percentage_for_tournament = percentage_for_tournament
        self.percentage_new_offspring = percentage_new_offspring
        self.elitism_percentage = elitism_percentage

        # Encodage du vecteur de coefficients
        #    - "bin" encode le vecteur en binaire et croise les bits
        #    - "float" encode le vecteur en réel, normé et croise par combinaison linéaire
        self.vector_encoding = vector_encoding

        # Méthode de sélection de parents
        #    - "wheel" : sélection par roulette
        #    - "tournament" : selection par tournoi
        self.parents_selection_method = parents_selection_method

        # Conservation des anciens individus
        #    - "elitism" : conserve un pourcentage des meilleurs de la génération d'avant
        #    - "best" : les enfants sont mélangé aux parents et on ne garde que les meilleurs
        #    - "none" : aucun parent n'est conservé
        self.old_generation_policy = old_generation_policy

        # Critère d'évaluation
        #    - "lines" : lignes créées
        #    - "score" : score total
        #    - "height" : hauteur maximum atteinte
        self.evaluation_criteria = evaluation_criteria

        self.population = []

        # Pour les stats
        self.num_generation = 0
        self.max_scores = []
        self.average_scores = []

    def sortPopulationDescending(self):
        """ Trie la population par ordre décroissant de scores """
        self.population.sort(key=lambda p: p["score"], reverse=True)

    def randomBinaryList(self):
        """ Renvoie une liste de self.nb_bits chiffres binaires aléatoires """
        return [randint(0, 1) for _ in range(self.nb_bits)]

    def randomBinaryVector(self):
        """ Renvoie un vecteur binaire aléatoire """
        return [self.randomBinaryList() for _ in range(VECTOR_SIZE)]

    def randomFloatVector(self):
        """ Renvoie un vecteur aléatoire normé """
        return normalize([random() for _ in range(VECTOR_SIZE)])

    def scoreOnOneGame(self, vector):
        """ Score sur une partie """
        player = AgentEvaluation(
            eval_coeffs=vector, silent=True)
        player.engine.max_blocks = self.max_nb_blocks
        score = player.engine.run()
        if self.evaluation_criteria == "lines":
            return player.engine.total_lines
        elif self.evaluation_criteria == "score":
            return score
        elif self.evaluation_criteria == "height" or True:
            return -player.engine.max_height_on_game

    def fitness(self, vector):
        """ Fitness de l'individu : score total sur nb_games_played parties """
        score = 0
        for i in range(self.nb_games_played):
            score += self.scoreOnOneGame(vector)
        return score / self.nb_games_played

    def updateBinaryIndivdu(self, individu):
        """ Met à jour les paramètres d'un individu à partir de son vecteur binaire """
        bin_vector = individu["bin_vector"]
        vector = binVectorToFloat(bin_vector)
        score = self.fitness(vector)
        individu["vector"] = vector
        individu["score"] = score

    def updateScore(self, individu):
        """ Met à jour le score de l'individu """
        individu["score"] = self.fitness(individu["vector"])

    def initPopulation(self):
        """ Initialise la population """
        print("%s - Initialisation de la population..." % dateNow())
        for k in range(self.population_size):
            print("%s - Individu %d/%d" %
                  (dateNow(), k + 1, self.population_size))
            if self.vector_encoding == "bin":
                bin_vector = self.randomBinaryVector()
                vector = binVectorToFloat(bin_vector)
                score = self.fitness(vector)
                self.population.append({"bin_vector": bin_vector,
                                        "vector": vector,
                                        "score": score})
            elif self.vector_encoding == "float" or True:
                vector = self.randomFloatVector()
                self.population.append({"vector": vector, "score": 0})
                self.updateScore(self.population[k])
        self.population.sort(key=lambda p: p["score"], reverse=True)

    def wheelSelection(self):
        """ Sélection d'un individu avec une roulette """
        score_total = sum([p["score"] for p in self.population])
        probas = [p["score"] / score_total for p in self.population]
        r = random()
        k = 0
        ptotal = probas[0]
        while ptotal < r:
            k += 1
            ptotal += probas[k]
        return self.population[k]

    def tournamentSelection(self):
        """ Sélection par tournoi """
        candidates = []
        # On sélectionne au hasard un pourcentage de la population
        for k in range(int(self.population_size * self.percentage_for_tournament)):
            candidates.append(choice(self.population))
        candidates.sort(key=lambda p: p["score"], reverse=True)
        return (candidates[0], candidates[1])

    def crossover(self, parent1, parent2):
        """ Renvoie le ou les enfants de parent1 et parent2 """
        if self.vector_encoding == "bin":
            bin_vector1 = []
            bin_vector2 = []
            for k in range(VECTOR_SIZE):
                crossover_point = randrange(0, self.nb_bits)
                bin_vector1.append(parent1["bin_vector"][k][:crossover_point] +
                                   parent2["bin_vector"][k][crossover_point:])
                bin_vector2.append(parent2["bin_vector"][k][:crossover_point] +
                                   parent1["bin_vector"][k][crossover_point:])
            child1 = {"bin_vector": bin_vector1}
            child2 = {"bin_vector": bin_vector2}
            return [child1, child2]
        elif self.vector_encoding == "float" or True:
            vector = normalize(linearCombination(parent1["score"], parent1["vector"],
                                                 parent2["score"], parent2["vector"]))
            return {"vector": vector, "score": 0}

    def mutateFloatVector(self, vector):
        """ Mute un individu (son vecteur) """
        if random() < self.proba_mutation:
            delta = uniform(-self.mutation_rate, self.mutation_rate)
            i = randrange(VECTOR_SIZE)
            vi = vector[i]
            if 0 <= vi + delta <= 1:
                vector[i] += delta
                vector = normalize(vector)
        return vector

    def mutateBinVector(self, bin_vector):
        """ Mute un vecteur """
        for i in range(VECTOR_SIZE):
            for k in range(self.nb_bits):
                if random() < self.proba_mutation:
                    bin_vector[i][k] = 1 - bin_vector[i][k]
        return bin_vector

    def mutate(self, individu):
        """ Mute un individu """
        if self.vector_encoding == "bin":
            individu["bin_vector"] = self.mutateBinVector(
                individu["bin_vector"])
        elif self.vector_encoding == "float" or True:
            individu["vector"] = self.mutateFloatVector(individu["vector"])
        else:
            return

    def generateNewOffspring(self):
        """ Renvoie la nouvelle génération """
        print("%s - Création des enfants... " % dateNow())
        new_offspring = []

        # Nombre d'enfants à créer
        if self.old_generation_policy == "best":
            nb_childs_to_create = int(
                self.population_size * self.percentage_new_offspring)
        elif self.old_generation_policy == "elitism":
            nb_childs_to_create = ceil(
                self.population_size * (1 - self.elitism_percentage))
        else:
            nb_childs_to_create = self.population_size

        # On crée un certain nombre d'enfants
        created_childs = 0
        while created_childs < nb_childs_to_create:
            if self.parents_selection_method == "wheel":
                parent1 = self.wheelSelection()
                parent2 = self.wheelSelection()
            elif self.parents_selection_method == "tournament" or True:
                (parent1, parent2) = self.tournamentSelection()

            if self.vector_encoding == "bin":
                print("%s - Génération %d - Enfants %d,%d/%d" %
                      (dateNow(), self.num_generation, created_childs + 1, created_childs + 2,
                       nb_childs_to_create))
                [child1, child2] = self.crossover(parent1, parent2)
                # On mute les enfants créés
                self.mutate(child1)
                self.mutate(child2)
                # Update des enfants créés
                self.updateBinaryIndivdu(child1)
                self.updateBinaryIndivdu(child2)
                # Ajout à la liste des enfants
                new_offspring += [child1, child2]
                created_childs += 2
            elif self.vector_encoding == "float" or True:
                print("%s - Génération %d - Enfant %d/%d" %
                      (dateNow(), self.num_generation, created_childs + 1, nb_childs_to_create))
                child = self.crossover(parent1, parent2)
                # On mute l'enfant créé
                self.mutate(child)
                # Calcul de son score
                self.updateScore(child)
                # Ajout à la liste des enfants
                new_offspring.append(child)
                created_childs += 1

        return new_offspring

    def keepOnlyElite(self):
        """ Garde les meilleurs éléments de la génération précédente """
        self.sortPopulationDescending()
        self.population = self.population[:int(
            self.elitism_percentage * self.population_size)]

    def deleteWorst(self):
        """ Enlève les moins bons éléments de la population """
        self.sortPopulationDescending()
        self.population = self.population[:self.population_size]

    def makeNewGeneration(self):
        """ Crée une nouvelle génération """
        self.num_generation += 1
        new_offspring = self.generateNewOffspring()
        if self.old_generation_policy == "elitism":
            self.keepOnlyElite()
        elif self.old_generation_policy == "best":
            pass
        else:
            self.popualtion = []
        self.population += new_offspring
        self.deleteWorst()  # Au cas où on dépasse population_size

    def updateStats(self):
        """ Met à jours les statistiques """
        self.max_scores.append(self.population[0]["score"])
        self.average_scores.append(sum([self.population[k]["score"]
                                        for k in range(self.population_size)]) / self.population_size)

    def plotStats(self):
        """ Courbes de statistiques """
#         plt.title("pop_size=%d - nb_games=%d - max_blocks=%d" %
#                   (self.population_size, self.nb_games_played, self.max_nb_blocks))
        plt.subplot(212)
        plt.plot(self.average_scores, label="Average scores")
        plt.plot(self.max_scores, label="Max scores")
        plt.legend()
        plt.xlabel("Génération")
        plt.ylabel("Score")
        plt.subplot(211)
        plt.box(on=False)
        plt.xticks(())
        plt.yticks(())
        plt.text(0, 0.5, self.stringOfParameters(),
                 horizontalalignment='left', verticalalignment='center',
                 bbox=dict(facecolor='white', alpha=1))
        plt.ion()
        plt.show()

    def stringOfParameters(self):
        """ Renvoie la chaine des paramètres de l'algorithme génétique """
        s = "Algorithme génétique de paramètres : \n"
        s += "  - vector_encoding : %s\n" % self.vector_encoding
        s += "  - parents_selection_method : %s\n" % self.parents_selection_method
        s += "  - old_generation_policy : %s\n" % self.old_generation_policy
        s += "  - evaluation_criteria : %s\n" % self.evaluation_criteria
        s += "  - nb_generations = %d\n" % self.nb_generations
        s += "  - population_size = %d\n" % self.population_size
        s += "  - max_nb_blocks = %d\n" % self.max_nb_blocks
        s += "  - nb_games_played = %d\n" % self.nb_games_played
        s += "  - proba_mutation = %.2f\n" % self.proba_mutation
        if self.vector_encoding == "float":
            s += "  - mutation_rate = %.2f\n" % self.mutation_rate
        if self.parents_selection_method == "tournament":
            s += "  - percentage_for_tournament = %.2f\n" % self.percentage_for_tournament
        if self.old_generation_policy == "elitism":
            s += "  - elitism_percentage = %.2f\n" % self.elitism_percentage
        elif self.old_generation_policy == "best":
            s += "  - percentage_new_offspring = %.2f\n" % self.percentage_new_offspring

        return s

    def process(self):
        """ Boucle principale de l'optimisation """
        print(self.stringOfParameters())

        self.initPopulation()
        self.updateStats()

        for k in range(self.nb_generations):
            print("Best : %s - Score : %d" % (str(self.population[0]["vector"]),
                                              self.population[0]["score"]))
            print("Max scores :", self.max_scores)
            print("Average scores :", self.average_scores)
            print("%s : Création de la génération %d/%d" %
                  (dateNow(), k + 1, self.nb_generations))
            self.makeNewGeneration()
            self.updateStats()

        print()
        best_coeffs = self.population[0]["vector"]
        print("Best coeffs = %s" % best_coeffs)
        print()
        print("Max scores :", self.max_scores)
        print("Average scores :", self.average_scores)
        self.plotStats()
        return best_coeffs


if __name__ == "__main__":
    optimizer = AGOptimizer()
    best_coeffs = optimizer.process()

    input("Press enter to see the agent in action...")
    os.system("clear")
    while True:
        player = AgentEvaluation(
            eval_coeffs=best_coeffs, temporisation=0, silent=False)
        player.engine.run()
        print("End of game")
        input("Press Enter to continue or CTRL+C to quit")
        os.system("clear")
