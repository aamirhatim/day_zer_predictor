# Day Zero Predictor
[Click here](Project Explanation.pdf) to read a description of the project.

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

#### Per Capita Consumption 
- listed for most recent years
- total water consumption per capita (m^3/inhab/year) [AQUASTAT]

# Initial Pre-processing Steps

#### 1. Filtering of precipitation data 
- filtering of data with pandas to obtain records for latest year and annual precipitation in mm/yr

#### 2. Filtering of water resources data
- filtering of data with pandas to obtain records for latest year and total renewable water resources per capita in m^3/inhab/yr
