import csv
from datetime import datetime, timedelta
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

def read_legal_brief_violations(filename):
    # TODO: make this function a little more robust. Right now it's quick &
    # dirty and relies on the legal brief scoring file being formatted as a
    # Markdown table with specific column headers.
    file_rows = []
    with open(filename, 'r') as f:
        file_rows = f.readlines()

    first_row = file_rows.pop(0)
    second_row = file_rows.pop(0)
    start_idx = first_row.find('Violation Codes') - 1
    end_idx = first_row.find('|', start_idx)

    violation_codes = set()
    for row in file_rows:
        codes = row[start_idx:end_idx].strip().split(',')
        for code in codes:
            stripped_code = code.strip()
            if not stripped_code:
                continue

            violation_codes.add(stripped_code)

    return list(violation_codes)

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

        results[reo_property['kiva_pin']] = {
            'start_date': reo_property['start_date'],
            'end_date': reo_property['end_date'],
            'violations': relevant_violations,
        }

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

def calculate_violation_stats(violations_per_property, legal_brief_violation_codes):
    results = {}

    for kiva_pin, property_data in violations_per_property.items():
        start_date = property_data['start_date']
        end_date = property_data['end_date'] or datetime.now()
        days = (end_date - start_date).days

        if not property_data['violations']:
            avg_daily_score = 0.0
            avg_duration = 0.0
        else:
            # Calculate an estimated score for the violations that were open during
            # the given period
            daily_scores = []
            for i in range(0, days):
                day = start_date + timedelta(days=i)
                day_violation_scores = []

                for violation in property_data['violations']:
                    violation_open_on_day = False
                    if violation.case_opened >= day:
                        if violation.is_open:
                            violation_open_on_day = True
                        elif violation.case_closed and violation.case_closed >= day:
                            violation_open_on_day = True

                    if not violation_open_on_day:
                        continue

                    score = 0

                    # Violations that are still open are weighted more heavily
                    if violation.is_open:
                        score += 2

                    # Violations that are relevant (based on the criteria extracted
                    # from the Chicago legal brief) are weighted more heavily
                    if violation.code.code in legal_brief_violation_codes:
                        score += 2

                    score += 1

                    day_violation_scores.append(score)

                daily_scores.append(sum(day_violation_scores))

            avg_daily_score = sum(daily_scores) / days

            # Find the average duration of violations open during the given period
            durations = [v.days_open for v in property_data['violations']]
            avg_duration = sum(durations) / len(durations)

        results[kiva_pin] = {
            'violation_count': len(property_data['violations']),
            'score': avg_daily_score,
            'avg_duration': avg_duration,
        }


    return results

def write_violation_stats(violation_stats, filename):
    file_output = []
    file_output.append([
        'KIVA PIN',
        'Violation Count',
        'Property Score',
        'Average Durations',
    ])

    for kiva_pin, stats in violation_stats.items():
        file_output.append([
            kiva_pin,
            stats['violation_count'],
            stats['score'],
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
    legal_brief_violation_codes = read_legal_brief_violations('../docs/scoring.md')
    violations = get_violations_per_property(app_token, properties)
    violation_stats = calculate_violation_stats(violations, legal_brief_violation_codes)
    write_violation_stats(violation_stats, 'example/results/violation_stats.csv')
