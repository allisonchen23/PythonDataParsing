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
        summary_entry = 
    print(len(data))
    print(len(summary))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('data to be imported')
    parser.add_argument('-f',
                        '--file',
                        default='dli_parsed_data_mvk.csv',
                        help='Summary of responses compared to expert')
    args = parser.parse_args()
    summarize(args.file)