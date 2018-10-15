from census import Census
import json
import requests
from us import states

class CensusTractRacePopulation:
    # Census ACS5 Data Profile dataset documentation
    # https://api.census.gov/data/2016/acs/acs5/profile/variables.html
    # Relevant Census Variables:
    #     DP05_0058E:  Estimate > RACE > Race alone or in combination with one or more other races > Total population
    #     DP05_0058PE: Percent > RACE > Race alone or in combination with one or more other races > Total population
    #     DP05_0059E:  Estimate > RACE > White
    #     DP05_0059PE: Percent > RACE > White
    #     DP05_0060E:  Estimate > RACE > Black or African American
    #     DP05_0060PE: Percent > RACE > Black or African American
    #     DP05_0061E:  Estimate > RACE > American Indian and Alaska Native
    #     DP05_0061PE: Percent > RACE > American Indian and Alaska Native
    #     DP05_0062E:  Estimate > RACE > Asian
    #     DP05_0062PE: Percent > RACE > Asian
    #     DP05_0063E:  Estimate > RACE > Native Hawaiian and Other Pacific Islander
    #     DP05_0063PE: Percent > RACE > Native Hawaiian and Other Pacific Islander
    #     DP05_0064E:  Estimate > RACE > Some other race
    #     DP05_0064PE: Percent > RACE > Some other race

    COUNTY_CODE_JACKSON_MO = '095'

    CENSUS_VARIABLE_TOTAL_POPULATION = 'DP05_0058'
    RACE_WHITE = 'DP05_0059'
    RACE_BLACK = 'DP05_0060'
    RACE_AMERICAN_INDIAN = 'DP05_0061'
    RACE_ASIAN = 'DP05_0062'
    RACE_NATIVE_HAWAIIAN = 'DP05_0063'
    RACE_OTHER = 'DP05_0064'

    VARIABLE_SUFFIX_ESTIMATE = 'E'
    VARIABLE_SUFFIX_ESTIMATE_PERCENT = 'PE'

    def __init__(self, census_json_data):
        self.state = states.lookup(census_json_data['state'])
        self.county = census_json_data['county']
        self.tract = census_json_data['tract']

        population_total_variable_name = CensusTractRacePopulation.CENSUS_VARIABLE_TOTAL_POPULATION + \
                                         CensusTractRacePopulation.VARIABLE_SUFFIX_ESTIMATE
        self.population_total_est = int(census_json_data[population_total_variable_name])

        race_variable_prefixes = CensusTractRacePopulation.get_all_races()

        variable_suffixes = [
            CensusTractRacePopulation.VARIABLE_SUFFIX_ESTIMATE,
            CensusTractRacePopulation.VARIABLE_SUFFIX_ESTIMATE_PERCENT,
        ]

        self.population_by_race_est = {}
        self.population_by_race_pctg = {}

        for race_prefix in race_variable_prefixes:
            est_variable_name = race_prefix + CensusTractRacePopulation.VARIABLE_SUFFIX_ESTIMATE
            pctg_variable_name = race_prefix + CensusTractRacePopulation.VARIABLE_SUFFIX_ESTIMATE_PERCENT

            self.population_by_race_est[race_prefix] = int(census_json_data[est_variable_name])

            percent = census_json_data[pctg_variable_name]
            percent = percent if percent > 0.0 else 0.0
            self.population_by_race_pctg[race_prefix] = percent

    def get_population_estimate_for_race(self, race):
        return self.population_by_race_est[race]

    def get_population_estimate_percentage_for_race(self, race):
        return self.population_by_race_pctg[race]

    @property
    def majority_race(self):
        max_population_race = None
        max_population = 0

        for race, population in self.population_by_race_est.items():
            if population > max_population:
                max_population_race = race
                max_population = population

        return max_population_race

    @staticmethod
    def get_race_display(race):
        if race == CensusTractRacePopulation.RACE_WHITE:
            return 'White'
        elif race == CensusTractRacePopulation.RACE_BLACK:
            return 'Black'
        elif race == CensusTractRacePopulation.RACE_AMERICAN_INDIAN:
            return 'American Indian and Alaska Native'
        elif race == CensusTractRacePopulation.RACE_ASIAN:
            return 'Asian'
        elif race == CensusTractRacePopulation.RACE_NATIVE_HAWAIIAN:
            return 'Native Hawaiian and Other Pacific Islander'
        elif race == CensusTractRacePopulation.RACE_OTHER:
            return 'Some other race'

        return ''

    @staticmethod
    def get_all_races():
        return [
            CensusTractRacePopulation.RACE_WHITE,
            CensusTractRacePopulation.RACE_BLACK,
            CensusTractRacePopulation.RACE_AMERICAN_INDIAN,
            CensusTractRacePopulation.RACE_ASIAN,
            CensusTractRacePopulation.RACE_NATIVE_HAWAIIAN,
            CensusTractRacePopulation.RACE_OTHER,
        ]

    @staticmethod
    def fetch(api_key, state, county, tract):
        client = Census(api_key)

        variable_prefixes = [
            CensusTractRacePopulation.CENSUS_VARIABLE_TOTAL_POPULATION,
            CensusTractRacePopulation.RACE_WHITE,
            CensusTractRacePopulation.RACE_BLACK,
            CensusTractRacePopulation.RACE_AMERICAN_INDIAN,
            CensusTractRacePopulation.RACE_ASIAN,
            CensusTractRacePopulation.RACE_NATIVE_HAWAIIAN,
            CensusTractRacePopulation.RACE_OTHER,
        ]

        variable_suffixes = [
            CensusTractRacePopulation.VARIABLE_SUFFIX_ESTIMATE,
            CensusTractRacePopulation.VARIABLE_SUFFIX_ESTIMATE_PERCENT,
        ]

        variable_names = []
        for prefix in variable_prefixes:
            for suffix in variable_suffixes:
                variable_names.append(prefix + suffix)

        results = client.acs5dp.state_county_tract(
            variable_names,
            state,
            county,
            tract,
        )

        return [CensusTractRacePopulation(result) for result in results]

    @staticmethod
    def fetch_by_address(api_key, address):
        # Use the Census geocoder service to try to find the census tract for
        # this address.
        # https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
        url = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress'
        params = {
            'address': address,
            'benchmark': 'Public_AR_Current',
            'vintage': 'Current_Current',
            'format': 'json',
        }

        geocoder_response = requests.get(url, params=params)
        try:
            geographies = json.loads(geocoder_response.text)
            census_tract = geographies['result']['addressMatches'][0]['geographies']['Census Tracts'][0]
        except:
            return None

        tracts = CensusTractRacePopulation.fetch(
            api_key,
            census_tract['STATE'],
            census_tract['COUNTY'],
            census_tract['TRACT'],
        )
        return tracts[0]
