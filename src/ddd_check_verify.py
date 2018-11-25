# -*- coding: utf-8 -*-

import os
import logging
from pathlib import Path

import ddd_utils
import sheet_stbl

# create logger
module_logger = logging.getLogger('ddd_check')







def lire_extract_stbl(rep_path):

    for file in os.listdir(rep_path):
        if file.endswith(".txt"):

            filename = file.replace('.txt', '')
            print(filename)

            file = os.path.join(rep_path, file)

            with open(file, encoding='mbcs') as openfile:
                module_logger.info('ouverture fichier = ' + file)

                liste_file = []
                for line in openfile:
                    module_logger.debug(line)
                    liste_file.append(line)







def Analyser_wb_stbl(pkl_stbl_path):

    df_wb_stbl_pkl = ddd_utils.lire_pkl(pkl_stbl_path)
    liste_wb_stbl = df_wb_stbl_pkl.values.tolist()
    MyExtract = sheet_stbl.StblExctract(liste_wb_stbl)
    MyExtract.LoadWb()
    # MyExtract.Afficher()
    # liste_stbl = MyExtract.ListerStbl()
    # print(str(liste_stbl))



def process(pkl_stbl_path, rep_path):

    print("Salut")
    
    index_test = -1
    
    for i in range (1,2):
        index_test += 1
        print('index_test = ' + str(index_test))
    
    Analyser_wb_stbl(pkl_stbl_path)



