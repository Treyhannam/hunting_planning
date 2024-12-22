""" Turns PDFs into CSV files

Start:
    2006 Elk Harvest, Hunters and Recreation Days for All Rifle Seasons 
     Total Total Percent Total 
Unit  Bulls Cows Calves Harvest Hunters Success Rec. Days 
 69 22 31 0 53 251 21 1,041
 ... 
 691 0 9 2 11 81 14 295 

Finish:
    

"""
import os
import sys
import glob
import logging
import pandas as pd
import PyPDF2
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(filename)s] [%(funcName)20s()] [%(levelname)s] - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


def parse_rows(pdf_page_data: list) -> list[list[str]]:
    """Each PDF page has the data sperated by new lines. Once a page is split by
    new lines ('\n') then iterate through each row to see if it contains data about
    a GMU. This follows a pattern of having eight integer elements.

    Example:
    >>> pdf_page_data = ['1, 2, 3, 4, 5, 6, 7, 8']
    >>> gmu_list = parse_rows(pdf_page_data)
    >>> gmu_list
    [['1', '2', '3', '4', '5', '6', '7', '8']]

    :param pdf_page_data: list of data from the PDF page

    :return: a list of lists containing GMU data
    """
    gmu_data = []
    for row in pdf_page_data:
        split_row = row.replace(",", "").split(" ")

        no_empty_elt = [elt for elt in split_row if len(elt) > 0]

        list_of_numbers = all(elt.isdigit() for elt in no_empty_elt)

        number_of_elt = len(no_empty_elt)

        if list_of_numbers and number_of_elt == 8:
            gmu_data.append(no_empty_elt)
        elif number_of_elt == 8 and no_empty_elt[0] == "total":
            break

    return gmu_data


def extract_archery_data(pdf_page: PyPDF2._page.PageObject):
    page_text = pdf_page.extract_text().lower()

    if (archery_str_index := page_text.find("archery")) != -1:
        archery_page_section = page_text[archery_str_index::]

        archery_data = archery_page_section.split("\n")

    else:
        archery_data = None

    return archery_data


def parse_pdf_archery_data(pdf_reader) -> pd.DataFrame:
    """The data is in a table format within the pdf and each row in
    the table represents a game unit. The rows come in a patter of eight
    different numbers that are the values for 8 different columns. If a row
    is parsed and does not have 8 different numbers then it is not the data
    we are looking for.

    Sample Page:
        2006 Elk Harvest, Hunters and Recreation Days for All Rifle Seasons
        Total Total Percent Total
    Unit  Bulls Cows Calves Harvest Hunters Success Rec. Days
    69 22 31 0 53 251 21 1,041
    ...
    691 0 9 2 11 81 14 295

    :param pdf: a pdf of the hunting data from CPW

    :return: pdf data as a pandas dataframe.
    """
    all_rows = []
    for pdf_page in pdf_reader.pages:
        archery_data = extract_archery_data(pdf_page)

        if archery_data:
            all_rows += parse_rows(archery_data)

    archery_df = pd.DataFrame(
        data=all_rows,
        columns=[
            "unit",
            "bulls",
            "cows",
            "calves",
            "total_harvest",
            "total_hunters",
            "percent_success",
            "total_rec_days",
        ],
    ).astype(int)

    return archery_df


def pdf_to_csv():
    file_directory = Path(__file__).parent

    pdf_directory = file_directory.parent / "pdf" / "harvest"

    pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))

    all_data = []
    for pdf_file in pdf_files:
        logger.info("Processing file %s: ", pdf_file)

        reader = PyPDF2.PdfReader(pdf_file)

        df = parse_pdf_archery_data(reader)

        year = pdf_file.split("\\")[-1][0:4]

        df["year"] = int(year)

        all_data.append(df)

        logger.info("Number of GMUs found %s: ", len(df))

    pd.concat(all_data).to_csv("data//hunting_data.csv", index=False)


if __name__ == "__main__":
    pdf_to_csv()
