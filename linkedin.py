# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 16:28:53 2022

@author: Richard.Spence
"""
import pandas as pd
import matplotlib.pyplot as plt

linkdinframe = pd.read_csv(r'linkedin.csv',header=[0])
linkdinframe['Likes'] = [1,2,3]
linkdinframe['Time'] = linkdinframe['Time'].map(str)
linkdinframe['Time'] = linkdinframe['Time'].str.replace(r"[a-zA-Z]",'')
linkdinframe['Time'] = ['3 Jan 2021','4 Jan 2021','7 Jan 2021']
linkdinframe['Time'] = pd.to_datetime(linkdinframe['Time'])
linkdinframe = linkdinframe.sort_values(by="Time")

data_score = linkdinframe.groupby("Time", as_index=False)\
    .agg(('count', 'mean'))\
    .reset_index()

plt.plot(data_score['Time'], data_score['Likes']['mean'])
plt.title('Average Likes Rating per Year')
plt.xlabel('Time')
plt.ylabel('Likes')
plt.axhline(data_score["Likes"]['mean'].mean(), color='green', linestyle='--')
plt.show()
linkdinframe['Location'] = ['United States','China','China']

data_score = linkdinframe.groupby("Location", as_index=False)\
    .agg(('count', 'mean'))\
    .reset_index()
data_score.plot.bar(x="Location", y='Likes', rot=70, title="Average Score");

linkdinframe['Length'] = linkdinframe['Comment'].apply(len)

linkdinframe.plot.scatter(x = 'Length', y = 'Likes')
plt.show()