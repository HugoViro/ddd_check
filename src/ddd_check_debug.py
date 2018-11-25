import pandas
import logging

import ddd_utils

# create logger
module_logger = logging.getLogger('ddd_check')


C_STBL_COL_DESC = ('sens', 'composant', 'donnee', 'valeur')
 

def test01():
    
    index_debut = len(C_STBL_COL_DESC)
    print ("Taille=", index_debut)
    liste_index_remove = list(range(index_debut, 17))
    print(liste_index_remove)
    
    for index, item in enumerate(C_STBL_COL_DESC):
        print(index, item)    
    
    # liste_toto = str(enumerate(C_STBL_COL_DESC, start=1))
    # print (liste_toto)

 
def lire_classeur(path, sheet_name):

    # lecture du fichier directement dans une data frame
    df = pandas.read_excel(path, sheetname=sheet_name)
   
    index_debut = len(C_STBL_COL_DESC)
    index_fin = df.num_columns
    if (index_fin > index_debut):
        liste_index_remove = list(range(index_debut, index_fin))
        
    df.drop(df.columns[liste_index_remove], axis=1) 
    
    # renommage des colonnes
    df.columns = C_COL_DESC

    # Infos debug
    # desc_matrice = df.describe()
    module_logger.info('lecture classeur --> ' + path)
    module_logger.info('lecture feuille --> ' + sheet_name)
    module_logger.info('champs = ' + desc_matrice)

    liste_df_brute = df.values.tolist()
    for item in liste_df_brute:
        module_logger.debug(item)

    module_logger.info("********************************************************************************")

    return (df)
    
    
def verifier_io_sheet_stbl(file_path):

    module_logger.info('analyse cohérence io')

    # lecture du fichier directement dans une data frame
    df = ddd_utils.lire_pkl(file_path)
    
    
    