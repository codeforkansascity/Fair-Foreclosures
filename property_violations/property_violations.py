from dateutil.parser import parse
from sodapy import Socrata

class PropertyViolationException(Exception):
    pass

class Coordinates:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return 'Coordintes: (%s, %s)' % (str(self.lat), str(self.lon))

class PropertyViolationCode:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    @property
    def is_infestation_violation(self):
        return self.code.startswith('NSINFEST')

    @property
    def is_fence_violation(self):
        return self.code.startswith('NSFENCE')

    def __str__(self):
        return 'Code: %s (%s)' % (self.code, self.description)

class PropertyViolationOrdinance:
    CHAPTER_FENCE = 'Fences and Walls'
    CHAPTER_NUISANCE = 'Nuisances'
    CHAPTER_PROPERTY_MAINTENANCE = 'Property Maintenance Code'
    CHAPTER_SOLID_WASTE = 'Solid Waste'
    CHAPTER_STREET = 'Streets, Sidewalks and Public Places'

    def __init__(self, chapter, ordinance):
        self.chapter = chapter
        self.ordinance = ordinance

    @property
    def chapter_title(self):
        title = ''

        if self.chapter == 27:
            title = PropertyViolationOrdinance.CHAPTER_FENCE
        elif self.chapter == 48:
            title = PropertyViolationOrdinance.CHAPTER_NUISANCE
        elif self.chapter == 56:
            title = PropertyViolationOrdinance.CHAPTER_PROPERTY_MAINTENANCE
        elif self.chapter == 62:
            title = PropertyViolationOrdinance.CHAPTER_SOLID_WASTE
        elif self.chapter == 64:
            title = PropertyViolationOrdinance.CHAPTER_STREET
        else:
            title = '(Unknown Ordinance Chapter)'

        return title

    @property
    def severity(self):
        severity = 0.0

        if self.chapter == 27:
            severity = 0.6
        elif self.chapter == 48:
            severity = 0.3
        elif self.chapter == 56:
            severity = 1.0
        elif self.chapter == 62:
            severity = 1.0
        elif self.chapter == 64:
            severity = 0.6
        else:
            severity = 1.0

        return severity

    def __str__(self):
        return 'Ordinance: %s (%s)' % (self.chapter, self.ordinance)

class PropertyViolation:
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

        violation.ordinance = PropertyViolationOrdinance(
            to_int(json_data.get('chapter')),
            json_data.get('ordinance'),
        )

        return violation

    @staticmethod
    def fetch(app_token, search_params):
        with Socrata(PropertyViolation.API_DATASET_NAME, app_token) as client:
            where_clause = ' and '.join(search_params)

            # Raises a requests.exceptions.HTTPError if bad criteria is given
            violation_records = client.get(
                PropertyViolation.API_RESOURCE_ID,
                where=where_clause,
            )

        return [PropertyViolation.from_json(rec) for rec in violation_records]

    @staticmethod
    def fetch_by_address(app_token, address):
        return PropertyViolation.fetch(
            app_token,
            ["address like '%s%%'" % address.upper()],
        )

    @staticmethod
    def fetch_by_pin(app_token, pin):
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
        fields = [
            "%d" % self.id_,
            "%d" % self.case_id,
            '"%s"' % self.status,
            '"%s"' % self.case_opened.strftime('%Y-%m-%d'),
            '"%s"' % self.case_closed.strftime('%Y-%m-%d'),
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
