import pandas as pd
import geopandas as gpd
import streamlit as st
import os
from pathlib import Path

# TODO create a class that caches the data and maintains session state
@st.cache_data
def get_geo_data():
    file_directory = Path(__file__).parent

    data_directory = file_directory.parent / 'data' 

    gdf = gpd.read_file(
        os.path.join(
            data_directory, 'cpw_gmu.geojson'
        )
    )

    gdf = gdf.rename(
        columns={
            'GMUID': 'GMU',
            'COUNTY': 'County',
            'ELKDAU': 'Elk DAU'
        },
    )
    
    gdf['County'] = gdf.County.apply(lambda x: '/'.join([county.title() for county in x.split()]))

    gdf['geometry'] = gdf['geometry'].apply(lambda x: x.simplify(0.001))

    return gdf


@st.cache_data
def get_hunting_data():
    file_directory = Path(__file__).parent

    data_directory = file_directory.parent / 'data' 

    df = pd.read_csv(
        os.path.join(
            data_directory, 'hunting_data.csv'
        )
    )
    
    df[['Percent Success', 'Total Hunters']] = df[['percent_success', 'total_hunters']].fillna(0)

    return df
