"""
Entry point for the app.

helpers:
    caches datasets for app to use
    creates session variables for user inputs
"""
import streamlit as st
from app.helpers.cache_state import st_sidebar, get_geo_data, get_hunting_data

st.set_page_config(layout="wide")

st_sidebar()

pages = {
    "More Information": [
        st.Page(
            st.session_state.pages_directory / "overview.py",
            title="📖Information and Submit Feedback",
        ),
    ],
    "Data Visualizations": [
        st.Page(
            st.session_state.pages_directory / "interactive_map.py",
            title="🗺️ Interactive Map",
        ),
        st.Page(
            st.session_state.pages_directory / "unit_trends.py", title="📈Unit Trends"
        ),
    ],
}

get_geo_data()

get_hunting_data()

pg = st.navigation(pages)

pg.run()
