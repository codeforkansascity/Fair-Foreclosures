import sys
from census import Census
from us import states

# Census ACS5 Data Profile dataset documentation
# https://api.census.gov/data/2016/acs/acs5/profile/variables.html

COUNTY_CODE_JACKSON_MO = '095'
VARIABLES = {
    'DP05_0058E': 'Estimate!!RACE!!Race alone or in combination with one or more other races!!Total population',
    'DP05_0058PE': 'Percent!!RACE!!Race alone or in combination with one or more other races!!Total population',
    'DP05_0059E': 'Estimate!!RACE!!White',
    'DP05_0059PE': 'Percent!!RACE!!White',
    'DP05_0060E': 'Estimate!!RACE!!Black or African American',
    'DP05_0060PE': 'Percent!!RACE!!Black or African American',
    'DP05_0061E': 'Estimate!!RACE!!American Indian and Alaska Native',
    'DP05_0061PE': 'Percent!!RACE!!American Indian and Alaska Native',
    'DP05_0062E': 'Estimate!!RACE!!Asian',
    'DP05_0062PE': 'Percent!!RACE!!Asian',
    'DP05_0063E': 'Estimate!!RACE!!Native Hawaiian and Other Pacific Islander',
    'DP05_0063PE': 'Percent!!RACE!!Native Hawaiian and Other Pacific Islander',
    'DP05_0064E': 'Estimate!!RACE!!Some other race',
    'DP05_0064PE': 'Percent!!RACE!!Some other race',
}

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Provide your Census API token as an argument when running this script.')
        sys.exit()

    api_key = sys.argv[1]
    if not api_key:
        print('Provide your Census API token as an argument when running this script.')
        sys.exit()

    client = Census(api_key)
    results = client.acs5dp.state_county_tract(
        list(VARIABLES.keys()),
        states.MO.fips,
        COUNTY_CODE_JACKSON_MO,
        Census.ALL,
    )

    for result in results:
        print('Tract: %s' % result['tract'])
        for variable_name, description in VARIABLES.items():
            print('  - %s: %d' % (description, result[variable_name]))
