import pandas as pd
import streamlit as st
import plotly.express as px
import plotly


def plot_annual_data(
    geo_df: pd.DataFrame, hunting_df: pd.DataFrame, color_col: str, opacity: float
) -> plotly.graph_objs._figure.Figure:
    """
    Plots annual hunting data on a choropleth map using Plotly.

    :param geo_df: geographical data.
    :param hunting_df: hunting data.
    :param color_col: Column name to determine the color of the map.
    :param opacity: Opacity level for the map.

    :return: map plotting hunting stats on a map.
    """
    combined_df = geo_df.merge(
        hunting_df, left_on=["GMU"], right_on=["Unit"], how="left"
    )
    combined_df.reset_index(names="location", inplace=True)

    # combined_df[["Percent Success", "Total Hunters"]] = combined_df[
    #     ["Percent Success", "Total Hunters"]
    # ].fillna(0)

    fig = px.choropleth_mapbox(
        combined_df,
        geojson=combined_df.geometry,
        locations=combined_df.location,
        color=color_col,
        color_continuous_scale="emrld",  # https://plotly.com/python/builtin-colorscales/
        opacity=opacity,
        hover_data={
            "location": False,
            "GMU": True,
            "County": True,
            "Elk DAU": True,
            "Total Hunters": True,
            "Private Either Sex": True,
            "Private Female": True,
            "Public Either Sex": True,
            "Public Female": True,
        },
        mapbox_style="carto-positron",
        center={"lat": 38.9, "lon": -105.7821},
        zoom=st.session_state.map_zoom,
    )

    fig.update_layout(autosize=True)

    fig.update_layout(**st.session_state.map_layout)

    return fig


def plot_metrics(
    hunter_df: pd.DataFrame,
    metrics: list[str],
    unit: list[int],
    title: str,
    year_range: list[int],
) -> plotly.graph_objs._figure.Figure:
    """
    Plots the specified metrics for hunters over a given range of years.
    Parameters:
    :param hunter_df: hunting data.
    :param metrics: metrics to plot (e.g., ['Bulls', 'Cows', 'Calves']).
    :param unit: unit numbers to filter the data by. Use "All" to include all units.
    :param title: Title of the plot.
    :param year_range: start and end year for the plot (e.g., [2010, 2020]).

    :return: plotted metrics.
    """
    hunter_df = hunter_df.loc[
        (hunter_df.Year >= year_range[0]) & (hunter_df.Year <= year_range[1])
    ]

    if unit == "All":
        modified_hunter_df = hunter_df.groupby("Year", as_index=False).agg(
            {
                "Bulls": "sum",
                "Cows": "sum",
                "Calves": "sum",
                "Total Harvest": "sum",
                "Total Hunters": "sum",
                "Percent Success": "mean",
                "Total Rec Days": "sum",
            }
        )

        modified_hunter_df["Percent Success"] = modified_hunter_df[
            "Percent Success"
        ].round()
    else:
        modified_hunter_df = hunter_df.loc[hunter_df.Unit.isin([unit])]

    df_long = modified_hunter_df.melt(
        id_vars="Year", value_vars=metrics, var_name="Metrics", value_name="Count"
    )

    df_long["formatted_Count"] = df_long["Count"].apply(lambda x: f"{x:,}")

    fig = px.line(
        df_long,
        x="Year",
        y="Count",
        color="Metrics",
        markers=True,
        text="formatted_Count",
        color_discrete_sequence=["#005845", "#629abf", "#00b4b1"],
    )

    fig.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center"},
        title_font=dict(size=24),
        xaxis=dict(title_font=dict(size=18), tickfont=dict(size=18)),
        yaxis=dict(
            title_font=dict(size=18),
            tickfont=dict(size=18),
            tickformat=",",
        ),
    )

    fig.update_traces(textposition="top center", textfont=dict(size=16))

    fig.update_layout(autosize=True)

    fig.update_layout(**st.session_state.trend_update_layout)

    return fig
