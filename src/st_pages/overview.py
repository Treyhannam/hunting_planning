import streamlit as st
import logging
import sys
from utils.st_helpers import st_sidebar
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(filename)s] [%(funcName)20s()] [%(levelname)s] - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)

src_directory = Path(__file__).parent.parent

resource_directory = src_directory.parent / 'resources'

st.set_page_config(layout="wide")

st_sidebar()

st.markdown(
"""
# Elk Archery Harvest Report Overview

This project aims to display archery Harvest data from Colorado Parks and Wildlife (CPW) in an easy to understand way. I find interactive graphs more productive than reading through PDFs.

There is data available for years [2019-2023 on their website](https://cpw.state.co.us/hunting/big-game/elk/statistics#4257225834-291300671).
Fortunetly, I was able to save years 2006-2018 before they removed those them from the website.

Note, there may be incorrect data displayed, the PDF files were turned into CSV files using a programming script and some unforseen issues may have occured.

#### Metrics from the PDF Files
- Percent Success: Success rate 0 meaning nobody got an elk, 100 meaning every hunter got an elk.
- Total Hunters: Number of hunters.
- Bulls: Number of bulls harvested.
- Cows: Number of cows harvested.
- Calves: Number of calves harvested.
- Total Harvest: Number of bulls, calves, and cows harvested.
- Total Rec Days: Number of days all hunters were present.

#### Future additions may be made depending on data availability. Such additions could be...
- Harvest by all other manners of take (Muzzle laoder, rifle)
- Other big game species (Moose, deer, goat)
- public/private land
- OTC/Draw for the unit
- draw results with points needed to pull
- hunt codes (Bull/Cow/Either Sex).

Some of this data is available in PDF form but is hard to systematically use a script to turn it into CSV data. Maybe CPW would be willing to provide the data as CSVs. Another avenue could be
using [Colorado Open Records Act (CORA)](https://www.sos.state.co.us/pubs/info_center/cora.html) but unsure what the fee's will cost or if the intention to share on a website will void that avenue.

## Data Visualization Pages on this Website

- **Unit Trends:** You can filter to specific units to see elk harvested, number of hunters, and success rate by year.
- **Interactive Map:** A map that plots each game management unit (GMU) in Colorado. Also, provides the ability to select a year and metric to view the status for each unit. If a unit does not show up then it was not hunted that year.

## Mobile VS Website Users

The graphs and map need additional adjustments depending on the device you are using. Use the navigation bar to indicate if you are using a mobile device or not.

##### 1. Open the Navbar located in the top left corner.
"""
)

st.image(os.path.join(resource_directory, 'Opening_sidebar.png'))

st.markdown("##### 2. Toggle if you are using a mobile device or not")

st.image(os.path.join(resource_directory, 'Mobile_device.png'))

st.markdown("## Submit Feedback")

with st.form(key='submission', clear_on_submit=True):
    email = st.text_input('Email (Optional)', key='email')

    feedback = st.text_input('Feedback', key='feedback')

    submitted = st.form_submit_button()

    if not feedback and submitted:
        st.write('Please provide feedback before submitting.')
    if submitted and feedback:
        logger.info(f'email={email}, feedback={feedback}')
        st.write('Thank you!')

