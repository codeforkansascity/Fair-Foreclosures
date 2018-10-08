from census import Census
from census_tract_race_population import CensusTractRacePopulation
import sys
from us import states

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Provide your Census API token as an argument when running this script.')
        sys.exit()

    api_key = sys.argv[1]
    if not api_key:
        print('Provide your Census API token as an argument when running this script.')
        sys.exit()

    tracts = CensusTractRacePopulation.fetch(
        api_key,
        states.MO.fips,
        CensusTractRacePopulation.COUNTY_CODE_JACKSON_MO,
        Census.ALL,
    )

    races = [
        CensusTractRacePopulation.RACE_WHITE,
        CensusTractRacePopulation.RACE_BLACK,
        CensusTractRacePopulation.RACE_AMERICAN_INDIAN,
        CensusTractRacePopulation.RACE_ASIAN,
        CensusTractRacePopulation.RACE_NATIVE_HAWAIIAN,
        CensusTractRacePopulation.RACE_OTHER,
    ]

    rows = []
    header_titles = []
    header_titles.append('Tract')
    header_titles.append('Majority')
    for race in races:
        header_titles.append(CensusTractRacePopulation.get_race_display(race))

    rows.append(','.join(header_titles))

    for tract in tracts:
        row_data = [
            tract.tract,
            CensusTractRacePopulation.get_race_display(tract.majority_race),
        ]

        for race in races:
            estimate = tract.get_population_estimate_for_race(race)
            percent = tract.get_population_estimate_percentage_for_race(race)

            row_data.append('%d (%.2f%%)' % (estimate, percent))

        rows.append(','.join(row_data))

    for row in rows:
        print(row)
