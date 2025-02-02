import re
import sys
import logging
from pathlib import Path
import numpy as np
import pandas as pd
from pypdf import PdfReader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(filename)s] [%(funcName)20s()] [%(levelname)s] - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


class DrawReportParser:
    def __init__(self, pdf_reader):
        self.all_data_dict = {
            "hunt_code": [],
            "list_code": [],
            "adult_res_draw_at": [],
            "adult_nonrest_draw_at": [],
            "youth_res_draw_at": [],
            "youth_nonrest_draw_at": [],
            "landowner_unrestr_draw_at": [],
            "landowner_restr_draw_at": [],
            "final_adult_res_draw_at": [],
            "final_adult_nonrest_draw_at": [],
            "final_youth_res_draw_at": [],
            "final_youth_nonrest_draw_at": [],
            "final_landowner_unrestr_draw_at": [],
            "final_landowner_restr_draw_at": [],
        }
        self.reader = pdf_reader
        self.max_len = 0
        self.code_cols = ["hunt_code", "list_code"]
        self.dra_cols = [
            "adult_res_draw_at",
            "adult_nonrest_draw_at",
            "youth_res_draw_at",
            "youth_nonrest_draw_at",
            "landowner_unrestr_draw_at",
            "landowner_restr_draw_at",
        ]
        self.final_dra_cols = [
            "final_adult_res_draw_at",
            "final_adult_nonrest_draw_at",
            "final_youth_res_draw_at",
            "final_youth_nonrest_draw_at",
            "final_landowner_unrestr_draw_at",
            "final_landowner_restr_draw_at",
        ]
        self.processed_text = None
        self.length_diff = 0
        self.draw_data = None
        self.have_code_cols = False
        self.have_dra_cols = False
        self.have_final_dra_cols = False
        self.length_dict = None
        self.page_number = 0
        self.text_data = None
        self.df = None

    def _clean_text(self):
        """Text data will be split by new lines. However, each hunt code will split into 3-10 lines. By removing certain text with
        new line characters this will make the hunt code split into 3 lines, the hunt code and list code, drawn out at results and
        final results.

        >>> text_data = 'EE001E1R A \nDrawn Out At 19 Pref \nPoints \n30 Pref \nPoints \nNone \nDrawn \nNone \nDrawn 4 Pref Points 2 Pref Points \n# Drawn at Final Level 1 of 3 1 of 1 N/A N/A 1 of 2 1 of 3'
        >>> drawReportParser(text_data=text_data)._clean_text()
        >>> self.processed_text()
        'EE001E1R A \nDrawn Out At 19 30 ND ND 4  2  \n# Drawn at Final Level 1/3 1/1 N/A N/A 1/2 1/3'
        """
        raw_text = re.sub(
            r"Pref \nPoints \n|Pref \nPoints |Pref Points", "", self.text_data
        )

        raw_text = re.sub(r"\nNone \nDrawn|None \nDrawn|None Drawn", "ND", raw_text)

        raw_text = re.sub(r"No Apps", "no-apps", raw_text)

        raw_text = re.sub(r"Choice ", "Choice-", raw_text)

        raw_text = re.sub(r"Leftover \nChoice", "Leftover-Choice", raw_text)

        raw_text = re.sub(r" of \n| of ", "/", raw_text)

        raw_text_with_split_markers = re.sub(r"\nEE", "split_marker EE", raw_text)

        raw_text_with_split_markers = re.sub(
            r"\nEF", "split_marker EF", raw_text_with_split_markers
        )

        raw_text_with_split_markers = re.sub(
            r"\nEM", "split_marker EM", raw_text_with_split_markers
        )

        raw_text_with_split_markers = re.sub(
            r"\nEP", "split_marker EP", raw_text_with_split_markers
        )

        raw_text_with_split_markers = re.sub(
            r"\nDrawn Out At| Drawn Out At",
            "split_marker DRA",
            raw_text_with_split_markers,
        )

        self.processed_text = re.sub(
            r"\n# Drawn at Final Level| # Drawn at Final Level",
            "split_marker DAFL",
            raw_text_with_split_markers,
        )

        self.draw_data = re.split(
            r"split_marker |\*  Hunts shaded", self.processed_text
        )

    def _elements_are_same(self, col_list):
        """Check if all elements in a list are the same. If they are the same return True, else return False."""
        return all(self.length_dict[col] == self.max_len for col in col_list)

    def _verify_value(self):
        """After the script runs all the data lists should be the same length. If they are not the same length the script will raise an error.
        This function is a proactive way to catch errors in the data parsing process.
        """
        value_lengths_key_array = [
            (len(v), k) for k, v in hunt_code_parser.all_data_dict.items()
        ]

        self.max_len = max(value_lengths_key_array)[0]

        lengths_diffs_key_array = [
            (length - self.max_len, k) for length, k in value_lengths_key_array
        ]

        self.length_diff = min(lengths_diffs_key_array)[0]

        if self.length_diff == -1:
            self.length_dict = {k: length for length, k in value_lengths_key_array}

            self.have_code_cols = self._elements_are_same(self.code_cols)
            self.have_dra_cols = self._elements_are_same(self.dra_cols)
            self.have_final_dra_cols = self._elements_are_same(self.final_dra_cols)

            logger.warning(
                "Data lists are not the same length for hunt code: %s, code data=%s DRA data=%s final DRA data=%s. Page number: %s",
                self.all_data_dict["hunt_code"][-1],
                self.have_code_cols,
                self.have_dra_cols,
                self.have_final_dra_cols,
                self.page_number,
            )

        elif self.length_diff < -1:
            return ValueError(
                f"Data lists have a difference greater than two. Most recent hunt code: {self.all_data_dict['hunt_code'][-1]}, data summary: {value_lengths_key_array}"
            )
        else:
            self.have_code_cols = False
            self.have_dra_cols = False
            self.have_final_dra_cols = False

    def _parse_text(self):
        for elt in self.draw_data:
            elt = elt.strip().replace("\n", " ")

            if elt.startswith(("EE", "EM", "EF", "EP")) and elt.endswith(
                ("A", "B", "C")
            ):
                self._verify_value()
                codes = elt.split(" ")

                if self.have_code_cols:
                    logger.info("Already have hunt code data for code: %s", codes[0])

                    continue

                if len(codes) != 2:
                    logger.info(
                        codes, self.max_len, self.all_data_dict["hunt_code"][-1]
                    )
                    logger.info(elt)
                    raise ValueError("List length is not 2")

                self.all_data_dict["hunt_code"].append(codes[0])
                self.all_data_dict["list_code"].append(codes[1])

            elif elt.startswith("DRA ") and "Report" not in elt:
                if self.have_dra_cols:
                    logger.info(
                        "Already have DRA data for hunt code: %s",
                        self.all_data_dict["hunt_code"][-1],
                    )
                    continue

                draw_data_str = elt.split("DRA ")[1]

                draw_out_data = [
                    data_point
                    for data_point in draw_data_str.split(" ")
                    if data_point != ""
                ]

                if len(draw_out_data) != 6:
                    logger.info(
                        draw_out_data, self.max_len, self.all_data_dict["hunt_code"][-1]
                    )
                    logger.info(elt)
                    raise ValueError("List length is not 6")

                self.all_data_dict["adult_res_draw_at"].append(draw_out_data[0])
                self.all_data_dict["adult_nonrest_draw_at"].append(draw_out_data[1])
                self.all_data_dict["youth_res_draw_at"].append(draw_out_data[2])
                self.all_data_dict["youth_nonrest_draw_at"].append(draw_out_data[3])
                self.all_data_dict["landowner_unrestr_draw_at"].append(draw_out_data[4])
                self.all_data_dict["landowner_restr_draw_at"].append(draw_out_data[5])

            elif elt.startswith("DAFL"):
                final_data_str = elt.split("DAFL ")[1]

                final_data = [
                    data_point
                    for data_point in final_data_str.split(" ")
                    if data_point != ""
                ]

                if len(final_data) != 6:
                    logger.info(
                        final_data, self.max_len, self.all_data_dict["hunt_code"][-1]
                    )
                    logger.info(elt)
                    raise ValueError("List length is not 6")

                self.all_data_dict["final_adult_res_draw_at"].append(final_data[0])
                self.all_data_dict["final_adult_nonrest_draw_at"].append(final_data[1])
                self.all_data_dict["final_youth_res_draw_at"].append(final_data[2])
                self.all_data_dict["final_youth_nonrest_draw_at"].append(final_data[3])
                self.all_data_dict["final_landowner_unrestr_draw_at"].append(
                    final_data[4]
                )
                self.all_data_dict["final_landowner_restr_draw_at"].append(
                    final_data[5]
                )

    def _add_cols(self):
        condition = [
            self.df.hunt_code.str.startswith("EE"),
            self.df.hunt_code.str.startswith("EM"),
            self.df.hunt_code.str.startswith("EF"),
            self.df.hunt_code.str.startswith("EP"),
        ]

        choices = ["Either Sex", "Male", "Female", "Preference Point"]

        self.df["animal_sex"] = np.select(condition, choices, "uh oh")

        self.df["gmu"] = self.df.hunt_code.str[2:5]

        condition = [
            self.df.hunt_code.str[-1] == "A",
            self.df.hunt_code.str[-1] == "M",
            self.df.hunt_code.str[-1] == "R",
            self.df.hunt_code.str[-1] == "X",
            self.df.hunt_code.str[-1] == "P",
        ]

        choices = ["Archery", "muzzleloader", "rifle", "season choice", "NA"]

        self.df["method_of_take"] = np.select(condition, choices, "uh oh")

    def pdf_to_csv(self):
        for i, page in enumerate(self.reader.pages):
            self.page_number = i

            text = page.extract_text()

            self.text_data = text

            self._clean_text()

            self._parse_text()

        self.df = pd.DataFrame(self.all_data_dict)

        self._add_cols()


if __name__ == "__main__":
    file_directory = Path(__file__).parent

    pdf_directory = (
        file_directory.parent.parent.parent
        / "pdf"
        / "draw_result"
        / "Drawn Out At Report 2024 Primary ELK.pdf"
    )

    reader = PdfReader(pdf_directory)

    hunt_code_parser = DrawReportParser(reader)

    hunt_code_parser.pdf_to_csv()

    file_directory = file_directory.parent / "assets" / "data" / "draw_results.csv"

    hunt_code_parser.df.to_csv(file_directory, index=False)
