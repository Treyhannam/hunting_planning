from streamlit.testing.v1 import AppTest
from pathlib import Path
import pytest


@pytest.fixture
def import_page():
    def _import_page(fname: str) -> AppTest:
        overview_page = (
            Path(__file__).parent.parent.parent / "src" / "app" / "st_pages" / fname
        )

        at = AppTest.from_file(str(overview_page))

        return at

    return _import_page


def import_page(fname: str) -> AppTest:
    overview_page = (
        Path(__file__).parent.parent.parent / "src" / "app" / "st_pages" / fname
    )

    at = AppTest.from_file(str(overview_page))

    return at
