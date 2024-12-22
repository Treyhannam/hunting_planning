import pytest
import pandas as pd


@pytest.fixture
def mock_hunter_df():
    data = {
        "GMU": [1, 2, 3],
        "Year": [2020, 2021, 2022],
        "Bulls": [10, 20, 30],
        "Cows": [5, 15, 25],
        "Calves": [2, 4, 6],
        "Total Hunters": [100, 200, 300],
        "Total Harvest": [17, 39, 61],
        "Percent Success": [17, 19.5, 20.3],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_gdf():
    data = {
        "geometry": ["POINT (1 1)", "POINT (2 2)", "POINT (3 3)"],
        "GMU": ["A", "B", "C"],
    }
    return pd.DataFrame(data)
