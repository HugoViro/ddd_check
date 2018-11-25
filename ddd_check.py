# -*- coding: utf-8 -*-
""" DDD check.


Usage: ddd_check.py process <DDD_EXCEL_FILE>
       ddd_check.py debug <OPTION_DEBUG> <DDD_PICKLE_FILE>
       ddd_check.py generate <DDD_EXCEL_FILE> <DDD_EXCEL_SHEET> <DDD_PICKLE_FILE>
       ddd_check.py compare <NB_COL> <CLASSEUR_1> <FEUILLE_1> <COL_1> <CLASSEUR_2> <FEUILLE_2> <COL_2>
       ddd_check.py verify <PKL_STBL> <STBL_REP> <CLASSEUR_1> <FEUILLE_1> <COL_1>

Process FILE and optionally apply correction to either left-hand side or
right-hand side.

Arguments:
  DDD_EXCEL_FILE : data dictionnary in Excel format
  DDD_PICKLE_FILE : data dictionnary in Python Pandas Pickle format
  OPTION_DEBUG : requested field to debug method

Options:
  -h        --help
  -v        --version
  process   process check DDD from DDD_EXCEL_FILE
  debug     debug a pickle DDD from DDD_PICKLE_FILE with OPTION_DEBUG
  generate  generate a DDD_PICKLE_FILE from DDD_EXCEL_SHEET from a DDD_EXCEL_FILE
  compare   compare NB_COL between CLASSEUR_1 FEUILLE_1 COL_1 and CLASSEUR_2 FEUILLE_2 COL_2
  verify    check in the *.txt STBL exported the presence of datas in the CLASSEUR_1 FEUILLE_1 COL_1
"""


''' 
    Imports 
'''
# import lib standard
from docopt import docopt
import os
import logging
import time
import sys

# import des modules
sys.path.insert(0, './src/')
import ddd_utils
import ddd_check_pandas
import ddd_check_compare
import ddd_verify
import ddd_check_process


''' 
    logger
'''
# creation de logger
module_logger = logging.getLogger('ddd_check')


''' 
    constantes
'''

def execute():

    arguments = docopt(__doc__, version='DDD check 0.1')
    print(arguments)
    
    # option process : verification des arguments
    if(arguments['process'] == True):
        module_logger.info('choix : process')
        ddd_xl_file = arguments['<DDD_EXCEL_FILE>']
        result = ddd_check_process.verifier_presence_fichier(ddd_xl_file)
        if (result) :
            print("Process")
            module_logger.info('verification presence : OK')
        else :
            module_logger.error('verification presence : KO')
            sys.exit()  

    # option debug : travail à partir d'un onglet convertit en format binaire pandas *.pkl
    if(arguments['debug'] == True):
    
        module_logger.info('choix : debug')
    
        # fichier excel : verification et fabrication chemin
        ddd_pkl_file_path = os.getcwd() + '\\' + arguments['<DDD_PICKLE_FILE>']
        ddd_check_process.verifier_presence_fichier(ddd_pkl_file_path)    
    
        option_debug = int(arguments['<OPTION_DEBUG>'])
        module_logger.info('choix : debug + option = ' + str(option_debug))
        
        if (option_debug == 1):
            ddd_check_pandas.verifier_io_sheet_stbl(ddd_pkl_file_path)

    
    
    # option generate : verification des arguments
    if(arguments['generate'] == True):
        module_logger.info('choix : generate')
        
        # fichier excel : verification et fabrication chemin
        ddd_xl_file_path = os.getcwd() + '\\' + arguments['<DDD_EXCEL_FILE>']
        ddd_check_process.verifier_presence_fichier(ddd_xl_file_path)

        # Fabrication chemins
        ddd_pkl_file = arguments['<DDD_PICKLE_FILE>']
        ddd_pkl_file_path = os.getcwd() + '\\' + ddd_pkl_file
        
        ddd_pkl_sheet = arguments['<DDD_EXCEL_SHEET>']
        
        ddd_utils.generate_pkl_from_excel(ddd_xl_file_path, ddd_pkl_sheet, ddd_pkl_file_path)
        
        ddd_utils.lire_pkl(ddd_pkl_file_path)

        
        
    # option compare : comparaison de 2 colonnes de 2 classeurs différents et génération rapport
    # <CLASSEUR_1> <FEUILLE_1> <COL_1> <CLASSEUR_2> <FEUILLE_2> <COL_2>
    if(arguments['compare'] == True):
        module_logger.info('choix : compare')
        
        # nombre de colonnes à comparer
        nb_col_cmp = arguments['<NB_COL>']
        
        # fichier excel 1 : verification
        xl_wb_1_path = os.getcwd() + '\\' + arguments['<CLASSEUR_1>']
        ddd_check_process.verifier_presence_fichier(xl_wb_1_path)
        xl_wb_1_sheet = arguments['<FEUILLE_1>']
        xl_wb_1_col =  arguments['<COL_1>']

        # fichier excel 2 : verification
        xl_wb_2_path = os.getcwd() + '\\' + arguments['<CLASSEUR_2>']
        ddd_check_process.verifier_presence_fichier(xl_wb_2_path)
        xl_wb_2_sheet = arguments['<FEUILLE_2>']
        xl_wb_2_col =  arguments['<COL_2>']
        
        ddd_check_compare.comp_wb_sheet_col(int(nb_col_cmp), xl_wb_1_path, xl_wb_1_sheet, int(xl_wb_1_col), xl_wb_2_path, xl_wb_2_sheet, int(xl_wb_2_col))
    
    
    # option verify : verifier si toutes les données du <CLASSEUR_1> <FEUILLE_1> <COL_1> sont dans les exports au format txt dans <STBL_REP>
    if(arguments['verify'] == True):
        module_logger.info('choix : verify')
        
        # fichier pkl STBL
        pkl_stbl_path = os.getcwd() + '\\' + arguments['<PKL_STBL>']
        module_logger.info('fichier pkl STBL = ' + pkl_stbl_path)
        
        # repertoire de vérification
        stbl_rep_path = os.getcwd() + '\\' + arguments['<STBL_REP>']
        module_logger.info('repertoire des STBL = ' + stbl_rep_path)

        # execution de la fonction de recherche
        ddd_verify.process(pkl_stbl_path, stbl_rep_path)


    # # Test si presence argument
    # if (len(sys.argv) != 2):
        # module_logger.error("ERREUR argument : commande = python.exe ddd_check.py nom_fichier_excel_DDD.xslx")
        # sys.exit()

    # # Test si fichier existe
    # source_file = str(list_arg[1])
    # if (os.path.isfile(source_file) == False):
        # module_logger.error('ERREUR Fichier : ' + source_file + ' existe pas')
        # sys.exit()

    # # Fabrication fichier resutlat et chemins
    # source_path = os.getcwd() + '\\' + source_file
    # dest_path   = os.getcwd() + '\\' + source_file
    # dest_path = dest_path[:-5] + '_' + str(time.strftime("_%Y-%m-%d-%H-%M")) + '.xlsx'

    # execution du programme d'analyse
    # ddd_check_parser.process(source_path, dest_path)
    
    
def create_logger():

    #
    # Creation du logger
    #

    # create logger with 'spam_application'
    logger = logging.getLogger('ddd_check')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('ddd_check.log', mode='w')
    fh.setLevel(logging.DEBUG)
    # formatage du fichier de log
    formatter = logging.Formatter('%(levelname)s - %(filename)s - %(funcName)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(filename)s - %(funcName)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    logger.info("Debut analyse Dictionnaire Des Données logiciel")
    
def main():

    create_logger()
    execute()

if __name__ == '__main__':
    main()
