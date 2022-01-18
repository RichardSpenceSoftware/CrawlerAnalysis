# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 14:14:31 2022

@author: Richard.Spence
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

btframe = pd.read_csv(r'test.csv',header=[0])
btframe['Date'] = pd.to_datetime(btframe['Date'])
btframe = btframe.sort_values(by="Date")
btframe['Year'] = btframe['Date'].dt.year
btframe['Package'] = np.random.randint(1, 5, btframe.shape[0])
btframe['Customer'] = np.random.randint(1, 5, btframe.shape[0])
btframe['Overall'] = np.random.randint(1, 5, btframe.shape[0])
btframe['Broadband'] = np.random.randint(1, 5, btframe.shape[0])

btframe = btframe.groupby('Year').agg({'Package': 'mean','Customer': 'mean','Overall': 'mean','Broadband': 'mean'}).reset_index()

plt.plot(btframe['Year'], btframe['Package'])
plt.plot(btframe['Year'], btframe['Customer'])
plt.plot(btframe['Year'], btframe['Broadband'])
plt.plot(btframe['Year'], btframe['Overall'])
plt.title('Average Star Rating per Year')
plt.xlabel('Date')
plt.ylabel('Different Ratings')
plt.show()