import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
from st_helpers import get_geo_data, get_hunting_data

st.set_page_config(layout="wide")

st.title("Elk Archery Percent Success and Number of Hunters")


def plot_annual_data(geo_df: pd.DataFrame, hunting_df: pd.DataFrame, color_col: str):
    """
    """
    combined_df = geo_df.merge(
        hunting_df,
        left_on=['GMU'],
        right_on=['unit'],
        how='inner'
    )

    combined_df.reset_index(names='locationt', inplace=True)

    combined_df[['Percent Success', 'Total Hunters']] = combined_df[['percent_success', 'total_hunters']].fillna(0)

    fig = px.choropleth_mapbox(
        combined_df,
        geojson=combined_df.geometry,
        locations=combined_df.locationt, 
        color= color_col,
        color_continuous_scale='emrld',  # https://plotly.com/python/builtin-colorscales/
        hover_data={
            'locationt': False,
            'GMU': True,
            'County': True,
            'Elk DAU': True,
            'Total Hunters': True  
        },
        mapbox_style="carto-positron", 
        center={"lat": 38.9, "lon": -105.7821},  
        zoom=7
    )

    fig.update_layout(
        title="Colorado Game Management Units",
        title_x=0.5,
        margin={"r":0, "t":40, "l":0, "b":0}
    )

    fig.update_layout(
        height=1080,
        width=1080,
        autosize=True
        )

    return fig

gdf = get_geo_data()

hunter_df = get_hunting_data()

with st.container():
    col1, col2, col3 = st.columns(3)

    metric = col1.selectbox(
        label='Pick a Metric',
        options=('Percent Success', 'Total Hunters')
    )

    year = col2.selectbox(
        label='Pick a year',
        options=hunter_df.year.unique(),
        key='maplot_year_selectbox'
    )

    if metric == 'Percent Success':
        metric_range = col3.slider(
            label=f'Select range for {metric}',
            value=(0, 100)
        )
    elif metric == 'Total Hunters':
        metric_range = col3.slider(
            label=f'Select range for {metric}',
            value=(0, hunter_df['Total Hunters'].max())
        )

    filtered_hunter_df = hunter_df.loc[
        (hunter_df.year == year)
        & (hunter_df[metric] >= metric_range[0])
        & (hunter_df[metric] <= metric_range[1])
    ].copy()

    # TODO make the range selector remain consistent for all years, changes a lot
    st.plotly_chart(
        plot_annual_data(gdf, filtered_hunter_df, metric),
        use_container_width=True,
    )