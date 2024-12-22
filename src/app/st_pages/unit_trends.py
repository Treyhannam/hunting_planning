import streamlit as st
from app.helpers.cache_state import get_hunting_data
from app.helpers.graphs import plot_metrics

hunter_df = get_hunting_data()

unit = st.selectbox(
    label="Select a GMU",
    options=["All"] + hunter_df.sort_values("Unit").Unit.unique().tolist(),
)

year_range = st.slider(
    label="Select Year(s)",
    min_value=hunter_df["Year"].min(),
    max_value=hunter_df["Year"].max(),
    value=(hunter_df["Year"].min(), hunter_df["Year"].max()),
    step=1,
)

st.plotly_chart(
    plot_metrics(
        hunter_df,
        ["Bulls", "Cows", "Calves"],
        unit,
        "Bulls, Cows and Calves",
        year_range,
    ),
    config={"displayModeBar": False},
)

st.plotly_chart(
    plot_metrics(
        hunter_df,
        ["Total Hunters", "Total Harvest"],
        unit,
        "Total Hunters and Total Harvest",
        year_range,
    ),
    config={"displayModeBar": False},
)

st.plotly_chart(
    plot_metrics(hunter_df, ["Percent Success"], unit, "Percent Success", year_range),
    config={"displayModeBar": False},
)
