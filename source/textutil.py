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

import re
from time import *

# Contantes de couleurs en mode 256 couleurs VTE
CRED = 196
CCYAN = 50
CPURPLE = 165
CGREEN = 82
CBLUE = 27
CORANGE = 202
CYELLOW = 226
CWHITE = 15
CBLACK = 232
CGRAY = 237


def textColor(string, bg=CWHITE, fg=CBLACK):
    """ Renvoie une chaîne contenant le texte coloré
        avec bg pour la couleur de fond
        et fg pour la couleur du texte.
        Utilise les codes ANSI/VT100. """
    return "\033[48;5;%dm\033[38;5;%dm%s\033[0m" % (bg, fg, string)


def mergeChains(string1, string2):
    """ Fusionne deux chaînes cote à cote pour l'affichage """
    lines1 = string1.split('\n')
    lines2 = string2.split('\n')
    result = ""
    # Utilisation d'une expression rrégulière pour supprimer
    # les caractères spéciaux de couleurs
    max_length_string1 = max([len(re.sub(r"\033.+?m", "", s)) for s in lines1])
    min_height = min(len(lines1), len(lines2))

    for k in range(min_height):
        result += lines1[k] + '  ' + ' ' * \
            (max_length_string1 - len(lines1[k])) + lines2[k] + '\n'

    if min_height == len(lines2):
        for k in range(min_height, len(lines1)):
            result += lines1[k] + "\n"
    else:
        for k in range(min_height, len(lines2)):
            result += " " * max_length_string1 + "  " + lines2[k] + "\n"
    return result


def center(string, length):
    """Centre la chaîne string sur la longueur"""
    c = len(string)
    l = length
    return ' ' * ((l - c) // 2) + string + ' ' * ((l - c) // 2 + (l - c) % 2) + '\n'


def boxed(text, prefix='', window_width=0, window_height=0):
    """Affiche chaque ligne de texte précédée d'un préfixe
    dans une boîte de largeur window_width"""
    lines = text.split('\n')
    if window_width == 0:
        window_width = max([len(l) for l in lines]) + 2
    if window_height == 0:
        window_height = len(lines)
    chain = ""
    chain += '╔' + '═' * window_width + '╗' + '\n'
    for ligne in lines:
        chain += "║ %s%s" % (prefix, ligne) + ' ' * \
            (window_width - (len(ligne) + len(prefix) + 1)) + '║' + '\n'
    for _ in range(window_height - len(lines)):
        chain += "║ " + ' ' * \
            (window_width + len(prefix) - 1) + '║' + '\n'
    chain += '╚' + '═' * window_width + '╝ '
    return chain


def dateNow():
    return strftime("%d/%m/%y - %H:%M:%S", localtime())


if __name__ == "__main__":
    print(textColor("TEST", CGREEN))
    input()

    text1 = """1++++++++++++++
2++++++
3+++++++++++++
4+++++++++
"""
    text2 = """1------------------
2------------
3-------------
4-----
5-----
6-----"""
    print(mergeChains(text1, text2))

    text1 = """1++++++++++++++
2++++++++++++++
3+++++++++++++
4++++++++++++
"""
    text2 = """1------------------
2------------
3-------------"""
    print(mergeChains(text1, text2))
