import pandas as pd
import csv
import argparse

def summarize(file_path):
    data = pd.read_csv(file_path)
    #print(data.loc[0])
    summary = []
    sum_row = 0
    dict_img_row={}

    # find entries from experts
    for i in range(len(data)):
        if (data.username[i] == "mvonkonrat"): # looking for expert
            # create a row in summary for that image 
            summary.append([data.image[i], [data.species[i],data.sporangia[i],data.leaf_division[i]]])
            dict_img_row[data.image[i]] = sum_row
            sum_row += 1
    
    # remove rows with expert as user
    data = data[data.username != "mvonkonrat"]

    # match citizens' entries to appropriate picture
    for i in range(len(data)):
        image = data.image[i]
        summary_row_num = dict_img_row.get(image,"NA")
        if summary_row_num == "NA": # skip entries that don't have an expert response for that image
            continue
        summary_entry = [data.species[i], data.sporangia[i], data.leaf_division[i]]
        summary[summary_row_num].append(summary_entry)
    
    # Create a new data frame 
    df_summary = pd.DataFrame()
    for entry in summary:
        if len(entry) <=2: #no user entries for tha species
            #image name, expert species, other species, expert sporangia responses, other sporangia responses, expert fern div responses, other fern div responses
            df_summary = df_summary.append([[entry[0], entry[1][0], "N/A", "N/A", entry[1][1], "N/A", "N/A", entry[1][2], "N/A", "N/A",0]])
        else:
            expert_response = [entry[1][0].lower(), entry[1][1], entry[1][2]] # species, sporangia, divisions
            i = 2 # index starts at 2 bc 0 is image name and 1 is the expert response
            num_user_entries = 1.0*(len(entry)-2)
            num_matches = [0, 0, 0] # species, sporangia, divisions
            while i < len(entry):
                user_response = entry[i]
                j = 0
                while j < len(user_response):
                    if user_response[j] == expert_response[j]:
                        num_matches[j] += 1
                    j += 1
                i += 1
            percent_matches = []
            for num in num_matches:
                percent_matches.append(100*num/num_user_entries)
            df_summary = df_summary.append([[entry[0], \
                entry[1][0],\
                str(percent_matches[0]) ,\
                str(100-percent_matches[0]),\
                entry[1][1],\
                str(percent_matches[1]),\
                str(100-percent_matches[1]),\
                entry[1][2],\
                str(percent_matches[2]),\
                str(100-percent_matches[2]),\
                num_user_entries]])
    df_summary = df_summary.rename({0: "Image Name",\
                                    1: "Expert Species Response",\
                                    2: "% Match with Expert Species" ,\
                                    3: "% NOT Match with Expert Species",\
                                    4: "Expert Sporangia Response",\
                                    5: "% Match with Expert Sporangia" ,\
                                    6: "% NOT Match with Expert Sporangia" ,\
                                    7: "Expert Leaf Division Response",\
                                    8: "% Match with Expert Division",\
                                    9: "% NOT Match with Expert Division",\
                                    10: "Number of User Entries"}, axis = "columns")
    return df_summary

if __name__ == '__main__':
    parser = argparse.ArgumentParser('data to be imported')
    parser.add_argument('-f',
                        '--file',
                        default='dli_parsed_data_mvk.csv',
                        help='Summary of responses compared to expert')
    args = parser.parse_args()
    summary_df = summarize(args.file)
    summary_df.to_csv(r'DLI_Summary.csv', encoding = 'utf-8', index=False)