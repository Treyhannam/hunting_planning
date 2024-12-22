import os
from pathlib import Path
import streamlit as st
from app.helpers.cache_state import st_sidebar, get_geo_data, get_hunting_data

if "pages_directory" not in st.session_state.keys():
    app_directory = Path(__file__).parent

    st.session_state.pages_directory = app_directory / 'st_pages'

# st.write(st.session_state.pages_directory)

pages = {
    "More Information": [
        st.Page(
            st.session_state.pages_directory / "overview.py",
            title="📖Information and Submit Feedback"
        ),
    ],
    "Data Visualizations": [
        st.Page(
            st.session_state.pages_directory / "interactive_map.py",
            title="🗺️ Interactive Map"
        ),
        st.Page(
            st.session_state.pages_directory / "unit_trends.py",
            title="📈Unit Trends"
            ),
    ],
}

st.set_page_config(layout="wide")

st_sidebar()

get_geo_data()

get_hunting_data()

pg = st.navigation(pages)

pg.run()