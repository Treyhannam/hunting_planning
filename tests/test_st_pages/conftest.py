from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest


def import_page(fname: str) -> AppTest:
    page = Path(__file__).parent.parent.parent / "src" / "app" / "st_pages" / fname

    at = AppTest.from_file(str(page))

    return at.run()


@pytest.fixture
def overview_page():
    yield import_page("overview.py")
