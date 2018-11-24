# -*- coding: utf-8 -*-

import logging
import os


# create logger
module_logger = logging.getLogger('ddd_check')

def verifier_presence_fichier(file_name):

    module_logger.info('verification presence : ' + file_name)
    
    if (os.path.isfile(file_name) == False):
        module_logger.error('verification presence : KO')
        return False   
    else:
        module_logger.info('verification presence : OK')
        return True