import pandas as pd

def get_species(df, row_num, key):
    spec_id=df.subject_ids[row_num]
    indices=pd.Index(key)
    print(indices.get_loc(spec_id))
    
data=pd.read_csv(open(r'C:\Users\achen\Desktop\Sum19FM\GitCopy\microplants_cleansing\time_testing.csv', encoding='utf-8'))
matches=pd.read_csv(open(r'C:\Users\achen\Desktop\Sum19FM\GitCopy\microplants_cleansing\MatchingIDs.csv', encoding='utf-8'))
get_species(data,0,matches)