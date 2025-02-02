import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from app.cleaning.harvest import parse_rows, extract_archery_data


def test_parse_rows():
    gmu_pdf_row_list = [
        "2 5 0 0 5 10 50 115",
        " 31 30 11 0 41 284 14 1,772 ",
        "total 1 2 3 4 5 6 7",
        "1, 2, 3, 4, 5, 6, 7, 8",
    ]

    parsed_list_of_lists = parse_rows(gmu_pdf_row_list)

    assert parsed_list_of_lists[0] == ["2", "5", "0", "0", "5", "10", "50", "115"]
    assert parsed_list_of_lists[1] == ["31", "30", "11", "0", "41", "284", "14", "1772"]


def test_extract_archery_data():
    archery_mid_page_path = (
        Path(__file__).parent.parent / "helpers" / "archery_mid_page.txt"
    )
    with archery_mid_page_path.open("r") as file:
        archery_mid_page = file.read()

    mock_page = MagicMock()
    mock_page.extract_text.return_value = archery_mid_page

    data = extract_archery_data(mock_page)

    assert data == [
        "archery seasons  ",
        "     total total percent total ",
        "unit  bulls cows calves harvest hunters success rec. days ",
        " 1 1 0 0 1 6 17 29 ",
    ]
