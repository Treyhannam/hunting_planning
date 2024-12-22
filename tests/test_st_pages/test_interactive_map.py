import pytest
from unittest.mock import patch
import plotly.graph_objects as go
from tests.helpers.st import import_page
from tests.helpers.mock_fixtures import mock_hunter_df, mock_gdf

@patch('app.helpers.cache_state.get_hunting_data')
@patch('app.helpers.cache_state.get_geo_data')
@patch('app.helpers.graphs.plot_annual_data')
def test_slider_percent_success(mock_plot_annual_data, mock_get_geo_data, mock_get_hunting_data, mock_gdf, mock_hunter_df):
    mock_get_geo_data.return_value = mock_gdf
    mock_get_hunting_data.return_value = mock_hunter_df
    
    mock_fig = go.Figure()
    mock_plot_annual_data.return_value = mock_fig
    
    at = import_page('interactive_map.py').run()

    at.selectbox[0].set_value('Percent Success').run()

    assert at.slider[0].value == (0, 100)


@patch('app.helpers.cache_state.get_hunting_data')
@patch('app.helpers.cache_state.get_geo_data')
@patch('app.helpers.graphs.plot_annual_data')
def test_slider_not_percent_success(mock_plot_annual_data, mock_get_geo_data, mock_get_hunting_data, mock_gdf, mock_hunter_df):
    mock_get_geo_data.return_value = mock_gdf
    mock_get_hunting_data.return_value = mock_hunter_df
    
    mock_fig = go.Figure()
    mock_plot_annual_data.return_value = mock_fig
    
    at = import_page('interactive_map.py').run()

    at.selectbox[0].set_value('Total Hunters').run()

    assert at.slider[0].value == (0, 300)
