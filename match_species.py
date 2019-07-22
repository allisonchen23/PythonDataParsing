import pandas as pd
import itertools
import argparse
import csv
import numpy as np

def match_species_id(matchingIDs):
    voucher_short=pd.read_csv(r'voucher_short.csv', encoding='utf-8')
    #voucher_short = pd.read_csv(r'G:\TimestampMatching\voucher_short.csv',encoding='utf-8')
    voucher_short.number = voucher_short['number'].apply(str)
    voucher_short.number = [x.strip().replace('/','-') \
                            for x in voucher_short.number]
    voucher_short.number = [x.strip().replace(' ','') \
                            for x in voucher_short.number]
    voucher_short.number = [x.strip().replace('  ','') \
                            for x in voucher_short.number]
    #this line may be redundant
    
    final = pd.DataFrame()
    row_num = 0
    i= 0
    while i < len(voucher_short):
        while row_num < len(matchingIDs):
            if matchingIDs['image_name'][row_num].startswith("DNA") or \
               matchingIDs['image_name'][row_num].startswith("Dna"):
                if str(voucher_short.isolate[i]) in matchingIDs['image_name'][row_num]:
                    final = final.append([[matchingIDs['subject_id'].loc[row_num], \
                                       voucher_short['species'].loc[i], \
                                       matchingIDs.image_name[row_num], \
                                       voucher_short.number.iloc[i]]])
            elif ('_' + str(voucher_short['number'][i] + '_') in \
               matchingIDs['image_name'][row_num]) or \
               str(voucher_short.in_analysis[i]) in matchingIDs['image_name'][row_num] or \
               str(voucher_short.GenID[i]) in matchingIDs['image_name'][row_num]:
                final = final.append([[matchingIDs['subject_id'].loc[row_num], \
                                       voucher_short['species'].loc[i], \
                                       matchingIDs.image_name[row_num], \
                                       voucher_short.number.loc[i]]])

            row_num = row_num + 1
        row_num=0
        i = i + 1
    final = final.rename({0: 'subject_id', \
                  1: 'species', \
                  2: 'image_name', \
                  3: 'number'}, \
                axis = 'columns')
    # print(final.head())
    # print(len(final))
    return final #final is a dataframe
    

matchingIDs = pd.read_csv(r'C:\Users\achen\Desktop\Sum19FM\GitCopy\microplants_cleansing\matchingIDs.csv', encoding='utf-8')
#matchingIDs = pd.read_csv(r'G:\TimestampMatching\matchingIDs.csv',encoding = 'utf-8',dtype=str)
newdata = match_species_id(matchingIDs)
newdata.to_csv(r'C:\Users\achen\Desktop\Sum19FM\GitCopy\microplants_cleansing\speciesKey.csv', encoding='utf-8', index=False)
#newdata.to_csv(r'G:\TimestampMatching\speciesKey.csv',encoding = 'utf-8',index=False)
