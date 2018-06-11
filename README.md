# Day Zero Predictor
"Day Zero" is a term that is used to refer to a situation of extreme water shortage - a situation that Cape Town came very close to facing last year. They have managed to avoid complete water shortage as of now, but it is a huge warning for the rest of the world. Many cities all around the world experience water shortages throughout the year, causing massive disruptions in day-to-day life of locals, businesses, and the economy. The ability to keep an eye on cities coming close to a ‘Day Zero’ event could be incredibly useful in not only effectively deploying aid, but also to take preventative actions early on so that local authorities are not forced to impose extreme water usage laws on short notice.

To help raise awareness to this situation, we used machine learning to develop a model to predict the water stress level of a country given a particular set of attributes. Though we do not have enough data to go down to the city level, viewing things from a larger perspective can certainly provide insight into how a nation should work as a whole to prevent reaching a Day Zero situation.

[Click here](Project_Explanation.pdf) to read a description of the project.

## About the Data
Most of our data was gathered from the extensive [AQUASTAT](http://www.fao.org/nr/water/aquastat/main/index.stm) database which provides many different water metrics for every country for the past 60 years. Another source was used to get rainwater harvesting information.

### Attributes
#### Geography
- % total country cultivated [AQUASTAT]
  - This is a percentage of the total land area of the country that has been cultivated.
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

### Dealing with Missing Attributes
Much of this data (at the time of this project) is difficult to measure and record for several countries, so there were a lot of missing fields to deal with. Our current setup uses linear regression to come up with a simple best-fit model for every attribute of every country. Any missing attributes are then populated using this model

#### Processing
Data from our sources were presented in several different formats and contained extra information that was not useful for our application, so we developed data purification scripts to keep only what was necessary. [`parse_csv`](parse_csv.py) contains functions to parse raw CSV files from our sources into datasets that are compatible with our machine learning application.

#### Per Capita Consumption
- listed for most recent years
- total water consumption per capita (m^3/inhab/year) [AQUASTAT]

# Initial Pre-processing Steps

#### 1. Filtering of precipitation data
- filtering of data with pandas to obtain records for latest year and annual precipitation in mm/yr

#### 2. Filtering of water resources data
- filtering of data with pandas to obtain records for latest year and total renewable water resources per capita in m^3/inhab/yr
