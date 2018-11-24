# -*- coding: utf-8 -*-

import os
import logging
import sys

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Color

from datetime import datetime

import matrice_traca_file_utils


# create logger
module_logger = logging.getLogger('matrice_traca')

def contruire_matrice_STBL(matrice_brute):

    list_req_sf        = []
    liste_matrice_stbl = []
    record_stbl        = []

    for item in matrice_brute:

        taille = len (item)
        module_logger.debug('Item::taille= ' + str(taille) + ' ::' + str(item))
        req_stbl   = "ERR"
        perim_stbl = "ERR"
        titre_stbl = "ERR"
        req_sf     = "ERR"

        # Exigence STBL
        if (taille > 0 and item[0] != None):
            req_stbl = item[0]
            req_stbl = req_stbl.replace("['", '').replace("']", '')
        else:
            req_stbl = "exigence_stbl_vide"

        # Perimetre
        if (taille > 2 and item[2] != None):
            perim_stbl = item[2]
            perim_stbl = perim_stbl.replace("['", '').replace("']", '')
        else:
            perim_stbl = "perimetre_vide"

        # Titre
        if (taille > 3 and item[3] != None):
            titre_stbl = item[3]
            titre_stbl = titre_stbl.replace("['", '').replace("']", '')
        else:
            titre_stbl = "Pas de titre"

        # Exigences SF couvertes
        list_req_sf = []
        nb_req_sf = 0
        if (item[1] == None):
            req_sf = ""
            nb_req_sf = 1
        else:
            # Virer l'eventuel \n de fin
            
            str_sf_brute = item[1]
            while (str_sf_brute.endswith('\n')):
                str_sf_brute = str_sf_brute[:-1]
                module_logger.debug('suppression EOL = ' + str_sf_brute)

        
            # Plusieurs exigences SF couvertes par STBL
            if ('\n' in str_sf_brute):
                for part in str_sf_brute.split('\n'):
                    if (part == None):
                        list_req_sf.append("exigence_sf_vide")
                    else:
                        req1 = part.replace("['", '').replace("']", '')
                        list_req_sf.append(req1)
                        nb_req_sf += 1
            else:
                req_sf = str_sf_brute
                req_sf.replace("['", '').replace("']", '')
                nb_req_sf = 1

        # Contruction de la liste
        if(nb_req_sf == 0):
            module_logger.error("ERREUR sur taille")
        elif (nb_req_sf == 1):
            record_stbl        = []
            record_stbl.append(req_stbl)
            record_stbl.append(req_sf)
            record_stbl.append(perim_stbl)
            record_stbl.append(titre_stbl)
            liste_matrice_stbl.append(record_stbl)
            module_logger.debug('Record = ' + str(record_stbl))
        else:
            for elt in list_req_sf:
                record_stbl        = []
                record_stbl.append(req_stbl)
                record_stbl.append(elt)
                record_stbl.append(perim_stbl)
                record_stbl.append(titre_stbl)
                module_logger.debug('Record = ' + str(record_stbl))
                liste_matrice_stbl.append(record_stbl)


    for ligne in liste_matrice_stbl:
        module_logger.debug(ligne)

    return (liste_matrice_stbl)

    
