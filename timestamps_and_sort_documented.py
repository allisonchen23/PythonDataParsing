#libraries/packages
import pandas as pd
import json
import itertools
#datetime is used to directly compare the timestamps
from datetime import datetime, timedelta
#pytz is for time zone conversion
import pytz
from pytz import timezone
#local files
from plant_and_segment_classes import *
from age_data_function import *
from match_species import match_species_id
from species_dict import make_species_dict
#to make sure the above works, go to your computers settings > search advanced settings > view more results > view advanced settings >
#environment variables > select PATH under system variables > New > add the path to this location

#argparse allows us to run code in terminal with an argument
import argparse
import csv


#------------------cleaning---------------------------
#vals_to_new_column takes one entry, finds the column with measurement data (that will have 0 or more measurement entries), 
# and creates a list of the coordinates of each point, essentially getting rid of extraneous data in that column
def vals_to_new_column(data_column):
    """
    takes the data.annotations column as a parameter
    returns dataframe with individual segment coordinates stored in a row
    """
    # create an empty list
    list_vals = []
    #for each entry, extract the coordinates of endpoints for each line segment drawn in the image
    #note: units are pixels
    for entry in json.loads(data_column)[0]['value']:
        list_vals.append([entry['x1'], entry['y1'], entry['x2'], entry['y2']])
    # return list of line segments
    return list_vals

#goodvsBadData will do measurements, label entries as good/bad and in or out of the desired time frame
# output data in a readable manner
def goodVsBadData(data_table):
    """
    takes the datasheet with 'listed_vals' column as a parameter
    returns data that corresponds with a timestamp and an age
    """

    #read the ages file as csv
    #    f = open(r'G:\TimestampMatching\ageFile.csv', encoding='utf-8')
    # f = open(r'C:\Users\achen\Desktop\Sum19FM\CSVSheets\ageFile.csv',
    #          encoding='utf-8')
    # ageFile = pd.read_csv(f)

    #cleanse_age is function in age_data_function.py
    ageFile = cleanse_age(r'age_data_google_analytics.csv')  #stores dataframe into variable ageFile and proceed as normal
    #convert the string to a datetime object in the ageFile
    ageFile.time_stamp = pd.to_datetime(ageFile.time_stamp)
    #df is the dataframe we will return
    df = pd.DataFrame()
    #convert the strings in data_table (from csv of measurements) to datetime objects
    data_table.created_at = pd.to_datetime(data_table.created_at)
    data_table.created_at = data_table.created_at.values.astype('<M8[m]')
    data_table.created_at = data_table.created_at.dt.tz_localize('UTC')

    #--------------Just some testing print statements-----------------
    # print(data_table.created_at.head())
    # print(ageFile.time_stamp)
    #print(data_table.classification_id[0])
    #print(ageFile.time_stamp[1])
    #print(data_table.loc[[1]])
    #print(ageFile.loc[[0]])
    #print(len(ageFile)) #expect 1024

    #-------------Create the species dictionary-----------
    # key is the subject_id and the value is the species
    matchingIDs = pd.read_csv(r'matchingIDs.csv', encoding='utf-8')

    # these two functions are imported
    species_key = match_species_id(matchingIDs)
    species_dict=make_species_dict(species_key)
    
    # species_dict ends up being a dictionary (python version of hashtable)
    # Connecting the image ID and the species

    row_num = 0  #row number of measurement data sheet
    i = 0 # row number of ageFile
    found_time_match = False #boolean to skip over the beginning entries in data_table that don't yet match with a timestamp in ageFile

    # loop through both CSVs simulataneously
    while i < len(ageFile) and row_num < len(data_table):
        #use a while loop because we don't want i to increment if measurement data has two entries with same timestamp
        if not found_time_match: #this if allows us to skip everything before the first timestamp in age data
            while row_num < len(data_table) and ageFile.time_stamp[
                    i] != data_table.created_at[row_num]:
                row_num = row_num + 1
            found_time_match = True # ensure we never enter this if again
        if row_num >= len(data_table):  #if out of bounds, end immediately
            break

        #each entry consists of essentially segments determined by the x and y coordinates of the end points. 
        # This for loop make all possible combinations of 2 segments on an image. If they don't intersect or aren't on the screen, 
        # we throw them out
        for combo in itertools.combinations(data_table.listed_vals[row_num],
                                            2):
            segments_to_check = CheckLeaf(combo[0], combo[1]) #combination of 2 segments from 1 image

            # if the segments intersect and are on the screen, they're most likely a major and minor axes of lobule
            if segments_to_check.line_segments_intersect(
            ) and segments_to_check.on_screen():
                if (int(data_table.workflow_id[row_num]) == 3449) and (float(
                        data_table.workflow_version[row_num]) == 5.8):
                    # do some calculations for segment lengths and point of intersection
                    lengths_minor_major = segments_to_check.calc_lengths_minor_major(
                    )
                    intersection_x = segments_to_check.find_the_intersection_point(
                    )[0]
                    intersection_y = segments_to_check.find_the_intersection_point(
                    )[1]

                    #variables for in or out of time range
                    # Any measurement over 2 minutes after an age timestamp is labeled as OUT since we cannot confidently say that this is the same person
                    time_range=""
                    if (ageFile.time_stamp[i] == data_table.created_at[row_num] \
                       or ageFile.time_stamp[i] + timedelta(minutes=2) >= data_table.created_at[row_num]):
                        time_range = "In"
                    else:
                        time_range="Out"

                    #variables for good or bad data based on angle (data quality check)
                    validity=""
                    if (abs(segments_to_check.calc_angle_between_segments()) >= 80.0):
                        validity = "Good"
                    else:
                        validity = "Bad"

                    #find the current entry in the species diectionary to get a species (if there)
                    cur_id=data_table.subject_ids[row_num]
                    cur_species=species_dict.get(cur_id,"N/A") #cur_species = "N/A" if not found
                    if not (cur_species == "N/A"):
                        cur_species=cur_species[0]
                    # Below adds a row onto df (the output data frame) with the values we care about
                    df = df.append([[data_table.classification_id[row_num], \
                                data_table.user_name[row_num], \
                                data_table.created_at[row_num], \
                                data_table.subject_data[row_num], \
                                data_table.subject_ids[row_num], \
                                cur_species, \
                                ageFile.age[i], \
                                validity, \
                                time_range, \
                                abs(segments_to_check.calc_angle_between_segments()), \
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

        #-----------------Below steps through the sheets appropriately, handling any weird cases------------------

        # because sometimes two timestamps from measurement data match with a timestampe from age data,
        # we want to apply that age data to both the entries from measurement data
        if (i + 1) == len(ageFile):  #last row in age data
            if (row_num + 1) == len(
                    data_table
            ):  #last row in measurement data as well so next step will have us quit
                i = i + 1
                #if at end of age data but not measurement data, only increment row_num (done below the else if)
            else:
                row_num = row_num + 1  #otherwise the remaining elements in measurement data should match to last entry of age data
            continue  #skip everything else, and this will end the outer loop--stop looking at data
        elif (row_num + 1) == len(data_table):  #last row of measure data but not last row of age data
            row_num = row_num + 1  #row_num will become out of bounds, ending the loops
            continue
        #because of the continue statements above, reaching this point means there are valid elements at index i+1 and row_num+1
        if (ageFile.time_stamp[i + 1] == data_table.created_at[row_num + 1]):
            #if the next entry in both data sets DO have the same timestamp, increment the row for age data
            i = i + 1
        elif (ageFile.time_stamp[i + 1] < data_table.created_at[row_num + 1]):
            #account for the case if there is a timestamp in age data where no measurement data timestamp is within 2 minutes of it
            while (ageFile.time_stamp[i + 1] + timedelta(minutes=2) < data_table.created_at[row_num + 1]):
                i = i + 1
                
            if (ageFile.time_stamp[i + 1] <= data_table.created_at[row_num + 1]):
                i = i + 1
            elif (ageFile.time_stamp[i + 1] > data_table.created_at[row_num + 1]): #at most we will be over by 1 timestamp
                i = i - 1
        row_num = row_num + 1  #no matter what, we should be looking at the next item in measurement data

    # rename columns
    df = df.rename({0: 'classification_id', \
                    1: 'username', \
                    2: 'created_at', \
                    3: 'subject_data', \
                    4: 'subject_id', \
                    5: 'species', \
                    6: 'age_group', \
                    7: 'validity', \
                    8: 'in_time_range', \
                    9: 'angle', \
                    10: 'intersection_point_x', \
                    11: 'intersection_point_y', \
                    12: 'major_axis_length', \
                    13: 'major_x1', \
                    14: 'major_y1', \
                    15: 'major_x2', \
                    16: 'major_y2', \
                    17:'minor_axis_length', \
                    18: 'minor_x1', \
                    19: 'minor_y1', \
                    20: 'minor_x2', \
                    21: 'minor_y2',},\
                   axis='columns')
    # at very end, return this new dataframe
    return df

# essentially calls all the functions we made up to this point
def clean_data(file_name): #takes in CSV already opened (so not just the path)
    print('importing ', file_name)
    data = pd.read_csv(file_name)
    data['listed_vals'] = data['annotations'].apply(vals_to_new_column)
    newsheet = goodVsBadData(data)
    print("returning new sheet now")
    return newsheet

#----------Allows to be used with any file---------------
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser('data to be imported')
#     parser.add_argument('-f',
#                         '--file',
#                         default='classifications_short.csv',
#                         help='Process some microplant data')
#     args = parser.parse_args()
#     clean_data(args.file)

#calling all our functions
measurements_data = open(r'time_testing.csv', encoding='utf-8')
# measurements_data = open(r'G:\TimestampMatching\time_testing.csv', encoding='utf-8')
newdata = clean_data(measurements_data)
newdata.to_csv(r'scruppedData.csv', encoding='utf-8')
# newdata.to_csv(r'G:\TimestampMatching\scruppedData.csv', encoding = 'utf-8')