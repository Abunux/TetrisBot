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


def mergeChains(string1, string2):
    """ Fusionne deux chaînes cote à cote pour l'affichage """
    lines1 = string1.split('\n')
    lines2 = string2.split('\n')
    result = ""
    max_length_string1 = max([len(s) for s in lines1])
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
    """Centre la string sur la longueur"""
    c = len(string)
    l = length
    return ' ' * ((l - c) // 2) + string + ' ' * ((l - c) // 2 + (l - c) % 2) + '\n'


def boxed(text, prefix='', window_width=0, window_height=0):
    """Affiche chaque ligne de text précédée d'un préfixe
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


if __name__ == "__main__":
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
