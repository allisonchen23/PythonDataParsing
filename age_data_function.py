import pandas as pd
from datetime import datetime, timedelta
import pytz
from pytz import timezone
import argparse

#f = open(r'C:\Users\achen\Desktop\Sum19FM\GitCopy\microplants_cleansing\age_data_google_analytics.csv', \encoding='utf-8')
#f = open(r'G:\TimestampMatching\age_data_all.csv', encoding='utf-8')
#will recieve a file to read from the directory and encode it with utf-8
def cleanse_age(full_file_path):
    f = open(f'{full_file_path}',encoding='utf-8')

    ageFile = pd.read_csv(f)
    #allows us to use the csv as a data frame

    ageFile = ageFile.iloc[6:,]
    #eliminate the first 6 rows, which are unneccesary

    ageFile = ageFile.reset_index(drop=True)
    #resets the indices

    ageFile.columns = ['date', 'hour', 'minute', \
                    'age', 'event_label', 'total_events']
    #renames the columns so we can refer to them by their new labels

    ageFile.age = [x.strip().replace('Answer: ', '') \
                            for x in ageFile.age]
    #gets rid of each instance of "Answer: " in the age column

    ageFile.age = [x.strip().replace('11-17', '11-17 years') \
                            for x in ageFile.age]
    #renames each instance of "11-17" to "11-17 years" in the age column
    #otherwise, Excel and other programs my read this as "-6" (11-17 = -6)

    ageFile['date'].apply(str)
    ageFile['hour'].apply(str)
    ageFile['minute'].apply(str)
    #converts the date, hour, and minute columns to string (for later use)

    ageFile['time_stamp'] = ageFile['date']+' '+ageFile['hour'] + ":" + \
                        ageFile['minute']
    #creates a new column 'time_stamp' populated with the date, hour, and minute
    #columns seperated by spaces and a colon

    ageFile['time_stamp'] = pd.Series(pd.to_datetime(ageFile['time_stamp']))
    #converts the 'time_stamp' columns into a series of datetime objects

    ageFile['time_stamp'] = ageFile['time_stamp'].dt.tz_localize('US/Central')
    #tell our program that our time_stamp column comes in US/Central (CST)

    ageFile['time_stamp'] =ageFile['time_stamp'].dt.tz_convert('UTC')
    #converts to UTC, which is easier to compute with and
    #is what our data comes in

    ageFile = ageFile.drop(columns=['event_label', 'total_events','date', \
                                    'hour', 'minute'])
    #drops the event_label, total events, date, hour, and minute columns

    ageFile.reindex(columns=['time_stamp','age'])
    #shifts the order of the columns

    return ageFile
    #returns a dataframe of the age data


#the below works when you run it in command prompt with the following command:
#(first open command terminal and ensure you are in the directory where your code and input data file is)
#Type the following:
#python age_data_function.py
#OR
#python age_data_function.py -f [YOUR FILE NAME HERE]
#ex: python age_data_function.py -f age_data_google_analytics.csv

if __name__== '__main__':
    parser = argparse.ArgumentParser('data to be imported')
    parser.add_argument('-f', '--file', default= 'age_data_google_analytics.csv', help='Process some microplant data')
    args = parser.parse_args()
    cleanse_age(args.file).to_csv(r'C:\Users\achen\Desktop\Sum19FM\GitCopy\microplants_cleansing\ageFile2.csv',
               encoding='utf-8', index=False)
    #print(cleanse_age(args.file).age.head())
