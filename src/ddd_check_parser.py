# -*- coding: utf-8 -*-

import pandas
import ddd_check_pandas
import logging
import numpy as np
import time

# create logger
module_logger = logging.getLogger('ddd_check')


def process(source_path, dest_path):

    
    ddd_check_pandas.test01()
    
    # st = time.clock()
    # df_stbl_brute = ddd_check_pandas.lire_classeur(source_path, "STBL")    
    # print (round(time.clock() - st,3), "seconds of loading time.")





