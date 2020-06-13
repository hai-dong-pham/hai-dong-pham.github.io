# Title: Delivery Optimization Project
# Author: Hai Pham

import pandas as pd
pd.set_option('display.max_columns', 500)
from geopy import distance
import numpy as np


# Read the Costco warehouse data and Starbuck retail store data
costco_raw_data = pd.read_csv(r'C:\Users\Hai Pham\Desktop\Delivery Optimization Project\costco warehouse.csv', index_col = 0)
starbuck_raw_data = pd.read_csv(r'C:\Users\Hai Pham\Desktop\Delivery Optimization Project\starbuck.csv', index_col = 0)


# Data cleaning

## Filter Costco warehouses which are based in the US and remove unnecessary columns.
## The clean Costco data has 543 rows which include location of 543 Costco warehouses around the US.
costco_raw_data1 = costco_raw_data[costco_raw_data['country']=='US']
costco = costco_raw_data1.loc[:, ['stlocID', 'city', 'state', 'latitude', 'longitude']]


## Filter Starbuck stores which are based in the US and remove unncessary columns.
## Due to limited processing power, a random sample of 100 stores is then selected to conduct this project
## The clean Starbuck data has 100 rows which include location of 100 Starbuck stores around the US
starbuck_raw_data1 = starbuck_raw_data[starbuck_raw_data['Country'] == 'US']
starbuck = starbuck_raw_data1.loc[:, ['Store Number', 'City', 'State/Province', 'Latitude', 'Longitude']]

starbuck_100 = starbuck.sample(n = 100, random_state = 5)



# Construct a dictionary to store final result
final = {'Starbuck_store_id': [],
         'Costco_warehouse_id': [],
         'Distance': []}


# Use for loop to calculate the distance from each Starbuck store to all Costco warehouses.
# The final result would show the distances of 54,300 Starbuck-Costco pairs
for starbuck_id in starbuck_100['Store Number']:
    for costco_id in costco['stlocID']:
        starbuck_store = starbuck_100[starbuck_100['Store Number'] == starbuck_id]
        costco_warehouse = costco[costco['stlocID'] == costco_id]

        starbuck_store_location = (starbuck_store['Latitude'].values, starbuck_store['Longitude'].values)
        costco_warehouse_location = (costco_warehouse['latitude'].values, costco_warehouse['longitude'].values)

        dist = distance.distance(starbuck_store_location, costco_warehouse_location).miles

        final['Starbuck_store_id'].append(starbuck_id)
        final['Costco_warehouse_id'].append(costco_id)
        final['Distance'].append(dist)

# Sort the final output into ascending order of distance to get the Costco warehouse - Starbuck store pair
# with the lowest distance, leading to 100 pairs 
final_dataframe = pd.DataFrame(final)

final_dataframe = final_dataframe.sort_values(by=['Starbuck_store_id', 'Distance'], ascending=True)
final_dataframe = final_dataframe.groupby('Starbuck_store_id').head(1)

# Write the final output to a csv file
final_dataframe.to_csv('final.csv')




