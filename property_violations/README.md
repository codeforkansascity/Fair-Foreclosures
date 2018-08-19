# Property Violations

### property_violations.py
This is a module containing some classes that make it easy to fetch data from the [KCMO Property Violations dataset](https://data.kcmo.org/Housing/Property-Violations/nhtf-e75a). The primary class is `PropertyViolation` which is a Python object representing a single record from the dataset. It doesn't have much functionality now, but it does convert the properties to their native Python data types. We can add to it as we go.

Fetching data from the API is done via static methods on this class. Here are a couple examples:

```python
>>> from property_violations import PropertyViolation
>>> violations = PropertyViolation.fetch_by_address([app token], '2624 Kensington Ave')
>>> for violation in violations:
...     print(violation.is_open)
...
False
False
False
[etc.]

>>> for violation in violations:
...     print(violation.case_opened.strftime('%m-%d-%Y'))
...
05-19-2014
08-15-2012
05-19-2014
[etc.]

>>> violations = PropertyViolation.fetch_by_pin([app token], 23895)
>>> for violation in violations:
...     print('%s (%s, %s, %d)' % (violation.address, violation.county, violation.state, violation.zip_code))
...
3412 E 29TH ST (Jackson, MO, 64128)
3412 E 29TH ST (Jackson, MO, 64128)
3412 E 29TH ST (Jackson, MO, 64128)
[etc.]

>>> violations = PropertyViolation.fetch_by_address([app token], '211 N Askew Ave')
>>> fence_violations = filter(lambda x: x.code.is_fence_violation, violations)
>>> for violation in fence_violations:
...     print(violation.code.code + ': ' + violation.code.description)
...
NSFENCE01: ALL FENCES AND RET. WALLS KEPT IN REPAIR
```

### violations_per_property.py
This script reads a CSV file containing a list of properties and date ranges (the dates that the lender owned the property) and outputs a set of stats about the code violations for each property.

### get_unique_codes.py
In the process of working with the property violation data, it seemed useful to have a list of the unique property violation codes and ordinances, so I wrote a couple scripts to generate these from the dataset. These scripts pull the entire dataset and identify unique (violation_code, violation_description) combinations and (chapter, ordinance) combinations, writing them to `results/violation_codes.csv` and `results/ordinance_numbers.csv`.

### Pipfile and Pipfile.lock
I'm not too familiar with `pipenv` but I used it in this project to create a virtual environment, and committed these files. I'm pretty sure that if you have `pipenv`, you can run `pipenv install` from the property_violations directory to create a virtual environment for yourself from these files, then `pipenv shell` to run in that environment. If that's not working, the requirements currently are:
* [sodapy](https://pypi.org/project/sodapy/)
* [python-dateutil](https://pypi.org/project/python-dateutil/)
