import csv
import pandas as pd

def make_species_dict(key_df): #take in dataframe that is already opened
    key_df = key_df.drop(['image_name','number'], axis=1)
    species_dict=key_df.set_index('subject_id').T.to_dict('list')
    # # Helper print statements
    # cs=species_dict.get(6262370, "N/A")
    # if not (cs=="N/A"):
    #     print(cs[0])
    # else:
    #     print(cs)
    return species_dict

spec=open(r'speciesKey.csv', encoding='utf-8')
spec_df=pd.read_csv(spec)
make_species_dict(spec_df)