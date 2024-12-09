import streamlit as st

pages = {
    "More Information": [
        st.Page("st_pages\\overview.py", title="📖Information and Submit Feedback"),
    ],
    "Data Visualizations": [
        st.Page("st_pages\\interactive_map.py", title="🗺️ Interactive Map"),
        st.Page("st_pages\\unit_trends.py", title="📈Unit Trends"),
    ],
}

pg = st.navigation(pages)
pg.run()