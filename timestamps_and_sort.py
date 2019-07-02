import pandas as pd
import json
import itertools
from plant_and_segment_classes import *
#to make sure the above works, go to your computers settings > search advanced settings > view more results > view advanced settings > environment variables > select PATH under system variables > New > add the path to this location
#import plant_and_segment_classes
import argparse
import csv

#------------------cleaning---------------------------
def vals_to_new_column(data_column):
    """
    takes the data.annotations column as a parameter
    returns dataframe with individual segment coordinates stored in a row
    """
    list_vals = []
    for entry in json.loads(data_column)[0]['value']:
        list_vals.append([entry['x1'], entry['y1'], entry['x2'], entry['y2']])
    return list_vals


def goodVsBadData(data_table):
    """
    takes the datasheet with 'listed_vals' column as a parameter
    returns data that corresponds with a timestamp and an age
    """

    #read the ages file as csv
    f = open(r'C:\Users\achen\Desktop\Sum19FM\CSVSheets\age_data.csv', encoding='utf-8')
    ageFile = pd.read_csv(f)
    df = pd.DataFrame(
    )  #columns = [0: 'classification_id', 'username', 'created_at', 'subject_data' , 'angle', 'major_axis_length', 'x1_major', 'x2_major', 'y1_major', 'y2_major', 'minor_axis_length', 'x1_minor', 'x2_minor', 'y1_minor', 'y2_minor'] (will rename at end)
    #dg = pd.DataFrame() #new csv with

    #--------------Just some testing print statements-----------------
    #print(data_table.created_at[3])
    # print(data_table.classification_id[0])
    #print(ageFile.Time_Stamp[1])
    #print(data_table.loc[[1]])
    #print(ageFile.loc[[0]])
    #print(len(ageFile)) #expect 1024

    row_num = 0  #row number of measurement data sheet
    i = 0
    found_time_match=False
    while i < len(ageFile) and row_num<len(data_table):  #use a while loop because we don't want i to increment if measurement data has two entries with same timestamp
        if not found_time_match:
            while row_num < len(data_table) and ageFile.Time_Stamp[i] != data_table.created_at[row_num]:
                row_num = row_num + 1
                found_time_match=True
        if row_num >= len(data_table):  #if out of bounds, end immediately
            break
        for combo in itertools.combinations(data_table.listed_vals[row_num],2):
            segments_to_check = CheckLeaf(combo[0], combo[1])
            if segments_to_check.line_segments_intersect() and segments_to_check.on_screen():
                if (int(data_table.workflow_id[row_num]) == 3449) and (
                        float(data_table.workflow_version[row_num]) == 5.8):
                    lengths_minor_major = segments_to_check.calc_lengths_minor_major(
                    )
                    intersection_x = segments_to_check.find_the_intersection_point(
                    )[0]
                    intersection_y = segments_to_check.find_the_intersection_point(
                    )[1]
                    if abs(segments_to_check.calc_angle_between_segments()) > 80.0: # and ageFile.Time_Stamp[i] == data_table.created_at[row_num]:
                        df = df.append([[data_table.classification_id[row_num], \
                                data_table.user_name[row_num], \
                                data_table.created_at[row_num], \
                                data_table.subject_data[row_num], \
                                data_table.subject_ids[row_num], ageFile.Age[i], \
                                "Good", \
                                segments_to_check.calc_angle_between_segments(), \
                                intersection_x, \
                                intersection_y, \
                                lengths_minor_major[0], \
                                lengths_minor_major[1][0], \
                                lengths_minor_major[1][1], \
                                lengths_minor_major[1][2], \
                                lengths_minor_major[1][3], \
                                lengths_minor_major[2], \
                                lengths_minor_major[3][0], \
                                lengths_minor_major[3][1], \
                                lengths_minor_major[3][2], \
                                lengths_minor_major[3][3]]])
                    else:
                        df = df.append([[data_table.classification_id[row_num], \
                                data_table.user_name[row_num], \
                                data_table.created_at[row_num], \
                                data_table.subject_data[row_num], \
                                data_table.subject_ids[row_num], \
                                ageFile.Age[i], \
                                "Bad", \
                                segments_to_check.calc_angle_between_segments(), \
                                intersection_x, \
                                intersection_y]])
                else:
                    df = df.append([[data_table.classification_id[row_num], \
                                data_table.user_name[row_num], \
                                data_table.created_at[row_num], \
                                data_table.subject_data[row_num], \
                                data_table.subject_ids[row_num], \
                                ageFile.Age[i], \
                                "Bad", \
                                segments_to_check.calc_angle_between_segments(), \
                                intersection_x, \
                                intersection_y]])
        # because sometimes two timestamps from measurement data match with a timestampe from age data,
        # we want to apply that age data to both the entries from measurement data
        if (i + 1) == len(ageFile): #last row in age data
            if (row_num+1)==len(data_table): #last row in measurement data as well so next step will have us quit
                i = i + 1
                #if at end of age data but not measurement data, only increment row_num (done below the else if)
            else:
                row_num = row_num + 1  #otherwise the remaining elements in measurement data should match to last entry of age data
            continue #skip everything else, and this will end the outer loop--stop looking at data
        elif (row_num+1)==len(data_table): #last row of measure data but not last row of age data
            row_num = row_num + 1 #row_num will become out of bounds, ending the loops
            continue
        #because of the continue statements above, reaching this point means there are valid elements at index i+1 and row_num+1
        if (ageFile.Time_Stamp[i+1] == data_table.created_at[row_num+1]):  #if the next entry in both data sets DO have the same timestamp, increment the row for age data
            i = i + 1
        #ONLY the line below this comment will execute if
        row_num = row_num + 1  #no matter what, we should be looking at the next item in measurement data

    df = df.rename({0: 'classification_id', \
                    1: 'username', \
                    2: 'created_at', \
                    3: 'subject_data', \
                    4: 'subject_id', \
                    5: 'age_group', \
                    6: 'validity', \
                    7: 'angle', \
                    8: 'intersection_point_x', \
                    9: 'intersection_point_y', \
                    10: 'major_axis_length', \
                    11: 'major_x1', \
                    12: 'major_y1', \
                    13: 'major_x2', \
                    14: 'major_y2', \
                    15:'minor_axis_length', \
                    16: 'minor_x1', \
                    17: 'minor_y1', \
                    18: 'minor_x2', \
                    19: 'minor_y2',},\
                   axis='columns')
    return df


def clean_data(file_name):
    print('importing ', file_name)
    data = pd.read_csv(file_name)
    data['listed_vals'] = data['annotations'].apply(vals_to_new_column)
    newsheet = goodVsBadData(data)
    print("returning new sheet now")
    return newsheet


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser('data to be imported')
#     parser.add_argument('-f',
#                         '--file',
#                         default='classifications_short.csv',
#                         help='Process some microplant data')
#     args = parser.parse_args()
#     clean_data(args.file)
measurements_data = open(
    r'C:\Users\achen\Desktop\Sum19FM\CSVSheets\mini_md_32_51.csv',
    encoding='utf-8')
#'C:\Users\achen\Desktop\Sum19FM\CSVSheets\mini_microplants_measurements.csv','r')
newdata = clean_data(measurements_data)
newdata.to_csv(r'C:\Users\achen\Desktop\Sum19FM\CSVSheets\scruppedData.csv')