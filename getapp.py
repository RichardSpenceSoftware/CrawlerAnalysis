# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 09:31:45 2022

@author: Richard.Spence
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

getframe = pd.read_csv(r'test.csv',header=[0])
getframe['Date'] = pd.to_datetime(getframe['Date'])
getframe = getframe.sort_values(by="Date")
getframe = getframe.head(n=3)
getframe['Year'] = getframe['Date'].dt.year
getframe['Package'] = np.random.randint(1, 5, getframe.shape[0])
getframe['Customer'] = np.random.randint(1, 5, getframe.shape[0])
getframe['Overall'] = np.random.randint(1, 5, getframe.shape[0])
getframe['Broadband'] = np.random.randint(1, 5, getframe.shape[0])

getframe = getframe.groupby('Year').agg({'Package': 'mean','Customer': 'mean','Overall': 'mean','Broadband': 'mean'}).reset_index()

plt.plot(getframe['Year'], getframe['Package'])
plt.plot(getframe['Year'], getframe['Customer'])
plt.plot(getframe['Year'], getframe['Broadband'])
plt.plot(getframe['Year'], getframe['Overall'])
plt.title('Average Star Rating per Year')
plt.xlabel('Date')
plt.ylabel('Different Ratings')
plt.show()

getframe['Location'] = ['United States','China','China']

data_score = getframe.groupby("Location", as_index=False)\
    .agg(('count', 'mean'))\
    .reset_index()
data_score.plot.bar(x="Location", y='Star Rating', rot=70, title="Average Score");
