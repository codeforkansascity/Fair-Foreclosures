# Census Tract Race Population

This is a class for working with census data for race population estimates per census tract. The data comes from the [Census ACS5DP dataset](https://api.census.gov/data/2016/acs/acs5/profile/variables.html) dataset.

Fetching data for a specific address uses the [Census geocoding service](https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html) as well.

Examples:

```python
>>> from census_tract_race_population import CensusTractRacePopulation
>>> tract = CensusTractRacePopulation.fetch_by_address([api token], '3412 E 29th St, Kansas City, MO')
>>> print('State: %s (%s)' % (tract.state.name, tract.state.abbr))
State: Missouri (MO)
>>> print('County FIPS code: %s' % tract.county)
County FIPS code: 095
>>> print('Census Tract: %s' % tract.tract)
Census Tract: 016500
>>> print(tract.population_total_est)
1829
>>> for race in CensusTractRacePopulation.get_all_races():
...     display = CensusTractRacePopulation.get_race_display(race)
...     population = tract.get_population_estimate_for_race(race)
...     population_pctg = tract.get_population_estimate_percentage_for_race(race)
...     print('%s: %d (%.2f)' % (display, population, population_pctg))
...
White: 148 (8.10)
Black: 1648 (90.10)
American Indian and Alaska Native: 12 (0.70)
Asian: 0 (0.00)
Native Hawaiian and Other Pacific Islander: 0 (0.00)
Some other race: 75 (4.10)
>>> print(CensusTractRacePopulation.get_race_display(tract.majority_race))
Black
>>> tract.majority_race == CensusTractRacePopulation.RACE_BLACK
True
```
