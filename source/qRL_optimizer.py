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

from tetris_RLenv import *
from time import *
from random import *
from math import *


def argmax(liste):
    """ Renvoie l'indice de la valeur max de liste
        ou un indice aléatoire si la liste ne contient que de 0 """
    if sum(liste) != 0:
        return liste.index(max(liste))
    else:
        return randrange(0, len(liste))


class QRLOptimizer:
    """ Optimisatio par Q-learning sur une configuration simple """

    def __init__(self, width=5, height=5, base_blocks_bag=DOMINO_BLOCK_BAG,
                 alpha=0.1, gamma=0.9,
                 epsilon_min=0.01, epsilon_max=1, epsilon_delta=0.001,
                 max_episodes=2000, max_blocks=500):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon_max
        self.epsilon = self.epsilon_max
        self.epsilon_delta = epsilon_delta
        self.max_episodes = max_episodes
        self.max_blocks = max_blocks

        self.q = {}

        self.env = TetrisEnv(
            width=width, height=height, base_blocks_bag=base_blocks_bag, max_blocks=self.max_blocks)

    def reinit(self):
        """ Réinitialise l'environnement """
        self.env.reset()
        self.epsilon = self.epsilon_max

    def initQValue(self, s):
        """ Initialise la Q-value de l'état s avec de 0 """
        if s not in self.q:
            self.q[s] = [0] * self.env.nb_actions

    def update(self, s, a):
        """ Met à jour la Q-table de l'état s sur une action a """
        self.env.step(self.env.action_space[a])
        s1 = self.env.getStateCode()
        r = self.env.reward
        if s not in self.q:
            self.initQValue(s)
        if s1 not in self.q:
            self.initQValue(s1)

        self.q[s][a] = (1 - self.alpha) * self.q[s][a] + \
            self.alpha * (r +
                          self.gamma * max(self.q[s1]))

    def learn(self):
        """ Lance l'apprentissage """
        print("%s - Lancement de l'apprentissage" % dateNow())
        for k in range(self.max_episodes):
            if k % (self.max_episodes // 10) == 0:
                print("%s - %d/%d" % (dateNow(), k, self.max_episodes))
            self.reinit()
            s = self.env.getStateCode()
            self.initQValue(s)
            while not self.env.done:
                g = uniform(0, 1)
                if g <= self.epsilon:
                    a = randrange(0, self.env.nb_actions)
                else:
                    #                     a = self.q[s].index(max(self.q[s]))
                    a = argmax(self.q[s])
                self.update(s, a)
                s = self.env.getStateCode()
                self.epsilon = self.epsilon_min + \
                    (self.epsilon_max - self.epsilon_min) * \
                    exp(-self.epsilon_delta * k)
#         for s in self.q:
#             print(s, self.q[s])
#         input()

    def play(self):
        """ Joue la partie avec la Q-table crée """
        self.reinit()
        self.env.max_blocks = 0
        s = self.env.getStateCode()
        while not self.env.done:
            self.env.render()
            sleep(0.1)
            if s in self.q:
                a = argmax(self.q[s])
            else:
                a = randrange(0, self.env.nb_actions)

            self.env.step(self.env.action_space[a])
            s = self.env.getStateCode()


if __name__ == "__main__":
    optimizer = QRLOptimizer()
    optimizer.learn()
    input("Press enter to see the agent in action ")
    while True:
        optimizer.play()
        input("Press enter to continue")
    input("End")
