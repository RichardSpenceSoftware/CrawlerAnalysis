# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 09:52:10 2022

@author: Richard.Spence
"""

import pandas as pd
import matplotlib.pyplot as plt

bankframe = pd.read_csv(r'lloyds.csv',header=[0])

bankframe['Time'] = pd.to_datetime(bankframe['Time'])
bankframe['Time'] = bankframe['Time'].map(str)
bankframe = bankframe.sort_values(by="Time")

data_score = bankframe.groupby("Year", as_index=False)\
    .agg(('count', 'mean'))\
    .reset_index()

plt.plot(data_score['Year'], data_score['Likes']['mean'])
plt.title('Average Likes Rating per Year')
plt.xlabel('Time')
plt.ylabel('Likes')
plt.axhline(data_score["Likes"]['mean'].mean(), color='green', linestyle='--')
plt.show()

bankframe['Length'] = bankframe['Review'].apply(len)

bankframe.plot.scatter(x = 'Length', y = 'Likes')
plt.show()
