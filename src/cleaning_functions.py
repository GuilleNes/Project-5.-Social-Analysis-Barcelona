import pandas as pd
import numpy as np
import os
import glob

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json



# Function for droping columns of a dataframe

def drop_column(df_,column):
    return  df_.drop(column, axis = 1, inplace = True)

# Function for droping row of a dataframe with a certain value

def drop_value(df_, column, value):
    df_ = df_.loc[df_[column]!= value]
    df_.reset_index(drop=True, inplace=True)
    return df_

# Droping the rows with certain values contained

def drop_rows(df_, column, list_of_values):
    for i in df_[column]:
        if i in list_of_values:
            df_.drop(df_.loc[df_[column]==i].index, inplace = True)
    df_.reset_index(drop=True, inplace=True)
    return df_

# Droping columns or rows with nan values

def drop_nan(df_, ax):
    df_.dropna(axis = ax, inplace = True)
    df_.reset_index(drop=True, inplace=True)
    return df_

# Deleting the rows with that does not contain certain values

def keep_rows(df_, column, list_of_values):
    for i in df_[column]:
        if i in list_of_values:
            df_.drop(df_.loc[df_[column]!=i].index, inplace = True)
    df_.reset_index(drop=True, inplace=True)
    return df_

# With this function we join different datasets in csv format

def concatenate_csv (dir_name, file_name):
    # Store the current directory to a variable
    current_dir = os.getcwd()
    # Set working directory to where files are located
    os.chdir(f'{dir_name}')
    # Match the pattern (‘csv’) and save the list of file names in the ‘all_filenames’ variable
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    # Combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # Export to csv
    combined_csv.to_csv(f'{file_name}', index=False, encoding='utf-8-sig')
    # Set working directory back to original 
    os.chdir(current_dir)
    return f'files combined!'

# Joining columns with nan values

def merge_columns(df_, column1, column2):
    df_[column1] = df_[column1].fillna(df_[column2])
    df_.drop(column2, axis = 1, inplace = True)
    return 

# Function for getting years on each row and setting the column as the new index

def set_years(df_, new_column, starting_year):
    df_[new_column]=np.divmod(np.arange(df_.shape[0]),10)[0]+starting_year
    df_.set_index(new_column, inplace = True)
    return df_

# We drop the values with a total values of less than a given number

def drop_value_less(df_, column, value):
    counts = df_[column].value_counts()
    return df_[~df_[column].isin(counts[counts < value].index)]
        
# Deleting the rows of the bus dataframe with stops out of Barcelona limits

def get_bcn_stops(geojson, df_):
    with open(geojson, encoding='utf-8') as geojson:
        geo_limits = json.load(geojson)
    polygon = Polygon(geo_limits["features"][0]["geometry"]["coordinates"][0][0])
    df_["polygon"] = df_.apply(lambda row: polygon.contains(Point(row.longitude, row.latitude)), axis=1)
    df_ = df_.drop(df_[~df_["polygon"]].index)
    df_.drop(["polygon"], axis = 1, inplace = True)
    df_.reset_index(drop=True, inplace=True)
    return df_



