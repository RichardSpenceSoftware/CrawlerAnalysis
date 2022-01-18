# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 09:28:08 2022

@author: Richard.Spence
"""

import pandas as pd
import matplotlib.pyplot as plt

amazonframe = pd.read_csv(r'test.csv',header=[0])
amazonframe['Date'] = pd.to_datetime(amazonframe['Date'])
amazonframe = amazonframe.sort_values(by="Date")
amazonframe['Year'] = amazonframe['Date'].dt.year

data_score = amazonframe.groupby("Year", as_index=False)\
    .agg(('count', 'mean'))\
    .reset_index()

plt.plot(data_score['Year'], data_score['Star']['mean'])
plt.title('Average Star Rating per Year')
plt.xlabel('Date')
plt.ylabel('Star')
plt.axhline(data_score["Star"]['mean'].mean(), color='green', linestyle='--')
plt.show()

amazonframe['Length'] = amazonframe['Review'].apply(len)

amazonframe.plot.scatter(x = 'Length', y = 'Star')
plt.show()
