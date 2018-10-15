from census import Census
from census_tract_race_population import CensusTractRacePopulation
import sys
from us import states

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Provide your Census API token and an address as arguments when running this script.')
        sys.exit()

    api_key = sys.argv[1]
    if not api_key:
        print('Provide your Census API token and an address as arguments when running this script.')
        sys.exit()

    address = sys.argv[2]
    if not address:
        print('Provide your Census API token and an address as arguments when running this script.')
        sys.exit()

    tract = CensusTractRacePopulation.fetch_by_address(api_key, address)
    races = [
        CensusTractRacePopulation.RACE_WHITE,
        CensusTractRacePopulation.RACE_BLACK,
        CensusTractRacePopulation.RACE_AMERICAN_INDIAN,
        CensusTractRacePopulation.RACE_ASIAN,
        CensusTractRacePopulation.RACE_NATIVE_HAWAIIAN,
        CensusTractRacePopulation.RACE_OTHER,
    ]

    print(address)
    for race in races:
        print('%s: %d (%.2f%%)' % (
            CensusTractRacePopulation.get_race_display(race),
            tract.get_population_estimate_for_race(race),
            tract.get_population_estimate_percentage_for_race(race),
        ))
