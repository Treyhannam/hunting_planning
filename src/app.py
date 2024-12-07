import streamlit as st

pages = {
    "More Information": [
        st.Page("pages\\overview.py", title="📖Information and Submit Feedback"),
    ],
    "Data Visualizations": [
        st.Page("pages\\interactive_map.py", title="🗺️ Interactive Map"),
        st.Page("pages\\unit_trends.py", title="📈Unit Trends"),
    ],
}

pg = st.navigation(pages)
pg.run()