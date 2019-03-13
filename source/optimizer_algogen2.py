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
from textutil import *
from random import *
from time import time
from math import sqrt
import matplotlib.pyplot as plt


class OptimzerAlgoGen2:
    def __init__(self, population_size=50, nb_generations=100, max_nb_blocks=500, nb_games_played=10,
                 proba_mutation=0.05, mutation_rate=0.2,
                 percentage_for_tournament=0.10, percentage_new_offspring=0.30):
        # Paramètres de l'algo génétique
        self.population_size = population_size
        self.nb_generations = nb_generations
        self.max_nb_blocks = max_nb_blocks
        self.nb_games_played = nb_games_played
        self.proba_mutation = proba_mutation
        self.mutation_rate = mutation_rate
        self.percentage_for_tournament = percentage_for_tournament
        self.percentage_new_offspring = percentage_new_offspring

        self.population = []

        # Pour les stats
        self.num_generation = 0
        self.max_scores = []
        self.average_scores = []

    def sortPopulationDescending(self):
        """ Trie la population par ordre décroissant de scores """
        self.population.sort(key=lambda p: p["score"], reverse=True)

    def normalize(self, vector):
        """ Normalise un vecteur """
        norm = sqrt(sum([v**2 for v in vector]))
        return [v / norm for v in vector]

    def initPopulation(self):
        """ Initialise la population """
        print("%s - Initialisation de la population..." % dateNow())
        for k in range(self.population_size):
            print("%s - Individu %d/%d" %
                  (dateNow(), k + 1, self.population_size))
            vector = self.normalize([random() for _ in range(4)])
            self.population.append({"vector": vector, "score": -1})
            self.updateScore(self.population[k])
        self.population.sort(key=lambda p: p["score"], reverse=True)

    def scoreOnOneGame(self, vector):
        """ Score sur une partie """
        player = AgentEvaluation(
            eval_coeffs=vector, silent=True)
        player.engine.max_blocks = self.max_nb_blocks
        player.engine.run()
        return player.engine.total_lines
#         return score

    def fitness(self, vector):
        """ Fitness de l'individu : score total sur nb_games_played parties """
        score = 0
        for i in range(self.nb_games_played):
            score += self.scoreOnOneGame(vector)
        return score

    def updateScore(self, individu):
        """ Met à jour le score de l'individu """
        individu["score"] = self.fitness(individu["vector"])

    def getPopulationScores(self):
        """ Calcule les scores de toute la population """
        for k in range(self.population_size):
            self.updateScore(self.population[k])

    def linearCombination(self, a1, vector1, a2, vector2):
        """ Renvoie la combinaison linéaire de deux vecteurs """
        return [a1 * vector1[k] + a2 * vector2[k] for k in range(4)]

    def crossover(self, i1, i2):
        """ Croise les individus i1 et i2 """
        return self.linearCombination(i1["score"], i1["vector"],
                                      i2["score"], i2["vector"])

    def mutateVector(self, vector):
        """ Mute un individu (son vecteur) """
        if random() < self.proba_mutation:
            delta = uniform(-self.mutation_rate, self.mutation_rate)
            i = randrange(4)
            vi = vector[i]
            if 0 <= vi + delta <= 1:
                vector[i] += delta
                vector = self.normalize(vector)
        return vector

    def generateNewOffspring(self):
        """ Renvoie la nouvelle génération """
        print("%s - Création des enfants... " % dateNow())
        new_offspring = []
        nb_childs_to_create = int(
            self.population_size * self.percentage_new_offspring)
        # On crée un ecratin nombre d'enfants
        created_childs = 0
        while created_childs < nb_childs_to_create:
            print("%s - Génération %d - Enfant %d/%d" %
                  (dateNow(), self.num_generation, created_childs + 1, nb_childs_to_create))
            # On sélectionne au hasard un pourcentage de la population
            candidates = []
            for k in range(int(self.population_size * self.percentage_for_tournament)):
                candidates.append(choice(self.population))
            candidates.sort(key=lambda p: p["score"], reverse=True)
            # On croise les deux meilleurs qu'on ajoute dans la nouvelle
            # génération
            offspring_vector = self.normalize(
                self.crossover(candidates[0], candidates[1]))
            # On mute l'enfant créé
            offspring_vector = self.mutateVector(offspring_vector)
            # Calcul de son score
            offspring_score = self.fitness(offspring_vector)
            # Ajout à la liste des enfants
            new_offspring.append({"vector": offspring_vector,
                                  "score": offspring_score})
            created_childs += 1
        return new_offspring

    def deleteWorst(self):
        """ Enlève les moins bons éléments de la population """
        self.sortPopulationDescending()
        self.population = self.population[:self.population_size]

    def makeNewGeneration(self):
        """ Crée une nouvelle génération """
        self.num_generation += 1
        new_offspring = self.generateNewOffspring()
        self.population += new_offspring
        self.deleteWorst()

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
        print("  - mutation_rate = %.2f" % self.mutation_rate)
        print("  - percentage_for_tournament = %.2f" %
              self.percentage_for_tournament)
        print("  - percentage_new_offspring = %.2f" %
              self.percentage_new_offspring)
        print()

        self.initPopulation()
        self.updateStats()
        for k in range(self.nb_generations):
            print("Best : %s - Score : %d" % (str(self.population[0]["vector"]),
                                              self.population[0]["score"]))
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
    optimizer = OptimzerAlgoGen2()
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
