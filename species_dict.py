import csv
import pandas as pd

def make_species_dict(species_key): #take in csv that is already opened
    key_df=pd.read_csv(species_key)
    key_df = key_df.drop(['image_name','number'], axis=1)
    species_dict=key_df.set_index('subject_id').T.to_dict('list')
    # cs=species_dict.get(6262370, "N/A")
    # if not (cs=="N/A"):
    #     print(cs[0])
    # else:
    #     print(cs)
    return species_dict

spec=open(r'C:\Users\achen\Desktop\Sum19FM\GitCopy\microplants_cleansing\speciesKey.csv', encoding='utf-8')
make_species_dict(spec)