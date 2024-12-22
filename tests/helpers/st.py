import pytest
from streamlit.testing.v1 import AppTest
from pathlib import Path


def import_page(fname: str) -> AppTest:
    overview_page = (
        Path(__file__).parent.parent.parent / "src" / "app" / "st_pages" / fname
    )

    at = AppTest.from_file(str(overview_page))

    return at
