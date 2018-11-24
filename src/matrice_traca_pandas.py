# -*- coding: utf-8 -*-

import pandas
import matrice_traca_file_utils
import logging
import numpy as np

# create logger
module_logger = logging.getLogger('matrice_traca')

C_COL_DESC = ('req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'uc_id', 'req_stbl_titre')


def lire_classeur(path, sheet_name):

    # Lecture du fichier directement dans une data frame
    xl = pandas.ExcelFile(path)
    df = xl.parse(sheet_name)

    # renomage des colonnes
    # df.columns = ['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'uc_id', 'req_stbl_titre']
    df.columns = C_COL_DESC

    desc_matrice = df.describe()

    # Infos debug
    module_logger.info('lecture classeur --> ' + path)
    module_logger.info('lecture feuille --> ' + sheet_name)
    # module_logger.info('champs = ' + desc_matrice)

    liste_df_brute = df.values.tolist()
    for item in liste_df_brute:
        module_logger.debug(item)

    module_logger.info("********************************************************************************")

    return (df)

'''

    Nettoyage des lignes avec \n dans la colonne req_sf

'''
def nettoyer_df_matrice_brute_col_sf(df):

    module_logger.info("Nettoyage des sauts de lignes")

    # Recherche et suppression des \n dans la colonne 'req_sf'
    s = df['req_sf'].str.split('\n').apply(pandas.Series, 1).stack()
    # to line up with df's index
    s.index = s.index.droplevel(-1)
    # needs a name to join
    s.name = 'req_sf'
    del df['req_sf']
    df = df.join(s)
    # df = df[['req_stbl', 'req_stbl_ver', 'req_stbl_perim', 'req_sf', 'req_stbl_titre']]
    df = df[['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'uc_id', 'req_stbl_titre']]
    # df = df[[C_COL_DESC]]
    cols = df.columns.tolist()


    module_logger.info("Nettoyage des req_sf vides")

    # Suppression des enregistrements avec saut de ligne compris dans 'req_sf'
    filter = df["req_sf"] != ""
    df1 = df[filter]

    liste_df_brute = df1.values.tolist()
    for item in liste_df_brute:
        module_logger.debug(item)

    module_logger.info("********************************************************************************")

    return(df1)

    
'''

    Nettoyage des lignes avec \n dans la colonne req_sf

'''
def nettoyer_df_matrice_brute_col_uc(df):

    module_logger.info("Nettoyage des sauts de lignes")

    # Recherche et suppression des \n dans la colonne 'uc_id'
    s = df['uc_id'].str.split('\n').apply(pandas.Series, 1).stack()
    # to line up with df's index
    s.index = s.index.droplevel(-1)
    # needs a name to join
    s.name = 'uc_id'
    del df['uc_id']
    df = df.join(s)
    # df = df[['req_stbl', 'req_stbl_ver', 'req_stbl_perim', 'req_sf', 'req_stbl_titre']]
    df = df[['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'uc_id', 'req_stbl_titre']]
    # df = df[[C_COL_DESC]]
    cols = df.columns.tolist()


    module_logger.info("Nettoyage des uc_id vides")

    # Suppression des enregistrements avec saut de ligne compris dans 'uc_id'
    filter = df["uc_id"] != ""
    df1 = df[filter]

    liste_df_brute = df1.values.tolist()
    for item in liste_df_brute:
        module_logger.debug(item)

    module_logger.info("********************************************************************************")

    return(df1)
    
    

def generer_matrice_sf_stbl(data):

    df = pandas.DataFrame(data, columns=['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'req_stbl_titre'])
    df1 = df[['req_sf', 'req_stbl', 'req_stbl_ver', 'req_stbl_perim', 'req_stbl_titre']]
    df1 = df1.sort_values(by=['req_sf', 'req_stbl'], ascending=[True, True])

    return (df1)

def generer_matrice_stbl_sf(data):

    df = pandas.DataFrame(data, columns=['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'req_stbl_titre'])
    df1 = df[['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'req_stbl_titre']]
    df1 = df1.sort_values(by=['req_stbl', 'req_sf'], ascending=[True, True])

    return (df1)
    
    
def generer_matrice_stbl_uc(data):

    df = pandas.DataFrame(data, columns=['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'uc_id', 'req_stbl_titre'])
    df1 = df[['req_stbl', 'uc_id', 'req_stbl_titre']]
    df1 = df1.sort_values(by=['req_stbl', 'uc_id'], ascending=[True, True])
    df1 = df1.drop_duplicates()

    return (df1)

def generer_matrice_uc_stbl(data):

    df = pandas.DataFrame(data, columns=['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'uc_id', 'req_stbl_titre'])
    df1 = df[['uc_id', 'req_stbl', 'req_stbl_titre']]
    df1 = df1.sort_values(by=['uc_id', 'req_stbl'], ascending=[True, True])
    df1 = df1.drop_duplicates()

    return (df1)

def lister_stbl_non_couvrantes(data):

    df = pandas.DataFrame(data, columns=['req_stbl', 'req_stbl_ver', 'req_sf', 'req_stbl_perim', 'req_stbl_titre'])
    df_sf_empty = df.loc[df['req_sf'].isnull()]

    return(df_sf_empty)


def analyser_matrice(matrice_sf_stbl):

    lst_stat = []
    record = []

    # statistiques
    desc_sf_stbl = matrice_sf_stbl.describe()

    # nombre exigences sf
    df_nb_req_sf   = desc_sf_stbl.loc['unique']['req_sf']
    # nombre exigences stbl
    df_nb_req_stbl = desc_sf_stbl.loc['unique']['req_stbl']
    # liste des versions exigences
    lst_req_ver = matrice_sf_stbl['req_stbl_ver'].unique()

    # comptage des exigences stbl / version
    df_matrice_stbl =  matrice_sf_stbl[['req_stbl', 'req_stbl_ver']]
    df_matrice_stbl = df_matrice_stbl.drop_duplicates()
    df_synthese_version = df_matrice_stbl.groupby('req_stbl_ver').count()
    lst_synthese_versions = df_synthese_version.reset_index().values.tolist()

    # comptage des exigences stbl / version en %
    df_pct_versions = df_synthese_version.apply(lambda x:100 * x / float(x.sum()))
    lst_synthese_versions_prct = df_pct_versions.reset_index().values.tolist()

    # fabrication synthese en list of list
    record.append("Nombre exigences sf")
    record.append(df_nb_req_sf)
    lst_stat.append(record)

    record = []
    record.append("Nombre exigences stbl")
    record.append(df_nb_req_stbl)
    lst_stat.append(record)

    record = []
    record.append("Nombre exigences stbl / version")
    lst_stat.append(record)
    lst_stat.append(['Version', 'Nombre'])
    for elt in lst_synthese_versions:
        lst_stat.append(elt)

    record = []
    record.append("Nombre exigences stbl / version (%)")
    lst_stat.append(record)
    lst_stat.append(['Version', '%'])
    for elt in lst_synthese_versions_prct:
        lst_stat.append(elt)

    return (lst_stat)

def generer_matrice(data, dest_path):

    matrice_sf_stbl = generer_matrice_sf_stbl(data)
    matrice_traca_file_utils.sauvegarder_df_in_excel_xslx(matrice_sf_stbl, dest_path, 'matrice_sf_stbl')

    matrice_stbl_sf = generer_matrice_stbl_sf(data)
    matrice_traca_file_utils.sauvegarder_df_in_excel_xslx(matrice_stbl_sf, dest_path, 'matrice_stbl_sf')
    
    matrice_stbl_uc = generer_matrice_stbl_uc(data)
    matrice_traca_file_utils.sauvegarder_df_in_excel_xslx(matrice_stbl_uc, dest_path, 'matrice_stbl_uc')

    matrice_uc_stbl = generer_matrice_uc_stbl(data)
    matrice_traca_file_utils.sauvegarder_df_in_excel_xslx(matrice_uc_stbl, dest_path, 'matrice_uc_stbl')

    matrice_stbl_non_couvrantes = lister_stbl_non_couvrantes(data)
    matrice_traca_file_utils.sauvegarder_df_in_excel_xslx(matrice_stbl_non_couvrantes, dest_path, 'exi_stbl_non_couvrantes')

    liste_analyse = analyser_matrice(matrice_sf_stbl)
    matrice_traca_file_utils.sauvegarder_liste_in_excel_xslx(liste_analyse, dest_path, 'Synthese')



