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
#    Analyse statistique avec création d'un
#    histogramme et d'un diagramme en boîte
#
#    Code récupéré et adapté d'un de mes anciens
#    projets : https://github.com/Abunux/pyBatNav
#
#-----------------------------------------------------

from math import *

try:
    import numpy as np
    import matplotlib.pyplot as plt
except:
    print("""
------------------------------------------------------------------
Attention, vous devez installer les librairies numpy et matplotlib
Sinon vous ne pourrez pas avoir les figures statistiques.
------------------------------------------------------------------
""")


class Stats:
    """ Représentation statistique des parties """

    def __init__(self, data=None, filename="", mean_time=0, nb_bars=10, title=""):
        if data:
            self.data = data
        elif filename:
            self.filename = filename
            self.loadData()
        else:
            return

        self.data.sort()
        self.nb_bars = nb_bars
        self.title = title

        self.getAllStats()

        if filename:
            self.filename = filename
        else:
            self.filename = "%s_n=%d" % (self.title, self.effectif)

        self.mean_time = mean_time

    #=========================================================================
    # Chargement et sauvegarde des données (pour analyse future)--------
    #=========================================================================
    def loadData(self):
        """Charge les données à partir d'un fichier texte"""
        self.data = []
        with open(self.filename + ".txt", "r") as datafile:
            for v in datafile:
                self.data.append(int(v))

    def saveData(self):
        """Sauvegarde les données dans un fichier texte"""
        with open(self.filename + ".txt", "w") as datafile:
            for k in range(len(self.data)):
                datafile.write(str(self.data[k]) + '\n')

        # Sauvegarde dans un tableau en LaTeX :
        with open(self.filename + ".tex", "w") as datafile:
            for k in range(len(self.data)):
                datafile.write(str(k) + " & " +
                               str(self.data[k]) + r'\\' + '\n')
                datafile.write(r"\hline" + '\n')

    #==========================================================================
    # Récupération des paramètres statistiques basiques ----------------
    #==========================================================================
    def getAllStats(self):
        """Récupère tous les indicateurs statistiques"""
        self.getEffectif()
        self.getMini()
        self.getMaxi()
        self.getQuartiles()
        self.getMean()
        self.getSigma()

    def getEffectif(self):
        """ Renvoie le nombre de données """
        self.effectif = len(self.data)

    def getMini(self):
        """ Renvoie le minimum des données """
        self.min = min(self.data)

    def getMaxi(self):
        """ Renvoie le maximum des données """
        self.max = max(self.data)

    def getQuartiles(self):
        """ Renvoie un tuple (Q1, Médiane, Q3) """
        # À revoir
        self.quartiles = (
            self.data[min(self.effectif - 1, ceil(self.effectif / 4))],
            self.data[min(self.effectif - 1, ceil(self.effectif / 2))],
            self.data[min(self.effectif - 1, ceil(3 * self.effectif / 4))]
        )

    def getMean(self):
        """ Renvoie la moyenne des données """
        self.mean = sum(self.data) / self.effectif

    def getSigma(self):
        """ Renvoie l'écart-type des données """
        self.sigma = sqrt(sum(
            [((self.data[k] - self.mean)**2) / self.effectif for k in range(self.effectif)]))

    #=========================================================================
    # Histogramme
    #=========================================================================
    def histogram(self, save=True):
        """ Crée et affiche l'histogramme """
        # Récupération des indicateurs statistiques
        n = self.effectif
        mini = self.min
        maxi = self.max
        q1 = self.quartiles[0]
        mediane = self.quartiles[1]
        q3 = self.quartiles[2]
        moyenne = self.mean
        sigma = self.sigma
        tmoy = self.mean_time

        try:
            fig = plt.figure()
        except:
            print("""
Création de la figure statistique impossible
(numpy et matplotlib manquants)
""")
            return

        # Histogramme
        plt.rcParams["patch.force_edgecolor"] = True
        plt.hist(self.data, self.nb_bars, density=True,
                 facecolor='g', alpha=0.75)

        # Création du diagramme en boite
        # Dimensions de la grille et des objets graphiques
        plt.ylim(ymin=0)
        gymin, gymax = plt.ylim()
        gxmin, gxmax = plt.xlim()
        yboite = (gymin + gymax) / 2        # Position verticale de la boite
        hboite = (gymax - gymin) / 10       # Hauteur de la boite
        # Hauteur des taquets en xmin et xmax
        hbornes = (gymax - gymin) / 30
        # Q1, Med et Q3
        plt.hlines(yboite - hboite, q1, q3, linewidths=2)
        plt.hlines(yboite + hboite, q1, q3, linewidths=2)
        plt.vlines(q1, yboite - hboite, yboite + hboite, linewidths=2)
        plt.vlines(mediane, yboite - hboite, yboite + hboite, linewidths=2)
        plt.vlines(q3, yboite - hboite, yboite + hboite, linewidths=2)
        plt.text(q1, yboite, r"$%d$" % q1, horizontalalignment='center',
                 verticalalignment='center', bbox={'facecolor': 'white', 'alpha': 1, 'pad': 2})
        plt.text(mediane, yboite, r"$%d$" % mediane, horizontalalignment='center',
                 verticalalignment='center', bbox={'facecolor': 'white', 'alpha': 1, 'pad': 2})
        plt.text(q3, yboite, r"$%d$" % q3, horizontalalignment='center',
                 verticalalignment='center', bbox={'facecolor': 'white', 'alpha': 1, 'pad': 2})
        # Xmin et Xmax
        plt.hlines(yboite, mini, q1, linewidths=2)
        plt.hlines(yboite, q3, maxi, linewidths=2)
        plt.vlines(mini, yboite - hbornes, yboite + hbornes, linewidths=2)
        plt.vlines(maxi, yboite - hbornes, yboite + hbornes, linewidths=2)
        plt.text(mini, yboite, r"$%d$" % mini, horizontalalignment='center',
                 verticalalignment='center', bbox={'facecolor': 'white', 'alpha': 1, 'pad': 2})
        plt.text(maxi, yboite, r"$%d$" % maxi, horizontalalignment='center',
                 verticalalignment='center', bbox={'facecolor': 'white', 'alpha': 1, 'pad': 2})
        # Texte de résumé statistique
        plt.text(gxmin + (gxmax - gxmin) * 0.05, gymin + (gymax - gymin) * 0.95,
                 r"$\bar x=%.2f$" % moyenne + '\n' + "$\sigma=%.2f$" % sigma,
                 horizontalalignment='left', verticalalignment='top', fontsize=15,
                 bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 15})
        # Mise en forme et affichage du graphique
        plt.xlabel("Score")
        plt.ylabel("Fréquence de parties")
        plt.title(self.title)
        if save:
            plt.savefig(self.filename + ".png", dpi=fig.dpi)
        plt.show()


if __name__ == "__main__":
    stats = Stats(data=[1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5,
                        5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 10])
    print(stats.effectif)
    print(stats.min)
    print(stats.max)
    print(stats.quartiles)
    print(stats.mean)
    print(stats.sigma)
    stats.histogram()
#     from agent_filtering import *
#     s = benchAgent(AgentFiltering, 10)
#     stats = Stats(data=s["scores"], mean_time=s["mean_time"])
#     stats.histogram()
