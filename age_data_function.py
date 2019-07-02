import pandas as pd
from datetime import datetime, timedelta
import pytz
from pytz import timezone

f = open(r'G:\TimestampMatching\age_data_all.csv', encoding='utf-8')
#will recieve a file to read from the directory and encode it with utf-8

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

ageFile.to_csv(r'G:\TimestampMatching\ageFile.csv',index = False)
#creates a new csv called ageFile.csv
#will be replaced with a return statement





