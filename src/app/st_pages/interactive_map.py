import streamlit as st
from app.helpers.cache_state import get_geo_data, get_hunting_data
from app.helpers.graphs import plot_annual_data

st.title("Elk Archery Percent Success and Number of Hunters")

gdf = get_geo_data()

hunter_df = get_hunting_data()

with st.expander("More information about the map"):
    st.write(
        """
        The map below is each of Colorado's Game management Unit (GMU) plotted. For a given unit CPW collects
    metrics related to hunting such as number of hunters present, elk harvested, etc. You can select a metric
    and it will be plotted on the map. The darker a GMU the more of a given metric. Example if you select 
    the metric "Total Hunters", units with the darkest color had the most hunters for a given year.

    If a GMU is not plotted then there is no data available for the metric and filters selection.
    """
    )

with st.container():
    col1, col2 = st.columns(2)

    metric = col1.selectbox(
        label="Pick a Metric",
        options=(
            "Percent Success",
            "Total Hunters",
            "Bulls",
            "Cows",
            "Calves",
            "Total Harvest",
            "Total Rec Days",
        ),
    )

    year = col1.selectbox(
        label="Pick a year",
        options=hunter_df.Year.unique(),
        key="maplot_year_selectbox",
    )

    otc_options = [
        "Private Either Sex",
        "Private Female",
        "Public Either Sex",
        "Public Female",
        "No Over the Counter",
    ]

    otc = col1.multiselect(
        "Choose to Display type of OTC Units or non OTC Units",
        options=otc_options,
        default=otc_options,
        placeholder="Choosing none is the same as choosing all",
    )

    opacity_str = col2.selectbox(
        label="Choose Plot Opacity", options=("25%", "50%", "75%", "100%"), index=3
    )

    opacity_float = float(int(opacity_str.replace("%", "")) / 100)

    if metric == "Percent Success":
        metric_range = col2.slider(label=f"Select range for {metric}", value=(0, 100))
    else:
        metric_range = col2.slider(
            label=f"Select range for {metric}", value=(0, hunter_df[metric].max())
        )

    filtered_hunter_df = hunter_df.loc[
        (hunter_df.Year == year)
        & (hunter_df[metric] >= metric_range[0])
        & (hunter_df[metric] <= metric_range[1])
        & (
            (hunter_df["Private Either Sex"] == ("Private Either Sex" in otc))
            & (hunter_df["Private Female"] == ("Private Female" in otc))
            & (hunter_df["Public Either Sex"] == ("Public Either Sex" in otc))
            & (hunter_df["Public Female"] == ("Public Female" in otc))
            | (hunter_df["No Over The Counter"] == ("No Over The Counter" in otc))
        )
    ].copy()

    st.session_state.fig = plot_annual_data(
        gdf, filtered_hunter_df, metric, opacity_float
    )

    with st.container():
        st.plotly_chart(
            st.session_state.fig,
            use_container_width=True,
        )
