import pandas as pd
from pandas import *
import json
import itertools
import argparse
import csv
import numpy as np

def match_species_id(matchingIDs):
    voucher_short = pd.read_csv(r'G:\TimestampMatching\voucher_short.csv',
                                  encoding='utf-8',dtype=str)
    
    final = pd.DataFrame()
    row_num = 0
    i= 0
    while i < len(voucher_short):
        while row_num < len(matchingIDs):
            if str(voucher_short['number'][i]) in \
               matchingIDs['image_name'][row_num]:
                final = final.append([[matchingIDs['subject_id'].loc[row_num], \
                                      voucher_short['species'].loc[i],voucher_short.number.iloc[i]]])

            row_num = row_num + 1
        row_num=0
        i = i + 1
    

    final = final.rename({0: 'subject_id', \
                  1: 'species', \
                  2: 'number'}, \
                axis = 'columns')
    print(final.head())
    return final

matchingIDs = pd.read_csv(r'G:\TimestampMatching\matchingIDs.csv',encoding = 'utf-8',dtype=str)
newdata = match_species_id(matchingIDs)
newdata.to_csv(r'G:\TimestampMatching\speciesKey.csv',encoding = 'utf-8',index=False)
