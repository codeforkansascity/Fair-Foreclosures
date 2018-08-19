import csv
from dateutil.parser import parse
from property_violations import PropertyViolation
import sys

def read_properties(filename):
    file_rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        file_rows = [row for row in reader]

    first_row = file_rows.pop(0)
    if first_row != ['KIVA PIN', 'Start Date', 'End Date']:
        raise ValueError('Unexpected input file format')

    processed_rows = []
    for row in file_rows:
        processed_row = {
            'kiva_pin': int(row[0]),
            'start_date': parse(row[1]),
            'end_date': parse(row[2]) if row[2] else None,
        }
        processed_rows.append(processed_row)

    return processed_rows

def get_violations_per_property(app_token, properties, debug=False):
    results = {}

    for reo_property in properties:
        violations = PropertyViolation.fetch_by_pin(
            app_token,
            reo_property['kiva_pin'],
        )

        relevant_violations = []
        for violation in violations:
            # TODO: violations will only be included here if the violation was
            # opened *after* the given start date. Is this correct? Are there
            # cases where the lender took over a property with open violations
            # that should still be counted here?
            if violation.case_opened >= reo_property['start_date']:
                if reo_property['end_date']:
                    if violation.case_opened <= reo_property['end_date']:
                        relevant_violations.append(violation)
                else:
                    relevant_violations.append(violation)

        results[reo_property['kiva_pin']] = relevant_violations

        # DEBUG
        if debug:
            for violation in violations:
                print('%d / %s: %s - %s %s' % (
                    violation.pin,
                    violation.address,
                    violation.case_opened.strftime('%Y-%m-%d'),
                    violation.case_closed.strftime('%Y-%m-%d') if violation.case_closed else '?',
                    ' -> INCLUDED' if violation in relevant_violations else '',
                ))

    return results

def calculate_violation_stats(violations_per_property):
    results = {}

    for kiva_pin, violations in violations_per_property.items():
        violation_count = len(violations)
        if violation_count > 0:
            avg_severity = sum(v.code.severity for v in violations) / violation_count
            avg_duration = sum(v.days_open for v in violations) / violation_count
        else:
            avg_severity = 0.0
            avg_duration = 0.0

        results[kiva_pin] = {
            'violation_count': violation_count,
            'avg_severity': avg_severity,
            'avg_duration': avg_duration,
        }

    return results

def write_violation_stats(violation_stats, filename):
    file_output = []
    file_output.append([
        'KIVA PIN',
        'Violation Count',
        'Average Severity',
        'Average Durations',
    ])

    for kiva_pin, stats in violation_stats.items():
        file_output.append([
            kiva_pin,
            stats['violation_count'],
            stats['avg_severity'],
            stats['avg_duration'],
        ])

    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerows(file_output)

    print('Output violation stats to ' + filename)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Provide your app token as an argument when running this script.')
        sys.exit()

    app_token = sys.argv[1]
    if not app_token:
        print('Provide your app token as an argument when running this script.')
        sys.exit()

    properties = read_properties('example/reo_properties.csv')
    violations = get_violations_per_property(app_token, properties)
    violation_stats = calculate_violation_stats(violations)
    write_violation_stats(violation_stats, 'example/results/violation_stats.csv')
