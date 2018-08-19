from sodapy import Socrata
import sys

API_DATASET_NAME = 'data.kcmo.org'
API_RESOURCE_ID = 'ha6k-d6qu'

def get_full_dataset(app_token):
    n_records = 0
    offset = 0
    limit = 1000
    dataset = []

    with Socrata(API_DATASET_NAME, app_token) as client:
        while True:
            violation_records = client.get(
                API_RESOURCE_ID,
                order='id',
                limit=limit,
                offset=offset,
            )

            if not violation_records:
                break

            for record in violation_records:
                dataset.append(record)
                n_records += 1

            print('Fetched %d records (offset=%d)' % (
                limit,
                offset,
            ))

            offset += limit

    return dataset

def find_unique_violation_codes(dataset):
    unique_violation_codes = set()

    for row in dataset:
        code_description = (
            row['violation_code'],
            row['violation_description'],
        )
        unique_violation_codes.add(code_description)

    violation_codes = []
    for item in unique_violation_codes:
        violation_codes.append({
            'code': item[0],
            'description': item[1],
        })

    return violation_codes

def write_violation_codes_file(filename, dataset):
    with open(filename, 'w') as f:
        for row in dataset:
            f.write('%s,"%s"\n' % (
                row['code'],
                row['description'],
            ))

def find_unique_ordinance_numbers(dataset):
    unique_ordinance_numbers = set()

    for row in dataset:
        ordinance = (
            row['chapter'],
            row['ordinance'],
        )
        unique_ordinance_numbers.add(ordinance)

    ordinance_numbers = []
    for item in unique_ordinance_numbers:
        ordinance_numbers.append({
            'chapter': item[0],
            'ordinance': item[1],
        })

    return ordinance_numbers

def write_ordinance_numbers_file(filename, dataset):
    with open(filename, 'w') as f:
        for row in dataset:
            f.write('%s,"%s"\n' % (
                row['chapter'],
                row['ordinance'],
            ))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Provide your app token as an argument when running this script.')
        sys.exit()

    app_token = sys.argv[1]
    if not app_token:
        print('Provide your app token as an argument when running this script.')
        sys.exit()

    print('Building violation codes...')

    dataset = get_full_dataset(app_token)

    violation_codes_filename = 'results/violation_codes.csv'
    violation_codes = find_unique_violation_codes(dataset)
    write_violation_codes_file(violation_codes_filename, violation_codes)
    print('Violation Codes: output %d records to %s' % (
        len(violation_codes),
        violation_codes_filename,
    ))

    ordinance_numbers_filename = 'results/ordinance_numbers.csv'
    ordinance_numbers = find_unique_ordinance_numbers(dataset)
    write_ordinance_numbers_file(ordinance_numbers_filename, ordinance_numbers)
    print('Ordinance Numbers: output %d records to %s' % (
        len(ordinance_numbers),
        ordinance_numbers_filename,
    ))
