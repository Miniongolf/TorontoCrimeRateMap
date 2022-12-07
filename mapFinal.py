import pandas as pd
import plotly.express as px

# reads the csv file into crimeFile
crimeFile = pd.read_csv("Neighbourhood_Crime_Rates.csv")


# Lists to select the years and crimes that affect the map.

allYears = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
selectedYears = list(map(int, input("What years would you like to see? (2014 - 2021 inclusive): ").split()))

allCrimes = ["Assault", "AutoTheft", "BreakAndEnter", "Robbery", "TheftOver", "Homicide", "Shootings"]
selectedCrimes = ["Assault", "AutoTheft", "BreakAndEnter", "Robbery", "TheftOver", "Homicide", "Shootings"]
selectedCrimes = input("What crimes would you like to see? (Assault, AutoTheft, BreakAndEnter, Robbery, TheftOver, Homicide, Shootings): ").split()


# Creates a DataFrame that only contains the data we need to make our graph.

crime_stats = pd.DataFrame()
# Includes the neighbourhood IDs (for mapping identification),
crime_stats["HoodID"] = crimeFile["HoodID"]
# Neighbourhood name (to display on the map on hover),
crime_stats["HoodName"] = crimeFile["HoodName"]
# Rates for every selected crime for every selected year.
for crime in selectedCrimes:
    for year in selectedYears:
        crime_stats[f"{crime}_Rate{year}"] = crimeFile[f"{crime}_Rate{year}"]


# Creates list crimeTotals that adds the mean crime rate for every crime type each year for each neighbourhood

for crime in selectedCrimes:
    crimeTotals = []
    # Sets the frame we read as the crimerate of the current crime.
    curFrame = crime_stats[[f"{crime}_Rate{year}" for year in selectedYears]]
    for i in range(140):
        sum, count = 0, 0
        for year in selectedYears:
            # Adds the rate of that crime that year in that neighbourhood to sum.
            sum += curFrame[crime + "_Rate" + str(year)][i]
            count += 1
        # Adds the mean rate to crimeTotals
        crimeTotals.append(round(sum/count, 3))
    # Adds a column in crimeFrames for the crime total
    crime_stats[f"{crime}_Total"] = pd.DataFrame(crimeTotals)


# Function to get a score from 1 to 10 based on the crime rate.

# A linear relation from a score of 10 at no crime to a score of 0 at the most crime.
def getScore(nums):
    high = max(nums)
    scores = [10 - 10*n/high for n in nums]
    return scores

# Creates a DataFrame for all the scores
totalsList = [0 for i in range(140)]
for crime in selectedCrimes:
    for i in range(140):
        totalsList[i] += crime_stats[f"{crime}_Total"][i]
scoresFrame = pd.DataFrame(getScore(totalsList), columns=["Scores"])

# Adds scoresFrame to crime_stats under column Scores
crime_stats["Scores"] = scoresFrame


# Create the choropleth map with plotly.express

fig = px.choropleth(
  crime_stats, # Selects the dataframe to use as a dataset
  geojson = "https://raw.githubusercontent.com/Miniongolf/TorontoCrimeRateMap/689129f87a8c993feb9a4ce507010f5a7a51963e/neighbourhoodsCoords.geojson", # Selects the geojson file used (from a raw github link)
  featureidkey="properties.AREA_LONG_CODE",
  locations="HoodID",
  color='Scores',
  color_continuous_scale="inferno",
  hover_name="HoodName",
  hover_data=["Scores"] + [f"{crime}_Total" for crime in selectedCrimes],
  title='Crime Rates in Toronto',
  height = 650
)

# Show the map
fig.update_geos(fitbounds="locations", visible=False)

# NOTE: map opens in browser.
fig.show()
