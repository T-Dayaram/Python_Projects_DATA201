#Troy's project for LaGuardia College Data Analytics course
#Objective; Analyze student test performance
# 1. Pick a school in the dataset as our initial point (our control)
# 2. Pick a feature/measure/score
# 3. compare at least one school to another school (individual or district or even borough)
# 4. include descriptive statistics, at least one cleaning tast and one visualization
# 5. Sum it up at the end briefly
# copy the following https://raw.githubusercontent.com/CunyLaguardiaDataAnalytics/datasets/master/2014-15_To_2016-17_School-_Level_NYC_Regents_Report_For_All_Variables.csv

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("https://raw.githubusercontent.com/CunyLaguardiaDataAnalytics/datasets/master/2014-15_To_2016-17_School-_Level_NYC_Regents_Report_For_All_Variables.csv")

schools = pd.DataFrame(df)
schools.info()
#Here's an overview of the data we will be looking at

#Using the first ten rows, let's see what the table looks like
schools.head(10)
#We have the column "school name" so we can build off of that

#Which schools are we able to choose from?
#There are a lot of schools so in order to list all of them, we need a 'for' loop
for school in schools['School Name'].unique():
    print(school)

#I am biased so I will pick my old high school; Queens Collegiate
#And I will use the most recent school year available in the data
#schools_qc = schools[schools['School Name'] == 'Queens Collegiate: A College Board School']
schools_qc = schools[schools['School Name'].str.contains('Queens Collegiate')]
schools_qc

#Lets restrict everything to the year 2017
schools_qc_2017 = schools_qc[schools_qc['Year'].astype('str').str.contains('2017')]
schools_qc_2017

#Time to clean the data. First we check for null rows
schools_qc_2017.dropna()

#15 rows with no data. Let's get rid of them
schools_qc_2017 = schools_qc_2017.dropna(how='any', axis = 0)
schools_qc_2017.info()

#Lets see the average test scores
for scores in schools_qc_2017['Mean Score'].unique():
  print(scores)

#Theres a value simply called s in here. Let's drop that row
schools_qc_2017 = schools_qc_2017[schools_qc_2017['Mean Score'] != 's'].copy()
#And run it again
for scores in schools_qc_2017['Mean Score'].unique():
  print(scores)

schools_qc_2017['Mean Score'] = schools_qc_2017['Mean Score'].astype(float)
schools_qc_2017 = schools_qc_2017[(schools_qc_2017['Mean Score'] > 70)]
schools_qc_2017.sort_values(by='Mean Score')

#Lets do a visualization for Queens Collegiate's test scores
schools_qc_2017.plot.scatter(y='Regents Exam', x='Mean Score')

#Let's compare the average test scores of Queens Collegiate with other schools
#First we check the list of unique scores
for school in schools['Mean Score'].unique():
    print(school)

#This will require a little more cleaning. Which is something we didn't think about when we were first seaching through this data
schools = schools[schools['Mean Score'] != 's'].copy()
#Next let's restrict it to other secondary schools
schools = schools[schools['School Level'] == 'Secondary School']
#I will also restrict the data to 2017
schools = schools[schools['Year'].astype('str').str.contains('2017')]

#Time to convert the Mean Score column from merely an object into a floating value
schools['Mean Score'] = schools['Mean Score'].astype(float)

#Now we can see the average Regents test scores across all the schools
schools = schools[(schools['Mean Score'] > 70)]
schools.sort_values(by='Mean Score')

#Let's put each school into their own data and find the average test score of each school. Including my own
schools_average = schools.groupby('School Name')['Mean Score'].mean()
pd.set_option('display.max_rows', None)
schools_average

#Lets visualize all of the schools test score averages
plt.figure(figsize=(5,5))
plt.hist(schools_average, density= True)
plt.show()

"""**Conclusion**

---

My alma matter and their test scores are admirable, but when compared to the test scores of varous schools around the area, it's not the most stellar. In the grand scheme of this data, my school is pretty average.
"""