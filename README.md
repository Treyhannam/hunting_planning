# Elk Archery Harvest Report

This project aims to display archery harvest data from Colorado Parks and Wildlife (CPW) in an easy-to-understand way. The data is visualized using interactive graphs and maps, making it more productive than reading through PDFs.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/hunting_planning.git
    cd hunting_planning
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install .
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run src/app/main.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to view the application.

## Features

- **Unit Trends:** Filter to specific units to see elk harvested, number of hunters, and success rate by year.
- **Interactive Map:** A map that plots each game management unit (GMU) in Colorado. Select a year and metric to view the status for each unit.

## (Possible) Future Additions

- Harvest by other manners of take (Muzzleloader, rifle)
- Other big game species (Moose, deer, goat)
- Public/private land
- OTC/Draw for the unit
- Draw results with points needed to pull
- Hunt codes (Bull/Cow/Either Sex)

## Feedback

We welcome your feedback! Please submit your feedback through the form available in the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.