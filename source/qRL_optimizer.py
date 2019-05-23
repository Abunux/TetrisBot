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
#    Classe QRLOptimizer
#
#    Optimisation par simple Q-learning
#
#-----------------------------------------------------

from tetris_RLenv import *
from time import *
from random import *
from math import *
import sys
from itertools import chain


def argmax(liste):
    """ Renvoie l'indice de la valeur max de liste
        ou un indice aléatoire si la liste ne contient que des 0 """
    if sum(liste) != 0:
        return liste.index(max(liste))
    else:
        return randrange(0, len(liste))


def total_size(o):
    """ Renvoie la taille totale d'un objet en mémoire
    Code récupéré sur : https://code.activestate.com/recipes/577504/ 
    et adapté au projet """
    def dict_handler(d): return chain.from_iterable(d.items())
    all_handlers = {list: iter,
                    dict: dict_handler}
    seen = set()                      # track which object id's have already been seen
    # estimate sizeof object without __sizeof__
    default_size = sys.getsizeof(0)

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = sys.getsizeof(o, default_size)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


class QRLOptimizer:
    """ Optimisation par Q-learning sur une configuration simple """

    def __init__(self, width=5, height=5, base_blocks_bag=DOMINO_BLOCK_BAG,
                 max_episodes=2000, max_blocks=500,
                 alpha=0.1, gamma=0.9,
                 epsilon_min=0.01, epsilon_max=1, epsilon_delta=0.001):
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
            width=width, height=height, base_blocks_bag=base_blocks_bag, max_blocks=self.max_blocks,
            agent_name="Q-Learning")

    def reinit(self):
        """ Réinitialise l'environnement """
        self.env.reset()
        self.epsilon = self.epsilon_max

    def initQValue(self, s):
        """ Initialise la Q-value de l'état s avec des 0 si s n'est pas encore dans la table """
        if s not in self.q:
            self.q[s] = [0] * self.env.nb_actions

    def update(self, s, a):
        """ Met à jour la Q-table de l'état s sur une action a """
        self.env.step(self.env.action_space[a])
        s1 = self.env.getStateCode()
        r = self.env.reward
        self.initQValue(s)
        self.initQValue(s1)

        # Équation de Bellman
        self.q[s][a] = (1 - self.alpha) * self.q[s][a] + \
            self.alpha * (r +
                          self.gamma * max(self.q[s1]))

    def learn(self):
        """ Lance l'apprentissage """
        start = time()
        print("%s - Lancement de l'apprentissage" % dateNow())
        for k in range(self.max_episodes):
            if k % (self.max_episodes // 100) == 0:
                print("%s - %d/%d (epsilon=%.3f)" %
                      (dateNow(), k, self.max_episodes, self.epsilon))
            # Initialisation de l'environnement
            self.reinit()
            s = self.env.getStateCode()
            self.initQValue(s)

            while not self.env.done:
                # Exploration vs exploitation
                g = uniform(0, 1)
                if g <= self.epsilon:
                    a = randrange(0, self.env.nb_actions)
                else:
                    a = argmax(self.q[s])

                # MAJ de la Q-Table
                self.update(s, a)
                s = self.env.getStateCode()

                # MAJ de epsilon
                self.epsilon = self.epsilon_min + \
                    (self.epsilon_max - self.epsilon_min) * \
                    exp(-self.epsilon_delta * k)

        print("%s - Fin de l'apprentissage" % dateNow())
        print("Temps total : %.2f secondes" % (time() - start))
        print("Taille de la q-table : %d octets" % total_size(self.q))

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
    try:
        optimizer.learn()
    except:
        print("Error !")
    input("Press enter to see the agent in action...")
    while True:
        optimizer.play()
        input("Press enter to continue")
    input("End")
