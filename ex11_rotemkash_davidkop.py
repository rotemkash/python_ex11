"""
======================================================================
ex11
======================================================================
Writen by: Rotem kashani, ID = 209073352,   login = rotemkash
	       David Koplev, ID = 208870279 ,    login = davidkop
Program follows 11 actions from the exercise given:
Q1 - Set the seed to 745
Q2 - Read the files
Q3 - Find the percentage of men in the table of people
Q4 - Add a new column to the people table and divide it into 4 groups: 1. 0-20, 2. 20-40, 3. 40-60, 4. 60+
Q5 - Change the format of the riding time
Q6 - Take the names column from the people table, turn it into a random list and add this column to the table The bike ride
Q7 - Add the random list as a column to the riding table
Q8 - Combine the two tables into one table.
Q9 - Print how many start stations there are
Q10 - Divide the table into groups according to the starting station
Q11 -Calculate for each starting station what is the average time they rode from it, and what is the standard deviation.
"""
import pandas as pd
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import itertools

#  Question 1:
random.seed(745)

#  Question 2:
people_file = pd.read_csv("people_list.csv")
ride_file = pd.read_csv("ride_2015.csv")

#  Question 3:
males = (people_file['Sex'].value_counts(normalize=True))
print(males.filter(items=["Male"]))

#  Question 4:
df = pd.DataFrame(people_file)
current_date = pd.Timestamp.now().normalize()  # Convert to pandas.Timestamp

people_file["Date of birth"] = pd.to_datetime(people_file["Date of birth"], format='%d/%m/%Y')
people_file['Age'] = people_file['Date of birth'].apply(lambda x: relativedelta(current_date, x).years)
bins = [-1, 20, 40, 60, float('inf')]
labels = ['0-20', '20-40', '40-60', '60+']
people_file['Age Group'] = pd.cut(people_file['Age'], bins=bins, labels=labels)

#  Question 5:
ride_file['Duration (ms)'] = ride_file['Duration (ms)'].astype(int)  # Convert to integer if necessary

ride_file['Days'] = ride_file['Duration (ms)'] // (24 * 60 * 60 * 1000)  # Number of days
ride_file['Duration (ms)'] %= 24 * 60 * 60 * 1000  # Remainder after days

ride_file['Hours'] = ride_file['Duration (ms)'] // (60 * 60 * 1000)  # Number of hours
ride_file['Duration (ms)'] %= 60 * 60 * 1000  # Remainder after hours

ride_file['Minutes'] = ride_file['Duration (ms)'] // (60 * 1000)  # Number of minutes
ride_file['Duration (ms)'] %= 60 * 1000  # Remainder after minutes

ride_file['Seconds'] = ride_file['Duration (ms)'] // 1000  # Number of seconds
ride_file['Duration (ms)'] %= 1000  # Remainder after seconds

format_time = ride_file.apply(lambda row: f"{row['Days']}:{row['Hours']:02d}:{row['Minutes']:02d}:{row['Seconds']:02d}", axis=1)
print(format_time)

#  Question 6+7:
names = people_file['First Name'].tolist()
random.shuffle(names)
names = list(itertools.islice(itertools.cycle(names), len(ride_file)))
ride_file["First Name"] = names

#  Question 8:
table = pd.merge(people_file, ride_file, on='First Name')

#  Question 9:
dif_station = ride_file["Start station"].nunique()
print(dif_station)

#  Question 10:
grp = ride_file.groupby("Start station")

#  Question 11:
days = ride_file['Days'].astype('timedelta64[D]')
hours = ride_file['Hours'].astype('timedelta64[h]')
minutes = ride_file['Minutes'].astype('timedelta64[m]')
seconds = ride_file['Seconds'].astype('timedelta64[s]')

format_timedelta = days + hours + minutes + seconds
ride_file['Time'] = format_timedelta
average_time = ride_file.groupby("Start station")['Time'].mean()
print(average_time)
std_time = ride_file.groupby("Start station")['Time'].std()
print(std_time)