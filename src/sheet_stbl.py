# -*- coding: utf-8 -*-

import os
import logging
import ddd_utils
from pathlib import Path

import ddd_utils

# create logger
module_logger = logging.getLogger('ddd_check')


class StblDonneeInstance:
    ''' Instance de la donnee dans une STBL
        - stbl : stbl d'origine
        - io : input ou outpout
        - valeur : valeur dans la STBL
    '''


    def __init__(self, stbl, io, valeur):
        self.stbl   = stbl
        self.io     = io
        if(valeur == True):
            self.valeur = "TRUE"
        elif(valeur == False):
            self.valeur = "FALSE"
        else:
            self.valeur = valeur


    def __str__(self):
        return "instance::stbl={}::io={}::valeur={}".format(
                self.stbl, self.io, self.valeur)

    def LireInstance(self):
        return (str(self.stbl) + ' ' + str(self.io) + ' ' + str(self.valeur))

    def Afficher(self):
        print(str(self.stbl) + ' ' + str(self.io) + ' ' + str(self.valeur))


class StblDonnee:
    ''' Donnee unique dans l'extract STBL
        - nom : nom de la donnee
        - liste_instances : liste d'objets de type StblDonneeInstance
        - nb_instances : nombre d'instances pour 1 donnee
    '''

    def __init__(self, nom):
        self.nom             = nom
        self.liste_instances = []
        self.nb_instances    = 0

    def __str__(self):
        return "StblDonnee::nom={}::nb_instances={}".format(
                self.nom, self.nb_instances)

    def Ajouter(self, stbl, io, valeur):
        a = StblDonneeInstance(stbl, io, valeur)
        if(self._VerifierPresenceInstance(a) == False):
            self.liste_instances.append(a)
            self.nb_instances += 1

    '''
        Verifier si l'instance existe deja
    '''
    def _VerifierPresenceInstance(self, instance):
        flag = False
        for elt in self.liste_instances:
            if(elt.io == instance.io):
                if(elt.valeur == instance.valeur):
                    flag = True
                    break
        return flag

    '''
        Retourne tous les etats possibles d'une donnee
    '''
    def ListerEtats(self):
        liste_etats = []
        for elt in self.liste_instances:
            liste_etats.append(elt.valeur)

        return (liste_etats)


    def Afficher(self):
        print("DonneeStbl-->Affiche")
        print('Nom = ' + self.nom)
        print('Nb instances = ' + str(self.nb_instances))
        for elt in self.liste_instances:
            print('Instances = ' + elt.LireInstance())



class Stbl:
    ''' Objet image d'une STBL :
        - nom_stbl : nom de la STBL
        - liste_donnees : liste d'objets de classe StblDonnee
        - nb_donnees : nombre de donnees pour 1 STBL'''

    def __init__(self, nom):
        self.nom           = nom # nom de la STBL
        self.liste_donnees = [] # Liste de classes de type StblDonnee
        self.nb_donnees    = 0 # nombre de donnees pour une STBL


    def __str__(self):
        return "Stbl::nom={}::nb_donnees={}::liste={}".format(
                self.nom, self.nb_donnees, (map(str, self.liste_donnees)))

    ''' Nettoie la liste des donnees de StblDonnee pour une STBL donnee
    '''
    def ChargerDonnee(self, liste_donnee_stbl):
        # copie de toutes les donnees STBL
        self.liste_donnees = list(liste_donnee_stbl)

        module_logger.debug('ChargerDonnee STBL = ' + self.nom + ' Taille Liste = ' + str(len(self.liste_donnees)))

        # Nettoyage pour chaque donnee n'ayant pas de rapport avec la stbl (attribut self.nom)
        for i, stbl_data in enumerate(self.liste_donnees):

            module_logger.debug('stbl_data = ' + str(stbl_data))

            # print('stbl_data = ' + str(stbl_data))
            # print('i= ' + str(i))
            flag_trouve_stbl = False
            # pour chaque instance
            for j, stbl_instance in enumerate(stbl_data.liste_instances):
                module_logger.debug('stbl_instance = ' + str(stbl_instance))
                if(stbl_instance.stbl == self.nom):
                    flag_trouve_stbl = True
                    # print('trouve instance stbl =' + stbl_instance.stbl + ' indice =' + str(j))
                else:
                    del self.liste_donnees[i].liste_instances[j]
                    # print('del instance =' + str(j))
            if(flag_trouve_stbl == False):
                # print('del donnee nom =' + self.liste_donnees[i].nom)
                del self.liste_donnees[i]



        self.nb_donnees = len(self.liste_donnees)
        for i, stbl_data in enumerate(self.liste_donnees):
            self.liste_donnees[i].nb_instances = len(self.liste_donnees[i].liste_instances)


    def Afficher(self):
        module_logger.debug('STBL:nom = ' + self.nom)
        for donnee in self.liste_donnees:
            for instance in donnee.liste_instances:
                str_print = "STBL:nom=::Donnee={}::Instance={}::io={}::valeur={}".format(
                self.nom, donnee.nom, instance.io, instance.valeur)
                module_logger.debug(str_print)


class StblExctract:
    ''' Image de l'onglet STBL:
        - liste_donnees_stbl : liste classes StblDonnee
        - liste_stbl : liste vue STBL (objet classe Stbl)
        - liste_extract : extraction brute de la feuille STBL du classeur'''

    def __init__(self, liste_extract_stbl):
        self.liste_donnees_stbl = []
        self.liste_stbl         = []
        self.liste_extract      = liste_extract_stbl


    '''
        Verifie si une donnee existe deja dans la liste
    '''
    def _VerifierPresenceDonnee(self, nom):
        index_data = -1
        trouve = False

        for elt in self.liste_donnees_stbl:
            index_data += 1

            if(elt.nom == nom):
                trouve = True
                break

        if (trouve == False): index_data = -1

        return index_data

    '''
        Retourne la liste des STBL
    '''
    def ListerStbl(self):
        liste_stbl = []
        for data_stbl in self.liste_donnees_stbl:
            print(data_stbl)
            for data_instance in data_stbl.liste_instances:
                if(data_instance.stbl not in liste_stbl):
                    liste_stbl.append(data_instance.stbl)
        return(liste_stbl)


    def SaveToExcel(self):

        # Sauvegarde de la liste des donnees de type classe StblDonne
        liste_to_save = []
        for data_stbl in self.liste_donnees_stbl:
            record = []
            record.append(data_stbl.nom)
            for data_instance in (data_stbl.liste_instances):
                record.append(data_instance.stbl)
                record.append(data_instance.io)
                record.append(data_instance.valeur)
            liste_to_save.append(record)
        ddd_utils.sauvegarder_liste_in_excel_xslx(liste_to_save, "toto.xlsx", "STBL")

        liste_to_save = []
        for stbl in self.liste_stbl:
            for data_stbl in stbl.liste_donnees:
                record = []
                record.append(stbl.nom)
                record.append(data_stbl.nom)
                # for data_instance in (data_stbl.liste_instances):
                    # record.append(data_instance.stbl)
                    # record.append(data_instance.io)
                    # record.append(data_instance.valeur)
            liste_to_save.append(record)
        ddd_utils.sauvegarder_liste_in_excel_xslx(liste_to_save, "toto.xlsx", "STBL2")




    '''
        Construit la liste des STBL (classes de type Stbl)
    '''
    def _ConstruireListeStbl(self):

        print("_ConstruireListeStbl")

        # recuperation de la liste des STBL
        liste_nom_stbl = self.ListerStbl()

        # creation des classes STBL
        for nom_stbl in liste_nom_stbl:
            a = Stbl(nom_stbl)
            a.ChargerDonnee(self.liste_donnees_stbl)
            a.Afficher()
            self.liste_stbl.append(a)
        # a = Stbl('OBS')
        # a.ChargerDonnee(self.liste_donnees_stbl)
        # self.liste_stbl.append(a)


        for stbl in self.liste_stbl:
            print(stbl)

        liste_dict_donnee = []
        # boucle sur toutes les donnees pour contruire une liste de dico d'enrigistrements atomiques
        for _stbl_donnee in self.liste_donnees_stbl:
            for _stbl_instance in _stbl_donnee.liste_instances:
                data = {'nom'    : _stbl_donnee.nom,
                        'stbl'   : _stbl_instance.stbl,
                        'io'     : _stbl_instance.io,
                        'valeur' : _stbl_instance.valeur}
                # data = 0
                liste_dict_donnee.append(data)


        # for elt in liste_dict_donnee:
            # _stbl = elt['stbl']

            # # cas de la premiere donnee
            # if(len(self.liste_stbl) == 0):
                # l_stbl = Stbl(_stbl)
                # l_stbl.AjouterDonnee(data)
                # self.liste_stbl.append(l_stbl)


            # print('ELT= ' + str(elt['nom']))





            # # verifier si la STBL existe deja
            # flag_stbl_nom_trouve = False
            # index_stbl = 0
            # for _stbl in self.liste_stbl:
                # if(data.nom == _stbl.nom):
                    # flag_stbl_nom_trouve = True
                    # _stbl.AjouterDonnee



    '''
        Statistique de l'ensemble des STBL
    '''
    def Stat(self):
        pass


    def LoggerContenu(self):
        for data in self.liste_donnees_stbl:
            module_logger.debug(data.nom)
            liste_etats = data.ListerEtats()
            for etat in liste_etats:
                module_logger.debug('      |- ' + str(etat))

        # self._ConstruireListeStbl()

    '''
        Charge les donnees (input : liste image de la feuille STBL du classeur)
    '''
    def LoadWb(self):
        for record in self.liste_extract:
            io     = record[0]
            stbl   = record[1]
            nom    = record[2]
            valeur = record[3]

            if(nom != ''):
                index_donnee = self._VerifierPresenceDonnee(nom)

                if(index_donnee == -1):
                    a = StblDonnee(nom)
                    a.Ajouter(stbl, io, valeur)
                    self.liste_donnees_stbl.append(a)
                else:
                    self.liste_donnees_stbl[index_donnee].Ajouter(stbl, io, valeur)
                    
        self.LoggerContenu()

        print('taille liste_donnees_stbl = ' + str(len(self.liste_donnees_stbl)))
        self._ConstruireListeStbl()
        self.SaveToExcel()

def quedal():
        pass

