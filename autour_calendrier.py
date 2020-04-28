# auteur : Eric W 
# date : septembre 2018
# objet : TP sur les expressions booléennes et instructions conditionnelles
#         http://www.fil.univ-lille1.fr/~L1S1Info/Doc/New/TP3_fr.html


# Première Partie : Années bissextiles

def est_divisible_par(a, b):
    """
    :param a, b: (int) deux entiers
    :return: (bool)
       - True si a est divisible par b
       - False sinon
    :CU: b non nul
    :Exemples:
    
    >>> est_divisible_par(10, 2)
    True
    >>> est_divisible_par(10, 3)
    False
    """
    return a % b == 0


def est_bissextile(annee):
    """
    :param annee: (int) année à tester
    :return: (bool)
       - True si annee est une année bissextile
       - False sinon
    :CU: aucune (ou annee > 1582 année d'établissement du calendrier grégorien)
    :Exemples:
    
    >>> est_bissextile(2018)
    False
    >>> est_bissextile(2008)
    True
    >>> est_bissextile(1900)
    False
    >>> est_bissextile(2000)
    True
    """
    return ((est_divisible_par(annee, 4) and not est_divisible_par(annee, 100)) or
            (est_divisible_par(annee, 400)))

    
# Deuxième partie : Nombre de jours dans un mois

def nbre_jours(mois, annee):
    """
    :param mois, annee: (int) mois et annee
    :return: (int) nombre de jours dans le mois mois de l'année annee.
    :CU: mois valide
    :Exemples:
    
    >>> nbre_jours(1, 2019)
    31
    >>> nbre_jours(2, 2019)
    28
    >>> nbre_jours(2, 2016)
    29
    >>> nbre_jours(4, 2019)
    30
    """
    if ((mois == 1) or (mois == 3) or (mois == 5) or
        (mois == 7) or (mois == 8) or (mois == 10) or (mois == 12)):
        nbre = 31
    elif ((mois == 4) or (mois == 6) or (mois == 9) or (mois == 11)):
        nbre = 30
    elif est_bissextile(annee):
        nbre = 29
    else:
        nbre = 28
    return nbre
        

# Troisième partie : validité d'une date


def est_mois_valide(m):
    '''
    :param m: (int)
    :return: (bool)
       - True si m est le numéro d'un mois
       - False sinon
    :CU: aucune
    :Exemples:

    >>> est_mois_valide(3)
    True
    >>> est_mois_valide(13)
    False
    >>> est_mois_valide(0)
    False
    '''
    return 1 <= m and m <= 12

def est_jour_valide(j, m, a):
    '''
    :param j, m, a: (int) trois entiers
    :return: (bool)
    :CU: m doit être un numéro de mois valide
    :Exemples:

    >>> est_jour_valide(25, 9, 2019)
    True
    >>> est_jour_valide(31, 9, 2019)
    False
    >>> est_jour_valide(29, 2, 2019)
    False
    >>> est_jour_valide(29, 2, 2020)
    True
    '''
    return 1 <= j and j <= nbre_jours(m, a)

def est_date_valide(j, m, a):
    """
    :param j, m, a: (int) trois entiers
    :return: (bool)
       - True si le triplet (j,m,a) représente une date valide
       - False sinon
    :CU: a >= 1583
    :Exemples:
    
    >>> est_date_valide(4, -1, 2018)
    False
    >>> est_date_valide(4, 15, 2018)
    False
    >>> est_date_valide(32, 1, 2018)
    False
    >>> est_date_valide(29, 2, 2018)
    False
    >>> est_date_valide(29, 2, 2016)
    True
    """
    return est_mois_valide(m) and est_jour_valide(j, m, a)

def nom_mois(m):
    """
    :param m: (int) numéro d'un mois
    :return: (str) nom du mois
    :CU: 1 <= m <= 12

    >>> nom_mois(1)
    'janvier'
    >>> nom_mois(10)
    'octobre'
    """
    return ('janvier', 'février', 'mars', 'avril',
            'mai', 'juin', 'juillet', 'août',
            'septembre', 'octobre', 'novembre', 'décembre')[m - 1]

def num_jour(jour, mois, annee):
    """
    :param jour: le quantième d
    :type jour: int
    :param mois: le numéro du mois
    :type mois: int
    :param annee: l'année
    :type annee: int
    :return: le numéro du jour 
    :rtype: int
    :CU: le triplet (jour, mois, annee) doit être une date valide
    :algo: cf https://fr.wikipedia.org/wiki/D%C3%A9termination_du_jour_de_la_semaine
    :Exemples:
    
    >>> num_jour(1, 1, 2018)
    1
    >>> num_jour(1, 1, 2100)
    5
    """
    ab, cd = divmod(annee, 100)
    k = cd // 4
    q = ab // 4
    Q = jour
    if est_bissextile(annee):
        TABLE = (3, 6, 0, 3, 5, 1, 3, 6, 2, 4, 0, 2)
    else:
        TABLE = (4, 0, 0, 3, 5, 1, 3, 6, 2, 4, 0, 2)
    M = TABLE[mois - 1]
    return (k + q + cd + M + Q + 2 + 5*ab) % 7


def nom_jour(jour, mois, annee):
    """
    :param jour, mois, annee: (int) une date
    :return: (str) nom du jour correspondant à cette date
    :CU: jour, mois, annee doit représenter une date valide
    """
    return ('dimanche', 'lundi', 'mardi', 'mercredi',
            'jeudi', 'vendredi', 'samedi')[num_jour(jour, mois, annee)]

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)

    
