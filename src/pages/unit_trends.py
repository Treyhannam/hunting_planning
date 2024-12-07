import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
from st_helpers import get_hunting_data, st_sidebar
from graphing import plot_metrics

st.set_page_config(layout="wide")

st_sidebar()

hunter_df = get_hunting_data()

unit = st.selectbox(
    label="Select a GMU",
    options=['All'] + hunter_df.sort_values('Unit').Unit.unique().tolist() 
)

year_range = st.slider(
        label=f'Select Year(s)',
        min_value=hunter_df['Year'].min(),
        max_value=hunter_df['Year'].max(),
        value=(hunter_df['Year'].min(), hunter_df['Year'].max()),
        step=1
    )

st.plotly_chart(
    plot_metrics(hunter_df, ['Bulls', 'Cows', 'Calves'], unit, 'Bulls, Cows and Calves', year_range),
    config={'displayModeBar': False}
)

st.plotly_chart(
    plot_metrics(hunter_df, ['Total Hunters', "Total Harvest"], unit, 'Total Hunters and Total Harvest', year_range),
    config={'displayModeBar': False}
)

st.plotly_chart(
    plot_metrics(hunter_df, ['Percent Success'], unit, 'Percent Success', year_range),
    config={'displayModeBar': False}
)