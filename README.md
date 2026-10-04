# sofia-temperature-analysis

## Description

This project analyzes how temperatures in Sofia have changed over time, focusing on mean, maximum, and minimum temperatures. Climate data is extracted, inspected, cleaned, and analyzed to identify changes and trends on a yearly, monthly, and seasonal basis.

The analysis aims to answer the following questions:

1. How has the average annual temperature changed over time?
2. Which months and seasons show the largest and most consistent changes?
3. Which years were the hottest and coldest?

## Getting Started

### 1. Clone the repository

### 2. Create and activate the virtual environment

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Retrieve the data

Run the data-loading script from the project root:

    python src/load_data.py

This retrieves the Sofia daily temperature data from Meteostat and saves the data and associated metadata to `data/raw/`.

### 5. Run the notebooks

Run the notebooks in the `notebooks` folder in numerical order, following the order indicated by their filenames.

## Data Source and Licence

Information regarding the sources and licences can be found in DATA_LICENCE.md