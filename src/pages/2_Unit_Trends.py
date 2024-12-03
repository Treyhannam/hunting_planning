import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
from st_helpers import get_hunting_data

st.set_page_config(layout="wide")

def plot_metrics(hunter_df: pd.DataFrame, metrics: list[str], unit: list[int], title: str, year_range: list[int]):
    """
    """
    hunter_df = hunter_df.loc[
        (hunter_df.year >= year_range[0])
        & (hunter_df.year <= year_range[1])
    ]

    if unit == 'All':
        modified_hunter_df = hunter_df.groupby('year', as_index=False).agg(
            {
                "bulls": "sum",
                "cows": "sum",
                "calves": "sum",
                "total_harvest": "sum",
                "total_hunters": "sum",
                "percent_success": "mean",
                "total_rec_days": "sum"
            }
        )

        modified_hunter_df["percent_success"] = modified_hunter_df["percent_success"].round()
    else:
        modified_hunter_df = hunter_df.loc[hunter_df.unit.isin([unit])]

    df_long = modified_hunter_df.melt(
        id_vars='year',
        value_vars=metrics,
        var_name='Metrics',
        value_name='Count'
    )

    fig = px.line(
        df_long,
        x='year',
        y='Count',
        color='Metrics',
        markers=True,
        text='Count',
        color_discrete_sequence=['#005845', '#629abf', '#00b4b1']
    )

    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Centers the title
            'xanchor': 'center'  # Ensures proper anchoring
        },
        title_font=dict(
            size=24
        ),
        xaxis=dict(
            title_font=dict(
                size=18  
            ),
            tickfont=dict(
                size=18  
            )
        ),
        yaxis=dict(
            title_font=dict(
                size=18
            ),
            tickfont=dict(
                size=18  
            )
        )
    )
    
    fig.update_traces(
        textposition='top center',
        textfont=dict(
            size=14
        )    
    )

    return fig

hunter_df = get_hunting_data()

unit = st.selectbox(
    label="Select a GMU",
    options=['All'] + hunter_df.sort_values('unit').unit.unique().tolist() 
)
st.write(hunter_df['year'].min())

year_range = st.slider(
        label=f'Select Year(s)',
        min_value=hunter_df['year'].min(),
        max_value=hunter_df['year'].max(),
        value=(hunter_df['year'].min(), hunter_df['year'].max()),
        step=1
    )

st.plotly_chart(
    plot_metrics(hunter_df, ['bulls', 'cows', 'calves'], unit, 'Bulls, Cows and Calves', year_range)
)

st.plotly_chart(
    plot_metrics(hunter_df, ['total_hunters', "total_harvest"], unit, 'Total Hunters and Total Harvest', year_range)
)

st.plotly_chart(
    plot_metrics(hunter_df, ['percent_success'], unit, 'Percent Success', year_range),
)