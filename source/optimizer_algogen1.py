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
from math import sqrt


class Individual:
    def __init__(self, nb_genes=16):
        self.nb_genes = nb_genes
        self.genom = [0] * 4
        for k in range(4):
            self.genom[k] = [randint(0, 1) for _ in range(self.nb_genes)]
        self.score = 0

    def toValues(self):
        """ Renvoie la liste des coefficients correspondant à cet individu """
        self.values = [0] * 4
        for i in range(4):
            for k in range(self.nb_genes):
                self.values[i] = (self.values[i] + self.genom[i]
                                  [self.nb_genes - 1 - k]) / 2
        return self.values


class OptimizerAlgoGen:
    def __init__(self, nb_genes=16, population_size=10, proba_mutation=0.01,
                 max_nb_blocks=500, elitism_percentage=5, nb_generations=10):
        self.nb_genes = nb_genes
        self.population_size = population_size
        self.proba_mutation = proba_mutation
        self.max_nb_blocks = max_nb_blocks
        self.elitism_percentage = elitism_percentage
        self.nb_generations = nb_generations
        self.population = [Individual(nb_genes=self.nb_genes)
                           for _ in range(self.population_size)]
        self.population_scores = []

    def evaluate(self, individual, silent=True):
        """ Renvoie le fitness d'un individu """
        player = AgentEvaluation(
            eval_coeffs=individual.toValues(), temporisation=0, silent=silent)
        player.engine.max_blocks = self.max_nb_blocks
        score = player.engine.run()
        individual.score = score
#         individual.score = -player.engine.max_height_on_game
#         individual.score = -player.engine.max_sum_heights_on_game
#         individual.score = player.engine.total_lines
        return score

    def populationScores(self, population, silent=True):
        """ Renvoie la liste des scores d'une population """
        return [self.evaluate(
            population[k], silent=silent) for k in range(len(population))]

    def wheelSelection(self, population, scores):
        """ Sélection d'un individu par la méthode de la roulette """
        r = random()
        S = sum(scores)
        cumulative_scores = [
            sum(scores[:(k + 1)]) / S for k in range(len(population))]
        index = 0
        while (r >= cumulative_scores[index]):
            index = index + 1
        return population[index]

    def crossover(self, parent1, parent2):
        """ Croisement entre deux individus """
        child1 = Individual(self.nb_genes)
        child2 = Individual(self.nb_genes)
        for k in range(4):
            crossover_point = randrange(0, self.nb_genes)
            child1.genom[k] = parent1.genom[k][:crossover_point] + \
                parent2.genom[k][crossover_point:]
            child1.genom[k] = parent2.genom[k][:crossover_point] + \
                parent1.genom[k][crossover_point:]
        return [child1, child2]

    def elitism(self, population, scores):
        """ Renvoie les meilleurs individus """
        nb_conserves = int(self.elitism_percentage *
                           self.population_size / 100)
        sorted_scores = sorted(scores)
        return [population[scores.index(sorted_scores[k])]
                for k in range(self.population_size - nb_conserves, self.population_size)]

    def mutate(self, invdividual):
        """ Mute un individu """
        for i in range(4):
            for k in range(self.nb_genes):
                if random() < self.proba_mutation:
                    invdividual.genom[i][k] = 1 - invdividual.genom[i][k]
        return invdividual

    def makeNewGeneration(self):
        """ Crée une nouvelle génération """
        self.population_scores = self.populationScores(
            self.population, silent=True)
        new_population = [0] * self.population_size
        for k in range(self.population_size // 2):
            descendance = self.crossover(
                self.wheelSelection(self.population, self.population_scores),
                self.wheelSelection(self.population, self.population_scores))
            new_population[2 * k] = descendance[0]
            new_population[2 * k + 1] = descendance[1]
        new_population_scores = self.populationScores(new_population)
        all_generations_population = self.population + new_population
        all_generations_scores = self.population_scores + new_population_scores
        meilleurs = self.elitism(
            all_generations_population, all_generations_scores)
        L = len(self.population) - \
            int(self.elitism_percentage * len(all_generations_population) / 100)
        final_population = [0] * L
        for k in range(L):
            final_population[k] = self.mutate(self.wheelSelection(
                all_generations_population, all_generations_scores))
        final_population = final_population + meilleurs
        return final_population

    def bestCoeffs(self):
        """ Renvoie les coeffs du meilleur individu """
        self.population_scores = self.populationScores(self.population)
        bestIndex = self.population_scores.index(max(self.population_scores))
        return self.population[bestIndex].toValues()

    def process(self):
        """ Boucle principale de l'algo génétique """
        print("Start : " + strftime("%d/%m/%y - %H:%M:%S", localtime()))
        for k in range(1, self.nb_generations + 1):
            print(strftime("%d/%m/%y - %H:%M:%S", localtime()))
            print("Génération %d/%d" % (k, self.nb_generations))
            self.population = self.makeNewGeneration()
        print("\nEnd : " + strftime("%d/%m/%y - %H:%M:%S", localtime()))
        print("Calcul des coeffs du meilleur....")
        best_coeffs = self.bestCoeffs()
        print("Best coeffs : %s" % str(best_coeffs))
        return best_coeffs


if __name__ == "__main__":
    optimizer = OptimizerAlgoGen(
        population_size=50, nb_generations=50, max_nb_blocks=1000)
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
