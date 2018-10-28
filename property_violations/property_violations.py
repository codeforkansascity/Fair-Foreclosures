from city_ordinance import CityOrdinance
from dateutil.parser import parse
from sodapy import Socrata

class PropertyViolationException(Exception):
    """An exception that may be raised by the PropertyViolation class."""
    pass

class Coordinates:
    """A pair of latitude/longitude coordinates."""

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return 'Coordintes: (%s, %s)' % (str(self.lat), str(self.lon))

class PropertyViolationCode:
    """A property violation code.

    Includes properties to help identify certain categories of violations. More
    properties can be added to the class as necessary.
    """

    def __init__(self, code, description):
        self.code = code
        self.description = description

    @property
    def is_electrical_violation(self):
        return self.code.startswith('NSELECT')

    @property
    def is_fence_violation(self):
        return self.code.startswith('NSFENCE')

    @property
    def is_infestation_violation(self):
        return self.code.startswith('NSINFEST')

    @property
    def is_plumbing_violation(self):
        return self.code.startswith('NSPLUMB')

    def __str__(self):
        return 'Code: %s (%s)' % (self.code, self.description)

class PropertyViolation:
    """A property violation.

    This class represents a single KCMO property violation and includes methods
    to obtain property violations from the KCMO Open Data API.

    https://data.kcmo.org/Housing/Property-Violations/nhtf-e75a
    """

    API_DATASET_NAME = 'data.kcmo.org'
    API_RESOURCE_ID = 'ha6k-d6qu'

    STATUS_OPEN = 'Open'
    STATUS_CLOSED = 'Closed'

    def __init__(self,
                 id_=0,
                 case_id=0,
                 status='',
                 case_opened=None,
                 case_closed=None,
                 days_open=0,
                 violation=None,
                 ordinance=None,
                 violation_entry_date=None,
                 address='',
                 county='',
                 state='',
                 zip_code=0,
                 coordinates=None,
                 pin=0,
                 council_district=0,
                 police_district='',
                 inspection_area='',
                 neighborhood='',
                 mapping_location=None):
        self.id_ = id_
        self.case_id = case_id
        self.status = status
        self.case_opened = case_opened
        self.case_closed = case_closed
        self.days_open = days_open
        self.violation = violation
        self.ordinance = ordinance
        self.violation_entry_date = violation_entry_date
        self.address = address
        self.county = county
        self.state = state
        self.zip_code = zip_code
        self.coordinates = coordinates
        self.pin = pin
        self.council_district = council_district
        self.police_district = police_district
        self.inspection_area = inspection_area
        self.neighborhood = neighborhood
        self.mapping_location = mapping_location

    @staticmethod
    def from_json(json_data):
        """Convert JSON data (obtained from the KCMO Open Data API) to a
        PropertyViolation object.
        """

        def to_date(value):
            return parse(value) if value else None

        def to_int(value):
            return int(value) if value else 0

        violation = PropertyViolation(
            id_=to_int(json_data.get('id')),
            case_id=to_int(json_data.get('case_id')),
            status=json_data.get('status', ''),
            case_opened=to_date(json_data.get('case_opened')),
            case_closed=to_date(json_data.get('case_closed')),
            days_open=to_int(json_data.get('days_open')),
            violation_entry_date=to_date(json_data.get('violation_entry_date')),
            address=json_data.get('address', ''),
            county=json_data.get('county', ''),
            state=json_data.get('state', ''),
            zip_code=to_int(json_data.get('zip_code')),
            pin=to_int(json_data.get('pin')),
            council_district=json_data.get('council_district', ''),
            police_district=json_data.get('police_district', ''),
            inspection_area=json_data.get('inspection_area', ''),
            neighborhood=json_data.get('neighborhood', ''),
            mapping_location=json_data.get('mapping_location'),
        )

        violation.coordinates = Coordinates(
            json_data.get('latitude'),
            json_data.get('longitude'),
        )

        violation.code = PropertyViolationCode(
            json_data.get('violation_code'),
            json_data.get('violation_description'),
        )

        violation.ordinance = CityOrdinance(
            to_int(json_data.get('chapter')),
            json_data.get('ordinance'),
        )

        return violation

    @staticmethod
    def fetch(app_token, search_params, limit=5000):
        """Fetch a list of PropertyViolation objects from the KCMO Open Data
        API. `search_params` is a list of search critera as allowed by the
        Socrata SoQL query language (https://dev.socrata.com/docs/queries/).
        All given parameters will be combined using 'AND' in the query.
        By default, we limit the results to 5000 records but you can specify
        a different limit with the `limit` parameter.
        """

        with Socrata(PropertyViolation.API_DATASET_NAME, app_token) as client:
            where_clause = ' and '.join(search_params)

            # Raises a requests.exceptions.HTTPError if bad criteria is given
            violation_records = client.get(
                PropertyViolation.API_RESOURCE_ID,
                where=where_clause,
                limit=limit,
            )

        return [PropertyViolation.from_json(rec) for rec in violation_records]

    @staticmethod
    def fetch_by_address(app_token, address):
        """Fetch a list of PropertyViolation objects from the KCMO Open Data
        API for a single address. Partial addresses can be given, but must
        match the beginning of the street address.
        """

        return PropertyViolation.fetch(
            app_token,
            ["address like '%s%%'" % address.upper()],
        )

    @staticmethod
    def fetch_by_pin(app_token, pin):
        """Fetch a list of PropertyViolation objects from the KCMO Open Data
        API for a single KIVA pin.
        """

        return PropertyViolation.fetch(
            app_token,
            ["pin = %d" % pin],
        )

    @property
    def is_open(self):
        return self.status == PropertyViolation.STATUS_OPEN

    @property
    def is_closed(self):
        return self.status == PropertyViolation.STATUS_CLOSED

    @property
    def as_csv(self):
        """Returns a string containing this object's properties in CSV format."""

        fields = [
            "%d" % self.id_,
            "%d" % self.case_id,
            '"%s"' % self.status,
            '"%s"' % self.case_opened.strftime('%Y-%m-%d'),
            '"%s"' % self.case_closed.strftime('%Y-%m-%d') if self.case_closed else '',
            "%d" % self.days_open,
            '"%s"' % self.violation_entry_date.strftime('%Y-%m-%d'),
            '"%s"' % self.address,
            '"%s"' % self.county,
            '"%s"' % self.state,
            "%d" % self.zip_code,
            '%s' % self.coordinates.lat,
            '%s' % self.coordinates.lon,
            "%d" % self.pin,
            '"%s"' % self.council_district,
            '"%s"' % self.police_district,
            '"%s"' % self.inspection_area,
            '"%s"' % self.neighborhood,
            '"%s"' % self.mapping_location,
            '"%s"' % self.code.code,
            '"%s"' % self.code.description,
            '%d' % self.ordinance.chapter,
            '"%s"' % self.ordinance.ordinance,
        ]

        return ','.join(fields)
