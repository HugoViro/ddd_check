import pandas
import numpy as np
import logging

import ddd_utils

# create logger
module_logger = logging.getLogger('ddd_check')


def comp_wb_sheet_col(nb_col_cmp, xl_path1, xl_sheet_1, xl_col_1, xl_path2, xl_sheet_2, xl_col_2):

    # Lecture classeur 1
    
    # fabrication liste des colonnes
    liste_col_1 = range(xl_col_1, xl_col_1 + nb_col_cmp)
    
    # debug
    module_logger.info('classeur 1 : comparaison des col = ' + str(liste_col_1))
    module_logger.info('classeur 1 : lecture classeur = ' + xl_path1)
    module_logger.info('classeur 1 : lecture sheet = ' + xl_sheet_1)
 
    # lecture de l'excel
    df1 = ddd_utils.lire_classeur(xl_path1, xl_sheet_1)
    
    # conservation des colonnes utiles
    df1 = df1.ix[:,liste_col_1]
    
    # debug
    headers = df1.columns
    module_logger.info('classeur 1 : headers = ' + str(headers))
    

    # Lecture classeur 2
    
    # fabrication liste des colonnes
    liste_col_2 = range(xl_col_2, xl_col_2 + nb_col_cmp)

    # debug
    module_logger.info('classeur 2 : comparaison des col = ' + str(liste_col_2))
    module_logger.info('classeur 2 : lecture classeur = ' + xl_path2)
    module_logger.info('classeur 2 : lecture sheet = ' + xl_sheet_2)

    # lecture de l'excel
    df2 = ddd_utils.lire_classeur(xl_path2, xl_sheet_2)
    # conservation des colonnes utiles
    df2 = df2.ix[:,liste_col_2]

    # debug
    headers = df2.columns
    module_logger.info('classeur 2 : headers = ' + str(headers))

    
    
    
    # module_logger.info("********************************************************************************")    



    
    
    
    
    
    
    
    
    # df1 = pandas.DataFrame(s1, columns=['A'])
    # df2 = pandas.DataFrame(s2, columns=['B'])
    # df3 = pandas.concat([df1, df2], join='outer', axis=1)

    
    
    
    
    # df3['a'] = df1[df1.columns[xl_col_1]]
    # df3['b'] = df2[df2.columns[xl_col_2]]
    
    # print(type(df3))
    # df2 = df2.iloc[:,xl_col_2]
    headers = df2.columns
    # df2.columns = ['data']
    
    # headers = list(df2.columns)
    print(headers)


    
    module_logger.info("====================================================================================")   
    liste_df_brute = df2.values.tolist()
    for item in liste_df_brute:
        module_logger.debug(item)

    # module_logger.info("********************************************************************************")   


    difference_locations = np.where(df1.sort(axis=0) != df2.sort(axis=0))
    changed_from = df1.values[difference_locations]
    changed_to = df2.values[difference_locations]
    df_diff = pandas.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)


    

