#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'FIL - Faculté des Sciences et Technologies -  Univ. Lille <http://portail.fil.univ-lille1.fr>_'
__date_creation__ = 'Sun Apr 12 16:58:23 2020'
__doc__ = """
:mod:`calendrier_pataphysique` module
:author: {:s} 
:creation date: {:s}
:last revision:

Conversions calendrier Ère Pataphysique <-> Calendrier vulgaire

""".format(__author__, __date_creation__)

import autour_calendrier as calendrier_vulgaire


class Date_vulgError(Exception):
    def __init__(self, msg):
        self.message = msg
        
class Date_vulg(object):
    def __init__(self, j, m ,a):
        if not calendrier_vulgaire.est_date_valide(j, m, a):
            raise Date_vulgError('données non valides : {:d} {:d} {:d}'.format(j, m, a))
        else:
            self.jour = j
            self.mois = m
            self.annee = a

    def demain(self):
        if self.jour < calendrier_vulgaire.nbre_jours(self.mois, self.annee):
            return Date_vulg(self.jour + 1, self.mois, self.annee)
        elif self.mois < 12:
            return Date_vulg(1, self.mois + 1, self.annee)
        else:
            return Date_vulg(1, 1, self.annee + 1)

    def hier(self):
        if self.jour > 1:
            return Date_vulg(self.jour - 1, self.mois, self.annee)
        elif self.mois != 1:
            mois = self.mois - 1
            return Date_vulg(calendrier_vulgaire.nbre_jours(mois, self.annee),
                             mois,
                             self.annee)
        else:
            return Date_vulg(31, 12, self.annee - 1)
        
    def __str__(self):
        return '{:s} {:d} {:s} {:d} (vulg)'.format(calendrier_vulgaire.nom_jour(self.jour,
                                                                                self.mois,
                                                                                self.annee),
                                                   self.jour,
                                                   calendrier_vulgaire.nom_mois(self.mois),
                                                   self.annee)


with open('calendrier_pataphysique.csv', 'rt') as entree:
    TOUT = entree.readlines()
    
CAL_PAT = dict()
CONVERSIONS = dict()
num_mois = 0
for i in range(2, len(TOUT)):
    data = TOUT[i].rstrip().split(';')
    if num_mois in CAL_PAT and data[0] == CAL_PAT[num_mois]['nom']:
        CAL_PAT[num_mois]['jours'].append(data[3])
    else:
        num_mois += 1
        CAL_PAT[num_mois] = {'nom' : data[0], 'jours' : [data[3]]}
    jm_EP = (int(data[1]), num_mois)
    cle_EP = jm_EP + ('EP',)
    if data[5] != '':
        jm_VULG = tuple(int(n) for n in data[5].split(' '))
        CONVERSIONS[cle_EP] = [jm_VULG]
        cle_VULG = jm_VULG + ('VULG',)
        if cle_VULG in CONVERSIONS:
            CONVERSIONS[cle_VULG].append(jm_EP)
        else:
            CONVERSIONS[cle_VULG] = [jm_EP]
        if data[6] != '':
            jm_VULG = tuple(int(n) for n in data[6].split(' '))
            cle_VULG = jm_VULG + ('VULG',)
            CONVERSIONS[cle_EP].append(jm_VULG)
            CONVERSIONS[cle_VULG] = [jm_EP]
    else:
        jm_VULG = tuple(int(n) for n in data[6].split(' '))
        CONVERSIONS[cle_EP] = [jm_VULG]
        CONVERSIONS[jm_VULG + ('VULG',)] = [jm_EP] 
        
def est_bissextile(a):
    return calendrier_vulgaire.est_bissextile(1873 + a)

def nbre_jours(m, a):
    if m == 11 or (m == 6 and est_bissextile(a)):
        return 29
    else:
        return 28

def est_date_valide(j, m, a):
    return (1 <= m <= 13 and
            1 <= j <= nbre_jours(m, a))

def nom_jour(j):
    '''
    :param j: (int) 
    :return: (str) nom du jour j dans le calendrier Pataphysique
    '''
    if j == 29:
        return 'hunyadi'
    else:
        return ('dimanche', 'lundi', 'mardi', 'mercredi',
                'jeudi', 'vendredi', 'samedi')[(j - 1) % 7]

def nom_mois(m):
    '''
    :param m: (int) 
    :return: (str) nom du jour m dans le calendrier Pataphysique
    '''
    return CAL_PAT[m]['nom']

    
class DateEPError(Exception):
    def __init__(self, msg):
        self.message = msg
        
class DateEP(object):
    def __init__(self, j, m ,a):
        if not est_date_valide(j, m, a):
            raise DateEPError('données non valides : {:d} {:d} {:d}'.format(j, m, a))
        else:
            self.jour = j
            self.mois = m
            self.annee = a

    def fete(self):
        return CAL_PAT[self.mois]['jours'][self.jour - 1]

    def demain(self):
        if self.jour < nbre_jours(self.mois, self.annee):
            return DateEP(self.jour + 1, self.mois, self.annee)
        elif self.mois < 13:
            return DateEP(1, self.mois + 1, self.annee)
        else: 
            return DateEP(1, 1, self.annee + 1)
                
    def hier(self):
        if self.jour > 1:
            return DateEP(self.jour - 1, self.mois, self.annee)
        elif self.mois != 1:
            mois = self.mois - 1
            return DateEP(nbre_jours(mois, self.annee), mois, self.annee)
        else:
            return DateEP(28, 13, self.annee - 1)
        
    def __str__(self):
        return '{:s} {:d} {:s} {:d} (EP)'.format(nom_jour(self.jour),
                                                   self.jour,
                                                   nom_mois(self.mois).capitalize(),
                                                   self.annee)

def date_vulgaire_en_EP(date):
    '''
    :param date: (Date_vulg) une date vulgaire à convertir
    :return: (DateEP) date du calendrier Pataphysique correspondante
    :CU: date postérieure au 8 sept 1873 (vulg) ou 1 absolu 1 (EP)
    
    >>> print(date_vulgaire_en_EP(Date_vulg(1, 9, 1873)))
    dimanche 1 ABSOLU 1 (EP)
    '''
    cleVULG = (date.jour, date.mois, 'VULG')
    if len(CONVERSIONS[cleVULG]) == 1 or calendrier_vulgaire.est_bissextile(date.annee):
        j_EP, m_EP = CONVERSIONS[cleVULG][0]
    else:
        j_EP, m_EP = CONVERSIONS[cleVULG][1]
    if date.mois >= 10 or (date.mois == 9 and date.jour >= 8):
        a_EP = date.annee - 1872
    else:
        a_EP = date.annee - 1873
    return DateEP(j_EP, m_EP, a_EP)

def date_EP_en_vulgaire(date):
    '''
    :param date: (DateEP) une date EP à convertir
    :return: (Date_vulg) date du calendrier vulgaire correspondante
    :CU: date postérieure au 1 ABSOLU 1 (EP) ou 8 sept 1 (vulg)
    
    >>> print(date_EP_en_vulgaire(DateEP(1, 1, 1)))
    lundi 8 septembre 1873 (vulg)
    '''
    cleEP = (date.jour, date.mois, 'EP')
    if len(CONVERSIONS[cleEP]) == 1 or not est_bissextile(date.annee):
        j, m = CONVERSIONS[cleEP][0]
    else:
        j, m = CONVERSIONS[cleEP][1]
    if m > 10 or (m == 9 and j >= 8):
        a = date.annee + 1872
    else:
        a = date.annee + 1873
    return Date_vulg(j, m, a)

def usage():
    print('Conversions date calendrier Pataphysique <-> calendrier vulgaire')
    print('Usage : {:s} [<opt> <date>]'.format(sys.argv[0]))
    print('où <opt> =')
    print('\t--vulg <date> : convertit la date vulgaire en date Pataphysique.')
    print('\t--EP   <date> : convertit la date Pataphysique en date vulgaire.')
    print('Les dates doivent être fournies au format j/m/a, j, m et a étant trois nombres.')
    print('Sans option : donne la date du jour en calendrier vulgaire et Pataphysique.')
    exit(1)
    
if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        import time
        aujourdhui = time.localtime()
        aujourdhui_vulg = Date_vulg(aujourdhui.tm_mday, aujourdhui.tm_mon, aujourdhui.tm_year)
        aujourdhui_EP = date_vulgaire_en_EP(aujourdhui_vulg)
        print('{:s} = {:s}'.format(str(aujourdhui_vulg), str(aujourdhui_EP)))
    elif sys.argv[1] in ('--vulg', '--EP'):
        try:
            date = tuple(int(elt) for elt in sys.argv[2].split('/'))
            assert len(date) == 3
        except IndexError:
            print('date manquante !')
            usage()
        except ValueError:
            print('date au format numérique j/m/a')
            usage()
        except AssertionError:
            print('date invalide')
            usage()
        if sys.argv[1] == '--vulg':
            try:
                print(date_vulgaire_en_EP(Date_vulg(*date)))
            except Date_vulgError:
                print('Date vulgaire invalide !')
                usage()
        else:
            try:
                print(date_EP_en_vulgaire(DateEP(*date)))
            except DateEPError:
                print('Date Pataphysique invalide')
                usage()
    else:
        usage()

    exit(0)
