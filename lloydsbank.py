# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 09:17:05 2022

@author: Richard.Spence
"""

import pandas as pd
import matplotlib.pyplot as plt

lloydsframe = pd.read_csv(r'lloyds.csv',header=[0])

lloydsframe['Time'] = pd.to_datetime(lloydsframe['Time'])
lloydsframe['Time'] = lloydsframe['Time'].map(str)
lloydsframe = lloydsframe.sort_values(by="Time")

data_score = lloydsframe.groupby("Year", as_index=False)\
    .agg(('count', 'mean'))\
    .reset_index()

plt.plot(data_score['Year'], data_score['Likes']['mean'])
plt.title('Average Likes Rating per Year')
plt.xlabel('Time')
plt.ylabel('Likes')
plt.axhline(data_score["Likes"]['mean'].mean(), color='green', linestyle='--')
plt.show()

data_score = lloydsframe.groupby("Location", as_index=False)\
    .agg(('count', 'mean'))\
    .reset_index()
data_score.plot.bar(x="Location", y='Likes', rot=70, title="Average Score");

lloydsframe['Length'] = lloydsframe['Review'].apply(len)

lloydsframe.plot.scatter(x = 'Length', y = 'Likes')
plt.show()

lloydsframe['Anonymous'] = lloydsframe['AUTHOR'].str.contains('Anonymous', regex=False)
#lloydsframe['Anonymous'] = pd.np.where(lloydsframe.AUTHOR.str.contains("Anonymous"), 1)

anonframe = lloydsframe.groupby("Anonymous").agg({'RATING': 'mean'}).reset_index()
transposed = anonframe.T
new_header = transposed.iloc[0] #Get the first row for the header
transposed = transposed[1:] #Take the data less the header row
transposed.columns = new_header #Set the header row as the df header

anonframe.plot.bar(x="Anonymous", y="RATING", rot=70, title="Average Score");
