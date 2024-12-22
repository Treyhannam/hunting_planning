"""
Functions to cache and retrieve geospatial and hunting data,
as well as configure the Streamlit sidebar for multi page use.
"""
import os
from pathlib import Path
import pandas as pd
import geopandas as gpd
import streamlit as st


@st.cache_data
def get_geo_data() -> gpd.GeoDataFrame:
    """loads geographic data from a GeoJSON file.

    :returns: df for plotting on a map
    """
    file_directory = Path(__file__).parent

    asset_directory = file_directory.parent / "assets" / "data"

    gdf = gpd.read_file(os.path.join(asset_directory, "cpw_gmu.geojson"))

    gdf = gdf.rename(
        columns={"GMUID": "GMU", "COUNTY": "County", "ELKDAU": "Elk DAU"},
    )

    gdf["County"] = gdf.County.apply(
        lambda x: "/".join([county.title() for county in x.split()])
    )

    gdf["geometry"] = gdf["geometry"].apply(lambda x: x.simplify(0.001))

    return gdf


@st.cache_data
def get_hunting_data() -> pd.DataFrame:
    """loads hunting data from a csv file.

    :returns: df for plotting on a hunting stats
    """
    file_directory = Path(__file__).parent

    asset_directory = file_directory.parent / "assets" / "data"

    df = pd.read_csv(os.path.join(asset_directory, "hunting_data.csv"))

    df.columns = [col.replace("_", " ").title() for col in df.columns]

    df[["Percent Success", "Total Hunters"]] = df[
        ["Percent Success", "Total Hunters"]
    ].fillna(0)

    return df


def st_sidebar():
    """
    Configures the sidebar in a Streamlit application to toggle between mobile
    and desktop views. This function checks if the 'is_mobile' key exists in
    the Streamlit session state. If not, it initializes it to True. It then
    creates a toggle button in the sidebar to allow the user to specify if they
    are on a mobile device. Depending on the user's choice, it adjusts various
    session state parameters to optimize the layout and appearance of the
    application for mobile or desktop viewing.

    Session State Variables:
    - is_mobile (bool): Indicates if the user is on a mobile device.
    - map_zoom (int): Zoom level for the map display.
    - map_layout (dict): Layout settings for the map display.
    - trend_font (int): Font size for trend display.
    - trend_start_year (int): Starting year for trend data.
    - trend_update_layout (dict): Layout settings for trend display.
    """
    if "pages_directory" not in st.session_state.keys():
        app_directory = Path(__file__).parent.parent

        st.session_state.pages_directory = app_directory / "st_pages"

    if "is_mobile" not in st.session_state.keys():
        st.session_state.is_mobile = True

    with st.sidebar:
        status = st.toggle(
            "Are you on a mobile device?", value=st.session_state.is_mobile
        )
        st.write("This will change the format of the website for easier viewing.")

        st.session_state.is_mobile = status

    if status:
        st.session_state.map_zoom = 5
        st.session_state.map_layout = {
            "coloraxis_showscale": False,
        }

        st.session_state.trend_font = 16
        st.session_state.trend_start_year = 17
        st.session_state.trend_update_layout = {
            "margin": dict(t=30),
            "yaxis_title": None,
            "height": 600,
            "legend": dict(yanchor="top", y=-0.1, xanchor="left", x=0.0),
        }

    else:
        st.session_state.map_zoom = 7
        st.session_state.map_layout = {"coloraxis_showscale": True, "height": 1080}

        st.session_state.trend_font = 20
        st.session_state.trend_start_year = 2006
        st.session_state.trend_update_layout = {
            "title_y": 1,
        }
