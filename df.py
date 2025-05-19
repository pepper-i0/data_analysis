# load and explore database
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#inline plotting
# %matplotlib inline

#load dataset
covidData = pd.read_csv(r'owid-covid-data.csv')

# clean data for clarity
covidData.columns = [col.replace(' ', '').lower() for col in covidData.columns]

# explore dataset first few rows
print(covidData.head())

#display info
print("\nDataset Information:")
print(covidData.info())

# filtering countries
countries = ['Nigeria', 'South Africa', 'Kenya', 'Ghana', 'Uganda', 'United Kingdom', 'United States', 'India', 'Brazil', 'China']
covidData = covidData[covidData['location'].isin(countries)]

# convert date column to datetime
covidData['date'] = pd.to_datetime(covidData['date'], errors='coerce')

# Drop rows with missing date or totalCases for case plots
casesData = covidData.dropna(subset=['date', 'total_cases'])

# Line graph over time by location for total cases
plt.figure(figsize=(15, 8))
for location in countries:
    subset = casesData[casesData['location'] == location]
    plt.plot(subset['date'], subset['total_cases'], label=location)

plt.title('Total COVID Cases Over Time by Location')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.tight_layout()
plt.show()

# Drop rows with missing date or total_deaths for death plots
deathsData = covidData.dropna(subset=['date', 'total_deaths'])

# Line chart for total deaths over time by location
plt.figure(figsize=(15, 8))
for location in countries:
    subset = deathsData[deathsData['location'] == location]
    plt.plot(subset['date'], subset['total_deaths'], label=location)

plt.title('Total COVID Deaths Over Time by Location')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.legend()
plt.tight_layout()
plt.show()

# Calculate Death Rate in percentage (avoid division by zero)
covidData['death_rate'] = np.where(
    covidData['total_cases'] > 0,
    (covidData['total_deaths'] / covidData['total_cases']) * 100,
    0
)

# Bar chart for top 5 countries by Total Cases
top_5_countries = covidData.sort_values('total_cases', ascending=False).groupby('location')['total_cases'].max().nlargest(5).index
top_5_data = covidData[covidData['location'].isin(top_5_countries)]

plt.figure(figsize=(12, 6))
sns.barplot(data=top_5_data, x='location', y='total_cases', palette='viridis', legend=False)
plt.title('Top 5 Countries by Total COVID Cases')
plt.xlabel('location')
plt.ylabel('total_cases')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Cumulative vaccination over time
vax_countries = ['United Kingdom', 'United States', 'Nigeria']
vaxData = covidData.dropna(subset=['date', 'total_vaccinations'])

plt.figure(figsize=(15,8))
for location in vax_countries:
    subset = vaxData[vaxData['location'] == location]
    plt.plot(subset['date'], subset['total_vaccinations'], label=location)

plt.title('Cumulative COVID Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.tight_layout()
plt.show()

# Pie chart for vaccinated vs unvaccinated in Nigeria (latest data)
nigeria_data = covidData[covidData['location'] == 'Nigeria'].dropna(subset=['total_vaccinations', 'population'])
if not nigeria_data.empty:
    latest_nigeria = nigeria_data.sort_values('date').iloc[-1]
    vaccinated = latest_nigeria['total_vaccinations']
    population = latest_nigeria['population']
    unvaccinated = max(population - vaccinated, 0)

    plt.figure(figsize=(8, 8))
    plt.pie([vaccinated, unvaccinated], labels=['Vaccinated', 'Unvaccinated'], autopct='%1.1f%%', startangle=90)
    plt.title('COVID Vaccination Status in Nigeria')
    plt.show()
else:
    print("No vaccination data available for Nigeria.")

print(covidData.columns)
print(covidData['total_deaths'])
