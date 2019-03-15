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

from agent_evaluation import *
from random import *
from time import time
from math import *
import matplotlib.pyplot as plt


# Fonctions utilitaires de conversion
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
    return [binToFloat(bin_vector[k]) for k in range(4)]


class OptimizerAlgoGen3:
    def __init__(self, nb_bits=16, population_size=50, nb_generations=20,
                 max_nb_blocks=500, nb_games_played=10,
                 proba_mutation=0.05, elitism_percentage=0.20):
        self.nb_bits = nb_bits
        self.population_size = population_size
        self.proba_mutation = proba_mutation
        self.max_nb_blocks = max_nb_blocks
        self.nb_games_played = nb_games_played
        self.nb_generations = nb_generations
        self.elitism_percentage = elitism_percentage
#         self.percentage_new_offspring = percentage_new_offspring

        self.population = []

        # Pour les stats
        self.num_generation = 0
        self.max_scores = []
        self.average_scores = []

    def sortPopulationDescending(self):
        """ Trie la population par ordre décroissant de scores """
        self.population.sort(key=lambda p: p["score"], reverse=True)

#     def sortPopulationAscending(self):
#         """ Trie la population par ordre croissant de scores """
#         self.population.sort(key=lambda p: p["score"])

    def randomBinaryList(self):
        """ Renvoie une liste de self.nb_bits chiffres binaires aléatoires """
        return [randint(0, 1) for _ in range(self.nb_bits)]

    def initPopulation(self):
        """ Initialisation de la population """
        print("%s - Initialisation de la population..." % dateNow())
        for k in range(self.population_size):
            print("%s - Individu %d/%d" %
                  (dateNow(), k + 1, self.population_size))
            bin_vector = [self.randomBinaryList() for _ in range(4)]
            vector = binVectorToFloat(bin_vector)
            score = self.fitness(vector)
            self.population.append({"bin_vector": bin_vector,
                                    "vector": vector,
                                    "score": score})
        self.sortPopulationDescending()

    def scoreOnOneGame(self, vector):
        """ Score sur une partie """
        player = AgentEvaluation(
            eval_coeffs=vector, silent=True)
        player.engine.max_blocks = self.max_nb_blocks
        player.engine.run()
        return player.engine.total_lines

    def fitness(self, vector):
        """ Fitness de l'individu : score total sur nb_games_played parties """
        score = 0
        for i in range(self.nb_games_played):
            score += self.scoreOnOneGame(vector)
        return score

    def updateScore(self, individu):
        """ Met à jour le score de l'individu """
        individu["score"] = self.fitness(individu["vector"])

    def updateBinaryIndivdu(self, individu):
        """ Met à jour les paramètres d'un individu à partir de son vecteur binaire """
        bin_vector = individu["bin_vector"]
        vector = binVectorToFloat(bin_vector)
        score = self.fitness(vector)
        individu["vector"] = vector
        individu["score"] = score

    def wheelSelection(self):
        """ Sélection d'un individu avec une roulette """
        self.sortPopulationAscending()
        score_total = sum([p["score"] for p in self.population])
        probas = [p["score"] / score_total for p in self.population]
        r = random()
        k = 0
        ptotal = probas[0]
        while ptotal < r:
            k += 1
            ptotal += probas[k]
        return self.population[k]

    def crossover(self, parent1, parent2):
        """ Renvoie les enfants de parent1 et parent2 """
        bin_vector1 = []
        bin_vector2 = []
        for k in range(4):
            crossover_point = randrange(0, self.nb_bits)
            bin_vector1.append(parent1["bin_vector"][k][:crossover_point] +
                               parent2["bin_vector"][k][crossover_point:])
            bin_vector2.append(parent2["bin_vector"][k][:crossover_point] +
                               parent1["bin_vector"][k][crossover_point:])
        child1 = {"bin_vector": bin_vector1}
        child2 = {"bin_vector": bin_vector2}
        return [child1, child2]

    def mutateBinVector(self, bin_vector):
        """ Mute un vecteur """
        for i in range(4):
            for k in range(self.nb_bits):
                if random() < self.proba_mutation:
                    bin_vector[i][k] = 1 - bin_vector[i][k]
        return bin_vector

    def generateNewOffspring(self):
        """ Renvoie la nouvelle génération """
        print("%s - Création des enfants... " % dateNow())
        new_offspring = []
#         nb_childs_to_create = int(
#             self.population_size * self.percentage_new_offspring)
        nb_childs_to_create = ceil(
            self.population_size * (1 - self.elitism_percentage))
        # On crée un certain nombre d'enfants
        created_childs = 0
        while created_childs < nb_childs_to_create:
            print("%s - Génération %d - Enfants %d,%d/%d" %
                  (dateNow(), self.num_generation, created_childs + 1, created_childs + 2,
                   nb_childs_to_create))
            parent1 = self.wheelSelection()
            parent2 = self.wheelSelection()
            [child1, child2] = self.crossover(parent1, parent2)
            # On mute les enfants créés
            child1["bin_vector"] = self.mutateBinVector(child1["bin_vector"])
            child2["bin_vector"] = self.mutateBinVector(child2["bin_vector"])
            # Update des enfants créés
            self.updateBinaryIndivdu(child1)
            self.updateBinaryIndivdu(child2)
            # Ajout à la liste des enfants
            new_offspring += [child1, child2]
            created_childs += 2
        return new_offspring

    def keepOnlyElite(self):
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
        self.keepOnlyElite()
        new_offspring = self.generateNewOffspring()
        self.population += new_offspring
        self.deleteWorst()  # Au cas où on dépasse population_size

    def updateStats(self):
        """ Met à jours les statistiques """
        self.max_scores.append(self.population[0]["score"])
        self.average_scores.append(sum([self.population[k]["score"]
                                        for k in range(self.population_size)]) / self.population_size)

    def plotStats(self):
        """ Courbes de statistiques """
        plt.title("pop_size=%d - nb_games=%d - max_blocks=%d" %
                  (self.population_size, self.nb_games_played, self.max_nb_blocks))
        plt.plot(self.average_scores, label="Average scores")
        plt.plot(self.max_scores, label="Max scores")
        plt.legend()
        plt.xlabel("Génération")
        plt.ylabel("Score")
        plt.show()

    def process(self):
        """ Boucle principale de l'optimisation """
        print("Algorithme génétique de paramètres :")
        print("  - nb_generations = %d" % self.nb_generations)
        print("  - population_size = %d" % self.population_size)
        print("  - nb_games_played = %d" % self.nb_games_played)
        print("  - max_nb_blocks = %d" % self.max_nb_blocks)
        print("  - proba_mutation = %.2f" % self.proba_mutation)
        print("  - elitism_percentage = %.2f" %
              self.elitism_percentage)
        print()

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
    optimizer = OptimizerAlgoGen3()
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
