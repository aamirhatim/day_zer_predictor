# Day Zero Predictor

### Attributes Considered
#### Geography
- total area of country (1000 ha) [AQUASTAT]
- cultivated area (1000 ha) [AQUASTAT]
- % total country cultivated [AQUASTAT]
- annual precipitation (mm/yr) [AQUASTAT]
- annual precipitation (10^9 m^3/yr) [AQUASTAT]

#### Water Resources
- total renewable water resources (10^9 m^3/yr) [AQUASTAT]
- water dependency ratio (%) [AQUASTAT]
- total renewable water resources per capita (m^3/inhab/yr) [AQUASTAT]
- total exploitable water resources (10^9 m^3/yr) [AQUASTAT]

### Data Collection and Processing
#### Sources
- AQUASTAT

#### Processing
Data from our sources were presented in several different formats and contained extra information that was not useful for our application, so we developed data purification scripts to keep only what was necessary. [`parse_csv`](parse_csv.py) contains functions to parse raw CSV files from our sources into datasets that are compatible with our machine learning application.
