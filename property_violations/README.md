# Open Data KC Utilities

This is a collection of utilities that make it easy to work with several of the Open Data KC datasets. API responses are converted to native Python objects which generally have some constants and methods to help work with the data.

### property_violations.py
This module deals with the [KCMO Property Violations dataset](https://data.kcmo.org/Housing/Property-Violations/nhtf-e75a). The primary class is `PropertyViolation` which is a Python object representing a single record from the dataset.

Examples:

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
...     print(violation.ordinance.chapter_title + ': ' + str(violation.ordinance))
...
NSFENCE01: ALL FENCES AND RET. WALLS KEPT IN REPAIR
Property Maintenance Code: Ordinance: 56 (56-114 C.O.)
```

### dangerous_buildings.py
This module deals with the [KCMO Dangerous Buildings dataset](https://dev.socrata.com/foundry/data.kcmo.org/rm2v-mbk5). The primary class is `DangerousBuilding` which is a Python object representing a single record from the dataset.

Examples:

```python
>>> from dangerous_buildings import DangerousBuilding
>>> dangerous_buildings = DangerousBuilding.fetch_by_address([app token], '5624 E 55TH ST')
>>> for dangerous_building in dangerous_buildings:
...     print(dangerous_building.statusofcase)
...
On Hold

>>> dangerous_buildings = DangerousBuilding.fetch_by_pin([app token], 29763)
>>> for dangerous_building in dangerous_buildings:
...     print(dangerous_building.address)
...     print(dangerous_building.coordinates)
...
4007 Chestnut Ave
Coordintes: (39.053094, -94.551058)
```

### service_request_calls.py
This module deals with the [KCMO 311 Call Center Service Requests dataset](https://dev.socrata.com/foundry/data.kcmo.org/cyqf-nban). The primary class is `ServiceRequestCall` which is a Python object representing a single record from the dataset.

Examples:

```python
>>> calls = ServiceRequestCall.fetch_by_address([app token], '11204 APPLEWOOD DR')
>>> for call in calls:
...     creation_date_time = call.creation_date_time.strftime('%m-%d-%Y')
...     status = 'Open' if call.is_open else 'Closed'
...     print('%d: %s on %s (%s)' % (call.case_id, call.type, creation_date_time, status))
...
2018023696: Nuisance on 02-26-2018 (Closed)
2011133841: Private Property on 06-06-2011 (Closed)
2012019413: Private Property on 02-17-2012 (Closed)
2013113880: Property Maintenance on 08-14-2013 (Closed)
2014006777: Investigation on 01-16-2014 (Closed)
2014102323: Bite on 08-07-2014 (Closed)
2014120749: Investigation on 09-17-2014 (Closed)
2015090907: Cruelty or Neglect on 07-30-2015 (Closed)
2015092984: Stray on 08-04-2015 (Closed)
2015146779: Permit / License on 12-15-2015 (Closed)
2016019857: Stray on 02-25-2016 (Closed)
2017001022: Dangerous Building on 01-04-2017 (Closed)
```
